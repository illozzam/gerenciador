from datetime import datetime
from urllib.parse import parse_qs

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from financial.models import BillsToPay


@method_decorator(csrf_exempt, name="dispatch")
class BillsToPayView(LoginRequiredMixin, View):
    def __report_payment(self, bill_id: int) -> int:
        bill = BillsToPay.objects.get(id=bill_id)
        bill.paid = True
        bill.save()
        return 200


    def get(self, request, **kwargs):
        template = "financial/bills_to_pay.html"
        context = {
            "bills": BillsToPay.objects.all(),
        }
        return render(request, template, context)

    def post(self, request, **kwargs):
        response = dict()

        if request.POST.get("barcode"):
            barcode = (
                request.POST["barcode"]
                .replace(" ", "")
                .replace(".", "")
                .replace("-", "")
            )
            barcode = (
                barcode.replace(" ", "").replace(".", "").replace("-", "")
            )
            for digit in range(4, len(barcode) + 12, 5):
                barcode = barcode[0:digit] + " " + barcode[digit:]
            if len(barcode) == 60:
                barcode = barcode[:-1]
        else:
            barcode = ""

        bill_data = {
            "date": datetime.fromisoformat(request.POST["date"]),
            "value": float(request.POST["value"].replace(",", ".")),
            "description": request.POST["description"],
            "barcode": barcode,
        }
        bill = BillsToPay.objects.create(**bill_data)

        response["bill"] = serialize("json", [bill])
        response["status"] = 200
        return JsonResponse(response, safe=False)

    def put(self, request, **kwargs):
        payload = parse_qs(request.body.decode())
        response = dict()

        if payload["action"][0] == "change-date":
            bill = BillsToPay.objects.get(id=payload["bill_id"][0])
            bill.date = payload["date"][0]
            bill.save()
            response["status"] = 200
        elif payload["action"][0] == "report-payment":
            response['status'] = self.__report_payment(payload["bill_id"][0])
        return JsonResponse(response)

    def delete(self, request, **kwargs):
        payload = parse_qs(request.body.decode())
        response = dict()
        if "bill_id" in payload.keys():
            if BillsToPay.objects.filter(id=payload["bill_id"][0]).exists():
                BillsToPay.objects.get(id=payload["bill_id"][0]).delete()
                response["status"] = 200
            else:
                response["status"] = 404
        else:
            response["status"] = 400
        return JsonResponse(response)
