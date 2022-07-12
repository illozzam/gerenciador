from django.contrib import admin
from financeiro.models import FluxoDeCaixa


@admin.register(FluxoDeCaixa)
class FluxoDeCaixaAdmin(admin.ModelAdmin):
    list_display = ["descricao", "tipo", "data_hora", "valor"]
    list_editable = ["valor"]
    list_filter = ["data_hora", "tipo"]
    search_fields = ["descricao"]
