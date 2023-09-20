from datetime import datetime
from urllib.parse import parse_qs

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from financial.models import BillsToReceive


@method_decorator(csrf_exempt, name="dispatch")
class BillsToReceiveView(LoginRequiredMixin, View):
    def __change_date(self, bill_id, date):
        bill = BillsToReceive.objects.get(id=bill_id)
        bill.date = date
        bill.save()
        return 200

    def __report_receipts(self, bill_id):
        bill = BillsToReceive.objects.get(id=bill_id)
        bill.received = True
        bill.save()
        return 200

    def get(self, request, **kwargs):
        template = "financial/bills_to_receive.html"
        context = {
            "bills": BillsToReceive.objects.all(),
        }
        return render(request, template, context)

    def put(self, request, **kwargs):
        payload = parse_qs(request.body.decode())
        response = {}

        if BillsToReceive.objects.filter(id=payload['id_conta'][0]).exists():
            if payload['action'][0] == "change-date":
                response["status"] = self.__change_date(
                    payload['bill_id'][0], payload['data'][0]
                )
            elif payload['action'][0] == "report-receipts":
                response["status"] = self.__report_receipts(
                    payload['bill_id'][0]
                )
        else:
            response["status"] = 404
        return JsonResponse(response)

    def post(self, request, **kwargs):
        response = dict()

        bill = BillsToReceive.objects.create(
            date=datetime.fromisoformat(request.POST.get('date')),
            value=float(request.POST.get('value').replace(',', '.')),
            description=request.POST.get('description'),
        )

        response["bill"] = serialize("json", [bill])
        response["status"] = 200
        return JsonResponse(response)

    def delete(self, request, **kwargs):
        payload = parse_qs(request.body.decode())
        response = dict()
        if BillsToReceive.objects.filter(id=payload["bill_id"][0]).exists():
            BillsToReceive.objects.get(id=payload["bill_id"][0]).delete()
            response["status"] = 200
        else:
            response["status"] = 404
        return JsonResponse(response)
