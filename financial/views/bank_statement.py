from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from financial.models import CashFlow
from financial.services.bank_statement import BankStatementService


class BankStatementView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            transactions = BankStatementService.extract(request.FILES["bank_statement"])
            CashFlow.objects.bulk_create(transactions)
            messages.success(request, "Extrato bancário importado com sucesso!")
        except IndexError:
            messages.warning(
                request, "Nenhuma movimentação encontrada após a última data cadastrada"
            )
        except Exception as error:
            messages.error(request, str(error))
        return redirect("financial:cash_flow")
