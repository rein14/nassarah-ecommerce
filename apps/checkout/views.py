from django.utils import six
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import FormView
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse, reverse_lazy
import logging

from . import forms

from apps.cashondelivery import gateway as cod_gateway
from apps.mobilemoney import gateway as momo_gateway
from apps.bank import gateway as bank_gateway


from oscar.apps.checkout import exceptions
from oscar.core.loading import get_model, get_class

Source = get_model("payment", "Source")
SourceType = get_model("payment", "SourceType")
RedirectRequired = get_class("payment.exceptions", "RedirectRequired")
UnableToPlaceOrder = get_class('order.exceptions', 'UnableToPlaceOrder')
OscarPaymentMethodView = get_class("checkout.views", "PaymentMethodView")
OscarPaymentDetailsView = get_class("checkout.views", "PaymentDetailsView")
OscarShippingMethodView = get_class("checkout.views", "ShippingMethodView")

logger = logging.getLogger(__name__)


# Inspired by https://github.com/django-oscar/django-oscar-docdata/blob/master/sandbox/apps/checkout/views.py
class PaymentMethodView(OscarPaymentMethodView, FormView):
    """
    View for a user to choose which payment method(s) they want to use.

    This would include setting allocations if payment is to be split
    between multiple sources. It's not the place for entering sensitive details
    like bankcard numbers though - that belongs on the payment details view.
    """
    template_name = "checkout/payment_method.html"
    step = 'payment-method'
    form_class = forms.PaymentMethodForm
    success_url = reverse_lazy('checkout:preview')

    pre_conditions = [
        'check_basket_is_not_empty',
        'check_basket_is_valid',
        'check_user_email_is_captured',
        'check_shipping_data_is_captured',
        'check_payment_data_is_captured',
    ]
    skip_conditions = ['skip_unless_payment_is_required']

    def get(self, request, *args, **kwargs):
        # if only single payment method, store that
        # and then follow default (redirect to preview)
        # else show payment method choice form
        if len(settings.OSCAR_PAYMENT_METHODS) == 1:
            self.checkout_session.pay_by(settings.OSCAR_PAYMENT_METHODS[0][0])
            return redirect(self.get_success_url())
        else:
            return FormView.get(self, request, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        # Redirect to the correct payments page as per the method (different methods may have different views &/or additional views)
        return reverse_lazy('checkout:preview')

    def get_initial(self):
        return {
            'payment_method': self.checkout_session.payment_method(),
        }

    def form_valid(self, form):
        # Store payment method in the CheckoutSessionMixin.checkout_session (a CheckoutSessionData object)
        self.checkout_session.pay_by(form.cleaned_data['payment_method'])
        return super().form_valid(form)


class PaymentDetailsView(OscarPaymentDetailsView):

    def handle_payment(self, order_number, order_total, **kwargs):
        method = self.checkout_session.payment_method()
        if method == 'cod':
            return self.handle_cod_payment(order_number, order_total, **kwargs)
        elif method == 'mobilemoney':
            return self.handle_momo_payment(order_number, order_total, **kwargs)
        elif method == 'bank':
            return self.handle_bank_payment(order_number, order_total, **kwargs)
        else:
            pass

    def handle_cod_payment(self, order_number, total, **kwargs):
        reference = cod_gateway.create_transaction(order_number, total)
        source_type, is_created = SourceType.objects.get_or_create(
            name='cash on delivery')
        source = Source(
            source_type=source_type,
            currency=total.currency,
            amount_allocated=total.incl_tax,
            amount_debited=total.incl_tax
        )
        self.add_payment_source(source)
        self.add_payment_event('awaiting-delivery', total.incl_tax, reference=reference)

    def handle_momo_payment(self, order_number, total, **kwargs):
            reference = momo_gateway.create_transaction(order_number, total)
            source_type, is_created = SourceType.objects.get_or_create(
                name='mobile money')
            source = Source(
                source_type=source_type,
                currency=total.currency,
                amount_allocated=total.incl_tax,
                amount_debited=total.incl_tax
            )
            self.add_payment_source(source)
            self.add_payment_event('awaiting-delivery', total.incl_tax, reference=reference)
    
    def handle_bank_payment(self, order_number, total, **kwargs):
            reference = bank_gateway.create_transaction(order_number, total)
            source_type, is_created = SourceType.objects.get_or_create(
                name='bank payment')
            source = Source(
                source_type=source_type,
                currency=total.currency,
                amount_allocated=total.incl_tax,
                amount_debited=total.incl_tax
            )
            self.add_payment_source(source)
            self.add_payment_event('awaiting-delivery', total.incl_tax, reference=reference)
            
    def _save_order(self, order_number, submission):
        # Finalize the order that PaymentDetailsView.submit() started
        # If all is ok with payment, try and place order
        logger.info("Order #%s: payment started, placing order", order_number)

        try:
            # Call OrderPlacementMixin.handle_order_placement()
            return self.handle_order_placement(
                order_number, submission['user'], submission['basket'],
                submission['shipping_address'], submission['shipping_method'],
                submission['shipping_charge'], submission['billing_address'],
                submission['order_total'], **(submission['order_kwargs'])
            )
        except UnableToPlaceOrder as e:
            # It's possible that something will go wrong while trying to
            # actually place an order.  Not a good situation to be in as a
            # payment transaction may already have taken place, but needs
            # to be handled gracefully.
            logger.error("Order #%s: unable to place order - %s", order_number, e, exc_info=True)
            msg = six.text_type(e)
            self.restore_frozen_basket()
            return self.render_to_response(self.get_context_data(error=msg))

    # Can't update CheckoutSessionMixin nicely without causing trouble,
    # hence dumping the overridden / new methods from that class here
    def check_payment_data_is_captured(self, request):
        pass
        