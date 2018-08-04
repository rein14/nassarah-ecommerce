from django.forms.widgets import Widget
from django.forms.widgets import RadioSelect
from django.template.loader import render_to_string

try:
    from django.utils.encoding import force_unicode as force_text
except ImportError:
    from django.utils.encoding import force_text


class AutoCompleteWiget(Widget):

    def __init__(self, url, user_field=None, *args, **kwargs):
        self.url = url
        self.user_field = user_field
        super(AutoCompleteWiget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = u''
        ctx = {
            'name': name,
            'url': self.url,
            'user_field': self.user_field,
            'value': value,
        }
        return render_to_string('oscar_support/widgets/autocomplete_widget.html', context=ctx)

AutoCompleteWidget = AutoCompleteWiget


class CustomRadioInput(RadioSelect):
    template_name = 'oscar_support/partials/custom_radio_select.html'
    option_template_name = 'oscar_support/partials/custom_radio_option.html'
