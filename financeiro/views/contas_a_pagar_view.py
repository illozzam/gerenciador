from datetime import datetime
from urllib.parse import parse_qs

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from financeiro.models import ContasAPagar, FluxoDeCaixa


@method_decorator(csrf_exempt, name="dispatch")
class ContasAPagarView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        template = "financeiro/contas_a_pagar.html"
        contexto = {
            "contas": ContasAPagar.objects.all(),
        }
        return render(request, template, contexto)

    def put(self, request, **kwargs):
        payload = parse_qs(request.body.decode())
        resposta = dict()

        if payload.get("codigo_barras"):
            codigo_barras = (
                payload["codigo_barras"][0]
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
            "data": datetime.strptime(payload["data"][0], "%Y-%m-%d"),
            "valor": float(payload["valor"][0].replace(",", ".")),
            "descricao": payload["descricao"][0],
            "codigo_barras": codigo_barras,
        }
        conta = ContasAPagar.objects.create(**dados_cadastro)

        resposta["conta"] = serialize("json", [conta])
        resposta["status"] = 200
        return JsonResponse(resposta, safe=False)

    def post(self, request, **kwargs):
        resposta = dict()

        if request.POST.get("acao") == "alterar-data":
            conta = ContasAPagar.objects.get(id=request.POST["id_conta"])
            conta.data = request.POST.get("data")
            conta.save()
            resposta["status"] = 200
        elif request.POST.get("acao") == "reportar-pagamento":
            conta = ContasAPagar.objects.get(id=request.POST["id_conta"])
            conta.pago = True
            conta.save()

            FluxoDeCaixa.objects.create(
                tipo="S", descricao=conta.descricao, valor=conta.valor
            )

            resposta["status"] = 200
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
