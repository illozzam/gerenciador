import codecs
import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from financeiro.models import ContasAPagar, ContasAReceber, FluxoDeCaixa
from datetime import datetime


class ExtratoBancarioView(LoginRequiredMixin, View):
    def post(self, request):
        resposta = {
            "status": "",
            "mensagem": "",
        }

        movimentacoes = []

        leitor = csv.reader(
            codecs.iterdecode(request.FILES["extrato_bancario"], "utf-8"), delimiter=";"
        )

        for linha in leitor:
            if len(linha) == 4 and linha[0] != "DATA LANÇAMENTO":
                movimentacoes.append(
                    FluxoDeCaixa(
                        # TODO: Definir categoria
                        tipo='S' if float(linha[2]) < 0 else 'E',
                        data_hora=datetime.strptime(linha[0], "%d/%m/%Y").replace(hour=9, minute=0, second=0, microsecond=0),
                        valor=abs(float(linha[2])),
                        descricao=linha[1],
                    )
                )

        resposta["status"] = "OK"
        return JsonResponse(resposta)
