from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from financeiro.models import FluxoDeCaixa
from financeiro.services.extrato_bancario import ExtratoBancarioService


class ExtratoBancarioView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            movimentacoes = ExtratoBancarioService.extrair(
                request.FILES["extrato_bancario"]
            )
            FluxoDeCaixa.objects.bulk_create(movimentacoes)
            messages.success(request, 'Extrato bancário importado com sucesso!')
        except IndexError:
            messages.warning(request, 'Nenhuma movimentação encontrada após a última data cadastrada')
        except Exception as error:
            messages.error(request, str(error))
        return redirect("financeiro:fluxo-de-caixa")