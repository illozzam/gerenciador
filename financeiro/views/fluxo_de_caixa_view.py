from datetime import datetime
from urllib.parse import parse_qs

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from financeiro.models import FluxoDeCaixa, Categoria


@method_decorator(csrf_exempt, name="dispatch")
class FluxoDeCaixaView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        if (
            not "data_inicial" in request.GET.keys()
            or not "data_final" in request.GET.keys()
        ):
            contexto = {"categorias": Categoria.objects.all()}
            template = "financeiro/fluxo_de_caixa.html"
            return render(request, template, contexto)
        else:
            contexto = {}
            try:
                contexto["saldo_anterior"] = 0

                data_inicial = datetime.fromisoformat(
                    request.GET.get("data_inicial")
                ).replace(hour=0, minute=0, second=0, microsecond=0)
                data_final = datetime.fromisoformat(
                    request.GET.get("data_final")
                ).replace(hour=23, minute=59, second=59, microsecond=999999)

                for movimentacao in FluxoDeCaixa.objects.filter(data__lte=data_inicial):
                    if movimentacao.tipo == "E":
                        contexto["saldo_anterior"] += float(movimentacao.valor)
                    else:
                        contexto["saldo_anterior"] -= float(movimentacao.valor)

                contexto["movimentacoes"] = serialize(
                    "json",
                    FluxoDeCaixa.objects.filter(
                        data__gte=data_inicial, data__lte=data_final
                    ),
                )
                contexto["status"] = 200
            except:
                contexto["status"] = 500
            return JsonResponse(contexto)

    def post(self, request, **kwargs):
        resposta = {}

        categoria = (
            Categoria.objects.get(id=int(request.POST["categoria"]))
            if request.POST["categoria"] != "0"
            else None
        )

        FluxoDeCaixa.objects.create(
            categoria=categoria,
            tipo=request.POST["tipo"],
            data=datetime.fromisoformat(request.POST["data"]),
            valor=float(request.POST["valor"].replace(",", ".")),
            descricao=request.POST["descricao"],
        )
        resposta["status"] = 200
        return JsonResponse(resposta)

    def delete(self, request, **kwargs):
        payload = parse_qs(request.body.decode())
        resposta = {}

        if FluxoDeCaixa.objects.filter(id=payload["fluxo_de_caixa_id"][0]).exists():
            try:
                FluxoDeCaixa.objects.get(id=payload["fluxo_de_caixa_id"][0]).delete()
                resposta["status"] = 200
            except:
                resposta["status"] = 404
        else:
            resposta["status"] = 500
        return JsonResponse(resposta)
