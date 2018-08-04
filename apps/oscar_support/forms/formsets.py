from django.forms import formset_factory, modelformset_factory
from django.forms import inlineformset_factory
from oscar.core.loading import get_model
from oscar_support.dashboard.forms import (
    PriorityForm,
    TicketStatusForm,
    TicketTypeForm
)

from oscar_support.forms import (
    AttachmentForm,
    RelatedOrderForm,
    RelatedOrderLineForm,
    RelatedProductForm,
)

Attachment = get_model('oscar_support', 'Attachment')
Order = get_model('order', 'Order')
RelatedOrder = get_model("oscar_support", "RelatedOrder")
Priority = get_model("oscar_support", "Priority")
RelatedOrderLine = get_model("oscar_support", "RelatedOrderLine")
RelatedProduct = get_model("oscar_support", "RelatedProduct")
Ticket = get_model("oscar_support", "Ticket")
TicketStatus = get_model("oscar_support", "TicketStatus")
TicketType = get_model("oscar_support", "TicketType")

BaseAttachmentFormSet = inlineformset_factory(
    Ticket, Attachment, form=AttachmentForm, extra=2,
    can_delete=True)


class AttachmentFormSet(BaseAttachmentFormSet):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AttachmentFormSet, self).__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['user'] = self.user
        return super(AttachmentFormSet, self)._construct_form(
            i, **kwargs)


BaseRelatedOrderFormSet = inlineformset_factory(
    Ticket, RelatedOrder, form=RelatedOrderForm, extra=1,
    can_delete=True)


class RelatedOrderFormSet(BaseRelatedOrderFormSet):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(RelatedOrderFormSet, self).__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['user'] = self.user
        return super(RelatedOrderFormSet, self)._construct_form(
            i, **kwargs)

    def get_num_orders(self):
        num_orders = 0
        for i in range(0, self.total_form_count()):
            form = self.forms[i]
            if (hasattr(form, 'cleaned_data')
                and form.cleaned_data.get('order', None)
                and not form.cleaned_data.get('DELETE', False)):
                num_orders += 1
        return num_orders


BaseRelatedOrderLineFormSet = inlineformset_factory(
    Ticket, RelatedOrderLine, form=RelatedOrderLineForm, extra=1,
    can_delete=True)


class RelatedOrderLineFormSet(BaseRelatedOrderLineFormSet):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(RelatedOrderLineFormSet, self).__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['user'] = self.user
        return super(RelatedOrderLineFormSet, self)._construct_form(
            i, **kwargs)


BaseRelatedProductFormSet = inlineformset_factory(
    Ticket, RelatedProduct, form=RelatedProductForm, extra=5,
    can_delete=True)


class RelatedProductFormSet(BaseRelatedProductFormSet):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(RelatedProductFormSet, self).__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['user'] = self.user
        return super(RelatedProductFormSet, self)._construct_form(
            i, **kwargs)
