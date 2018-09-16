from django.views.generic import ListView, DetailView

from apps.mobilemoney import models


class TransactionListView(ListView):
    model = models.MobileMoneyTransaction
    context_object_name = 'transactions'
    template_name = 'dashboard/mobilemoney/transaction_list.html'


class TransactionDetailView(DetailView):
    model = models.MobileMoneyTransaction
    context_object_name = 'txn'
    template_name = 'dashboard/mobilemoney/transaction_detail.html'
