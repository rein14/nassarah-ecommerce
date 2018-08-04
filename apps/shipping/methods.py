from decimal import Decimal as D
from django.template.loader import render_to_string

from oscar.apps.shipping import methods
from oscar.core import prices


class OfficePickUp(methods.Base):
    code = 'Pick Up'
    name = 'Pick up from Office'
    description = ''

    def calculate(self, basket):
        return prices.Price(currency=basket.currency,
            excl_tax=D('0.00'), incl_tax=D('0.00'))


class Standard(methods.Base):
    code = 'standard'
    name = 'standard shipping'

    charge_per_item = D('0.99')
    description = ''
    days = ' including handling fee'
    '''render_to_string(
        'shipping/express.html', {'charge_per_item': charge_per_item})
'''
    def calculate(self, basket):
        total = basket.num_items * self.charge_per_item
        return prices.Price(
            currency=basket.currency,
            excl_tax=total,
            incl_tax=total)
