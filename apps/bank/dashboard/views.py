from django.views.generic import ListView, DetailView

from apps.bank import models


class TransactionListView(ListView):
    model = models.BankTransaction
    context_object_name = 'transactions'
    template_name = 'dashboard/bank/transaction_list.html'


class TransactionDetailView(DetailView):
    model = models.BankTransaction
    context_object_name = 'txn'
    template_name = 'dashboard/bank/transaction_detail.html'
