from django.contrib import admin
from financial.models import BillsToPay


@admin.register(BillsToPay)
class BillsToPayAdmin(admin.ModelAdmin):
    list_display = ["description", "date", "value", "paid"]
    list_editable = ["value"]
    list_filter = ["date", "paid"]
    search_fields = ["description"]
