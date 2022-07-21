from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from financeiro.models import FluxoDeCaixa
from financeiro.services.extrato_bancario import ExtratoBancarioService


class ExtratoBancarioView(LoginRequiredMixin, View):
    def post(self, request):
        resposta = {
            "status": "",
            "mensagem": "",
        }

        try:
            movimentacoes = ExtratoBancarioService.extrair(
                request.FILES["extrato_bancario"]
            )
            FluxoDeCaixa.objects.bulk_create(movimentacoes)
        except Exception as error:
            resposta["status"] = "ERRO"
            resposta["mensagem"] = str(error)
            messages.error(request, str(error))
            return JsonResponse(resposta)

        resposta["status"] = "OK"
        return JsonResponse(resposta)
