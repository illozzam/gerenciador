from django.urls import path

from .views import (
    BillsToPayView,
    BillsToReceiveView,
    BankStatementView,
    CashFlowView,
)

urlpatterns = [
    path("bills-to-pay/", BillsToPayView.as_view(), name="bills-to-pay"),
    path("bills-to-receive/", BillsToReceiveView.as_view(), name="bills-to-receive"),
    path("cash-flow/", CashFlowView.as_view(), name="cash-flow"),
    path("bank-statement/", BankStatementView.as_view(), name="bank-statement"),
]
