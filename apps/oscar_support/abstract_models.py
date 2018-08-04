from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from shortuuidfield import ShortUUIDField
from django_extensions.db.fields import AutoSlugField

from oscar.core.compat import AUTH_USER_MODEL

from .utils import TicketNumberGenerator
from .mixins import ModificationTrackingMixin


class BaseSupportModel(models.Model):
    uuid = ShortUUIDField(_("UUID"), primary_key=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class AbstractTicketType(BaseSupportModel):
    slug = AutoSlugField(_("Slug"), populate_from='name', unique=True)
    name = models.CharField(_("Name"), max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = _("Ticket type")
        verbose_name_plural = _("Ticket types")


@python_2_unicode_compatible
class AbstractTicketStatus(BaseSupportModel):
    slug = AutoSlugField(_("Slug"), populate_from='name', unique=True)
    name = models.CharField(_("Name"), max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = _("Ticket status")
        verbose_name_plural = _("Ticket statuses")


@python_2_unicode_compatible
class AbstractTicket(ModificationTrackingMixin, BaseSupportModel):
    number = models.CharField(
        _("Number"),
        max_length=64,
        db_index=True
    )
    subticket_id = models.PositiveIntegerField(
        _("Subticket number"),
        default=0,
    )
    parent = models.ForeignKey(
        'Ticket',
        verbose_name=_("Parent ticket"),
        related_name="subtickets",
        null=True,
        blank=True
    )
    requester = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name=_("Requester"),
        related_name='submitted_tickets'
    )
    status = models.ForeignKey(
        'TicketStatus',
        verbose_name=_("Status"),
        related_name="tickets"
    )
    type = models.ForeignKey(
        'TicketType',
        verbose_name=_("Type"),
        related_name="tickets",
    )

    assigned_group = models.ForeignKey(
        'auth.Group',
        verbose_name=_("Assigned group"),
        related_name="tickets",
        null=True,
        blank=True,
    )
    assignee = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name=_("Assignee"),
        related_name="assigned_tickets",
        null=True,
        blank=True,
    )

    # main content of the (initial) ticket
    subject = models.CharField(_("Subject"), max_length=255)
    body = models.TextField(_("Body"), blank=True)
    # TODO: In CreateForm in dashboard JS give us: An invalid form control with name='body' is not focusable,
    # for avoid it was needed make BODY unrequired, putting "black=true" property. It doesn't happen in customer view.

    priority = models.ForeignKey(
        'Priority',
        verbose_name=_("Priority"),
        related_name='tickets',
        null=True,
        blank=True
    )

    related_lines = models.ManyToManyField(
        'order.Line',
        verbose_name=_("Related order lines"),
        related_name='tickets',
        through='RelatedOrderLine',
        blank=True,
    )
    related_orders = models.ManyToManyField(
        'order.Order',
        verbose_name=_("Related Orders"),
        related_name='tickets',
        through='RelatedOrder',
        blank=True,
    )
    related_products = models.ManyToManyField(
        'catalogue.Product',
        verbose_name=_("Related products"),
        related_name='tickets',
        through='RelatedProduct',
        blank=True,
    )

    is_internal = models.BooleanField(
        _("Internal ticket"),
        default=False,
        help_text=_("use this ticket only internally and don't display to "
                    "the customer")
    )

    @property
    def printable_number(self):
        if self.subticket_id:
            return "{0}-{1}".format(self.number, self.subticket_id)
        return self.number

    def save(self, *args, **kwargs):
        if not self.number:
            ticket_numbers = TicketNumberGenerator.generate_ticket_number()
            self.number = ticket_numbers['number']
            self.subticket_id = ticket_numbers['subticket_id']
        return super(AbstractTicket, self).save(*args, **kwargs)

    def __str__(self):
        return _("Ticket #{0}").format(self.printable_number)

    def get_absolute_url(self):
        """
        Return a product's absolute url
        """
        return reverse('support:customer-ticket-update',
                       kwargs={'pk': self.uuid})

    class Meta:
        abstract = True
        # we want the oldest tickets to be first in the queue so that
        # they get updated before newer ones (FIFO queue handling)
        ordering = ['-date_updated']
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")
        unique_together = (('number', 'subticket_id'),)


@python_2_unicode_compatible
class AbstractPriority(BaseSupportModel):
    name = models.CharField(_("Name"), max_length=255)
    slug = AutoSlugField(_("Slug"), populate_from='name')
    comment = models.TextField(_("Comment"), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = _("Priority")
        verbose_name_plural = _("Priorities")


@python_2_unicode_compatible
class AbstractMessage(ModificationTrackingMixin, BaseSupportModel):
    PUBLIC = u'public'
    INTERNAL = u'internal'
    MESSAGE_TYPES = (
        (PUBLIC, _("Public message")),
        (INTERNAL, _("Internal note")),
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name=_("Sender"),
        related_name="messages"
    )
    type = models.CharField(
        _("Message type"),
        max_length=30,
        choices=MESSAGE_TYPES,
        default=PUBLIC,
    )
    ticket = models.ForeignKey(
        'Ticket',
        verbose_name=_("Ticket"),
        related_name="messages"
    )
    text = models.TextField(_("Text"))

    @property
    def is_internal(self):
        return self.type == self.INTERNAL

    def __str__(self):
        return _("{0} from {1} for {2}").format(
            self.type,
            self.user.email,
            self.ticket
        )

    class Meta:
        abstract = True
        ordering = ['-date_created']
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")


@python_2_unicode_compatible
class AbstractRelatedItem(ModificationTrackingMixin, BaseSupportModel):
    ticket = models.ForeignKey(
        'Ticket',
        verbose_name=_("Ticket"),
        related_name="%(class)ss",
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name=_("Added by"),
        related_name="%(class)ss",
    )

    def __str__(self):
        return _("{0} related to {1}").format(self.ticket, self.user)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class AbstractRelatedOrderLine(AbstractRelatedItem):
    line = models.ForeignKey(
        "order.Line",
        verbose_name=_("Order line"),
        related_name="ticket_related_order_lines",
    )

    def __str__(self):
        return _("{0} related to {1}").format(self.line, self.ticket)

    class Meta:
        abstract = True
        verbose_name = _("Related order line")
        verbose_name_plural = _("Related order lines")


@python_2_unicode_compatible
class AbstractRelatedOrder(AbstractRelatedItem):
    order = models.ForeignKey(
        "order.Order",
        verbose_name=_("Order"),
        related_name="ticket_related_orders",
    )

    def __str__(self):
        return _("{0} related to {1}").format(self.order, self.ticket)

    class Meta:
        abstract = True
        verbose_name = _("Related order")
        verbose_name_plural = _("Related orders")


@python_2_unicode_compatible
class AbstractRelatedProduct(AbstractRelatedItem):
    product = models.ForeignKey(
        "catalogue.Product",
        verbose_name=_("Product"),
        related_name="ticket_related_products",
    )

    def __str__(self):
        return _("{0} related to {1}").format(self.product, self.ticket)

    class Meta:
        abstract = True
        verbose_name = _("Related product")
        verbose_name_plural = _("Related products")


@python_2_unicode_compatible
class AbstractAttachment(ModificationTrackingMixin, BaseSupportModel):
    ticket = models.ForeignKey(
        'Ticket',
        verbose_name=_("Ticket"),
        related_name="attachments",
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name=_("User"),
        related_name="attachments"
    )
    file = models.FileField(
        upload_to="oscar_support/%Y/%m",
        verbose_name=_("File"),
        help_text=_("Add documents that present important information to understand the problem, "
                    "such as: invoices, catalogs, photos, orders, etc.")
    )

    def __str__(self):
        return _("{0} attached to {1}").format(self.file.url, self.ticket)

    class Meta:
        abstract = True
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")
