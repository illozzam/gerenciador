from django.contrib import admin
from financeiro.models import FluxoDeCaixa


@admin.register(FluxoDeCaixa)
class FluxoDeCaixaAdmin(admin.ModelAdmin):
    list_display = ["descricao", "tipo", "data", "valor"]
    list_editable = ["valor"]
    list_filter = ["data", "tipo"]
    search_fields = ["descricao"]
