from datetime import datetime
from urllib.parse import parse_qs

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from financeiro.models import ContasAPagar


@method_decorator(csrf_exempt, name="dispatch")
class ContasAPagarView(LoginRequiredMixin, View):
    def __reportar_pagamento(self, id_conta: int) -> int:
        conta = ContasAPagar.objects.get(id=id_conta)
        conta.pago = True
        conta.save()
        return 200


    def get(self, request, **kwargs):
        template = "financeiro/contas_a_pagar.html"
        contexto = {
            "contas": ContasAPagar.objects.all(),
        }
        return render(request, template, contexto)

    def post(self, request, **kwargs):
        resposta = dict()

        if request.POST.get("codigo_barras"):
            codigo_barras = (
                request.POST["codigo_barras"]
                .replace(" ", "")
                .replace(".", "")
                .replace("-", "")
            )
            codigo_barras = (
                codigo_barras.replace(" ", "").replace(".", "").replace("-", "")
            )
            for digito in range(4, len(codigo_barras) + 12, 5):
                codigo_barras = codigo_barras[0:digito] + " " + codigo_barras[digito:]
            if len(codigo_barras) == 60:
                codigo_barras = codigo_barras[:-1]
        else:
            codigo_barras = ""

        dados_cadastro = {
            "data": datetime.fromisoformat(request.POST["data"]),
            "valor": float(request.POST["valor"].replace(",", ".")),
            "descricao": request.POST["descricao"],
            "codigo_barras": codigo_barras,
        }
        conta = ContasAPagar.objects.create(**dados_cadastro)

        resposta["conta"] = serialize("json", [conta])
        resposta["status"] = 200
        return JsonResponse(resposta, safe=False)

    def put(self, request, **kwargs):
        payload = parse_qs(request.body.decode())
        resposta = dict()

        if payload["acao"][0] == "alterar-data":
            conta = ContasAPagar.objects.get(id=payload["id_conta"][0])
            conta.data = payload["data"][0]
            conta.save()
            resposta["status"] = 200
        elif payload["acao"][0] == "reportar-pagamento":
            resposta['status'] = self.__reportar_pagamento(payload["id_conta"][0])
        return JsonResponse(resposta)

    def delete(self, request, **kwargs):
        payload = parse_qs(request.body.decode())
        resposta = dict()
        if "id_conta" in payload.keys():
            if ContasAPagar.objects.filter(id=payload["id_conta"][0]).exists():
                ContasAPagar.objects.get(id=payload["id_conta"][0]).delete()
                resposta["status"] = 200
            else:
                resposta["status"] = 404
        else:
            resposta["status"] = 400
        return JsonResponse(resposta)
