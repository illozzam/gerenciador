from django.contrib.admin import ModelAdmin, TabularInline, register
from financial.models import FinancialCategory, FinancialTerm


class FinancialTermAdmin(TabularInline):
    model = FinancialTerm
    extra = 0


@register(FinancialCategory)
class FinancialCategoryAdmin(ModelAdmin):
    inlines = [FinancialTermAdmin]
    list_display = ["name", "description"]
    search_fields = ["name", "description"]
    ordering = ["name"]
    save_on_top = True
