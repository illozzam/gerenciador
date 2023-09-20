from datetime import datetime
from urllib.parse import parse_qs

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from financial.models import FinancialCategory, CashFlow
from main.models import Config


@method_decorator(csrf_exempt, name="dispatch")
class CashFlowView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        if (
            not "start_date" in request.GET.keys()
            or not "end_date" in request.GET.keys()
        ):
            context = {
                "categories": FinancialCategory.objects.all(),
                "last_bank_statement_date": datetime.fromisoformat(
                    Config.objects.get(variable="ultima_data_extrato_bancario").value
                ).strftime("%d/%m/%Y"),
            }
            template = "financial/cash_flow.html"
            return render(request, template, context)
        else:
            context = {}
            try:
                context["previous_balance"] = 0

                start_date = datetime.fromisoformat(
                    request.GET.get("start_date")
                ).replace(hour=0, minute=0, second=0, microsecond=0)
                end_date = datetime.fromisoformat(request.GET.get("end_date")).replace(
                    hour=23, minute=59, second=59, microsecond=999999
                )

                for transaction in CashFlow.objects.filter(data__lte=start_date):
                    if transaction.type == "E":
                        context["previous_balance"] += float(transaction.value)
                    else:
                        context["previous_balance"] -= float(transaction.value)

                context["transactions"] = serialize(
                    "json",
                    CashFlow.objects.filter(date__gte=start_date, date__lte=end_date),
                )
                context["status"] = 200
            except:
                context["status"] = 500
            return JsonResponse(context)

    def post(self, request, **kwargs):
        response = {}

        category = (
            FinancialCategory.objects.get(id=int(request.POST["category"]))
            if request.POST["category"] != "0"
            else None
        )

        CashFlow.objects.create(
            category=category,
            type=request.POST["type"],
            date=datetime.fromisoformat(request.POST["date"]),
            value=float(request.POST["value"].replace(",", ".")),
            description=request.POST["description"],
        )
        response["status"] = 200
        return JsonResponse(response)

    def delete(self, request, **kwargs):
        payload = parse_qs(request.body.decode())
        response = {}

        if CashFlow.objects.filter(id=payload["cash_flow_id"][0]).exists():
            try:
                CashFlow.objects.get(id=payload["cash_flow_id"][0]).delete()
                response["status"] = 200
            except:
                response["status"] = 404
        else:
            response["status"] = 500
        return JsonResponse(response)
