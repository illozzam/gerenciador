from django.contrib import admin
from financial.models import BillsToReceive


@admin.register(BillsToReceive)
class BillsToReceiveAdmin(admin.ModelAdmin):
    list_display = ["description", "date", "value", "received"]
    list_editable = ["value"]
    list_filter = ["date", "received"]
    search_fields = ["description"]
