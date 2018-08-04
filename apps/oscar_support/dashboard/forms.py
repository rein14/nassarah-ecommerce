from django import forms
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from oscar.core.compat import get_user_model
from oscar.core.loading import get_model

from ..forms.widgets import AutoCompleteWidget
from ..forms.widgets import CustomRadioInput

User = get_user_model()
CommunicationEventType = get_model('customer', 'CommunicationEventType')
Message = get_model('oscar_support', 'Message')
Priority = get_model("oscar_support", "Priority")
Ticket = get_model('oscar_support', 'Ticket')
TicketStatus = get_model("oscar_support", "TicketStatus")
TicketType = get_model("oscar_support", "TicketType")

REQUESTER_FIELDS = ['requester', 'is_internal']
MESSAGE_FIELDS = ['subject', 'body']


class TicketCreateForm(forms.ModelForm):
    def get_message_fields(self):
        for field in self:
            if field.name in MESSAGE_FIELDS:
                yield field

    def get_property_fields(self):
        ignore_fields = REQUESTER_FIELDS + MESSAGE_FIELDS + ['status']
        for field in self:
            if field.name not in ignore_fields:
                yield field

    class Meta:
        model = Ticket
        fields = REQUESTER_FIELDS + [
            'status',
            'priority', 'type',
            'assigned_group', 'assignee',
        ] + MESSAGE_FIELDS
        widgets = {
            'status': forms.HiddenInput(),
            'priority': forms.Select(attrs={'style': 'width: 100%;'}),
            'type': forms.Select(attrs={'style': 'width: 100%;'}),
            'assigned_group': forms.Select(attrs={'style': 'width: 100%;'}),
        }


class TicketUpdateForm(forms.ModelForm):
    message_type = forms.ChoiceField(
        widget=CustomRadioInput(attrs={'class': 'radio-inline'}),
        choices=Message.MESSAGE_TYPES,
        label=_("Message type"),
        initial=Message.PUBLIC,
    )
    message_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        label=_("Message text"),
        required=False
    )

    def get_property_fields(self):
        for field in self:
            if not field.name.startswith('message'):
                yield field

    def get_message_fields(self):
        for field in self:
            if field.name.startswith('message'):
                yield field

    class Meta:
        model = Ticket
        fields = [
            'status',
            'priority',
            'assignee',
            'assigned_group',
            'message_type',
            'message_text'
        ]
        widgets = {
            'status': forms.HiddenInput(),
        }


class RequesterCreateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class PriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = ['name', 'comment', ]


class TicketStatusForm(forms.ModelForm):
    class Meta:
        model = TicketStatus
        fields = ['name', ]


class TicketTypeForm(forms.ModelForm):
    class Meta:
        model = TicketType
        fields = ['name', ]
