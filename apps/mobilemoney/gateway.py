from django.db import transaction
from apps.mobilemoney import models


@transaction.atomic
def create_transaction(order_number, total, *args, **kwargs):
    txn = models.MobileMoneyTransaction.objects.get_or_create(
        order_number=order_number,
        amount=total.incl_tax,
        currency=total.currency
    )
    return txn[0].reference
