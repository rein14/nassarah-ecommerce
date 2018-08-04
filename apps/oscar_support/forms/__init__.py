from django import forms
from django.utils.translation import ugettext_lazy as _

from oscar.core.loading import get_model

from .. import utils

Attachment = get_model('oscar_support', 'Attachment')
Order = get_model('order', 'Order')
RelatedOrder = get_model("oscar_support", "RelatedOrder")
RelatedOrderLine = get_model("oscar_support", "RelatedOrderLine")
RelatedProduct = get_model("oscar_support", "RelatedProduct")


class AttachmentForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AttachmentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Attachment
        fields = ['ticket', 'file', ]

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(AttachmentForm, self).save(*args, **kwargs)
        obj.user = self.user
        obj.save()
        return obj


class RelatedOrderForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(RelatedOrderForm, self).__init__(*args, **kwargs)

    class Meta:
        model = RelatedOrder
        fields = ['order']

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(RelatedOrderForm, self).save(*args, **kwargs)
        obj.user = self.user
        obj.save()
        return obj


class RelatedOrderLineForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(RelatedOrderLineForm, self).__init__(*args, **kwargs)

    class Meta:
        model = RelatedOrderLine
        fields = ['line']

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(RelatedOrderLineForm, self).save(*args, **kwargs)
        obj.user = self.user
        obj.save()
        return obj


class RelatedProductForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(RelatedProductForm, self).__init__(*args, **kwargs)

    class Meta:
        model = RelatedProduct
        fields = ['product']

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(RelatedProductForm, self).save(*args, **kwargs)
        obj.user = self.user
        obj.save()
        return obj


class TicketUpdateForm(forms.ModelForm):
    message_text = forms.CharField(label=_("Message"), widget=forms.Textarea())

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(TicketUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = get_model("oscar_support", "Ticket")
        fields = ['message_text']


class TicketCreateForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(TicketCreateForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(TicketCreateForm, self).save(*args, **kwargs)
        obj.status = utils.TicketStatusGenerator.get_initial_status()
        obj.requester = self.user
        obj.save()
        return obj

    class Meta:
        model = get_model("oscar_support", "Ticket")
        fields = ['type', 'subject', 'body']
