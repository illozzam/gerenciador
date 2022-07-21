from django.contrib import admin
from financeiro.models import ContasAPagar


@admin.register(ContasAPagar)
class ContasAPagarAdmin(admin.ModelAdmin):
    list_display = ["descricao", "data", "valor", "pago"]
    list_editable = ["valor"]
    list_filter = ["data", "pago"]
    search_fields = ["descricao"]
