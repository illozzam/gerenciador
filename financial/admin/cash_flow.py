from django.contrib import admin
from financial.models import CashFlow


@admin.register(CashFlow)
class CashFlowAdmin(admin.ModelAdmin):
    list_display = ["description", "type", "date", "value"]
    list_editable = ["value"]
    list_filter = ["date", "type", "category"]
    search_fields = ["description"]
