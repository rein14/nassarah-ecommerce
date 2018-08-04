from oscar.apps.order import processing
from oscar.apps.payment import exceptions

from .models import PaymentEventType


class EventHandler(processing.EventHandler):

    def handle_shipping_event(self, order, event_type, lines,
                              line_quantities, **kwargs):
        self.validate_shipping_event(
            order, event_type, lines, line_quantities, **kwargs)

        payment_event = None
        if event_type.name == 'Shipped':
            # Take payment for order lines
           
            self.consume_stock_allocations(
                order, lines, line_quantities)

        shipping_event = self.create_shipping_event(
            order, event_type, lines, line_quantities,
            reference=kwargs.get('reference', None))
        if payment_event:
            shipping_event.payment_events.add(payment_event)
            