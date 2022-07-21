from datetime import datetime
from urllib.parse import parse_qs

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from financeiro.models import ContasAReceber, FluxoDeCaixa


@method_decorator(csrf_exempt, name="dispatch")
class ContasAReceberView(LoginRequiredMixin, View):
    def alterar_data(self, id_conta, data):
        conta = ContasAReceber.objects.get(id=id_conta)
        conta.data = data
        conta.save()
        return 200

    def reportar_recebimento(self, id_conta):
        conta = ContasAReceber.objects.get(id=id_conta)
        conta.recebido = True
        conta.save()

        FluxoDeCaixa.objects.create(
            tipo="E", descricao=conta.descricao, valor=conta.valor
        )
        return 200

    def get(self, request, **kwargs):
        template = "financeiro/contas_a_receber.html"
        contexto = {
            "contas": ContasAReceber.objects.all(),
        }
        return render(request, template, contexto)

    def put(self, request, **kwargs):
        payload = parse_qs(request.body.decode())
        resposta = dict()

        conta = ContasAReceber.objects.create(
            data=datetime.strptime(payload["data"][0], "%Y-%m-%d"),
            valor=float(payload["valor"][0].replace(",", ".")),
            descricao=payload["descricao"][0],
        )

        resposta["conta"] = serialize("json", [conta])
        resposta["status"] = 200
        return JsonResponse(resposta)

    def post(self, request, **kwargs):
        resposta = dict()

        if ContasAReceber.objects.filter(id=request.POST.get("id_conta")).exists():
            if request.POST.get("acao") == "alterar-data":
                resposta["status"] = self.alterar_data(
                    request.POST.get("id_conta"), request.POST.get("data")
                )
                return JsonResponse(resposta)
            elif request.POST.get("acao") == "reportar-recebimento":
                resposta["status"] = self.reportar_recebimento(
                    request.POST.get("id_conta")
                )
        else:
            resposta["status"] = 404
        return JsonResponse(resposta)

    def delete(self, request, **kwargs):
        payload = parse_qs(request.body.decode())
        resposta = dict()
        if ContasAReceber.objects.filter(id=payload["id_conta"][0]).exists():
            ContasAReceber.objects.get(id=payload["id_conta"][0]).delete()
            resposta["status"] = 200
        else:
            resposta["status"] = 404
        return JsonResponse(resposta)
