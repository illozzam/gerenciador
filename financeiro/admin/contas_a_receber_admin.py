from django.contrib import admin
from financeiro.models import ContasAReceber


@admin.register(ContasAReceber)
class ContasAReceberAdmin(admin.ModelAdmin):
    list_display = ["descricao", "data", "valor", "recebido"]
    list_editable = ["valor"]
    list_filter = ["data", "recebido"]
    search_fields = ["descricao"]
