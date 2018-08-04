from django.contrib import admin
from apps.cashondelivery.models import CashOnDeliveryTransaction


class CashOnDeliveryTransactionAdmin(admin.ModelAdmin):
    readonly_fields = [
        'order_number',
        'method',
        'amount',
        'reference',
        'confirmed',
        'date_confirmed',
        'date_created'
    ]

    list_display = [
        'order_number',
        'date_created',
        'amount',
        'currency',
        'confirmed',
        'date_confirmed',
    ]

    list_filter = [
        'confirmed'
    ]


admin.site.register(CashOnDeliveryTransaction, CashOnDeliveryTransactionAdmin)
