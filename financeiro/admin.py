from django.contrib import admin

from .models import ContasAPagar, ContasAReceber, FluxoDeCaixa


@admin.register(ContasAPagar)
class ContasAPagarAdmin(admin.ModelAdmin):
	list_display = ['descricao', 'data', 'valor', 'pago']
	list_editable = ['valor']
	list_filter = ['data', 'pago']
	search_fields = ['descricao']


@admin.register(ContasAReceber)
class ContasAReceberAdmin(admin.ModelAdmin):
	list_display = ['descricao', 'data', 'valor', 'recebido']
	list_editable = ['valor']
	list_filter = ['data', 'recebido']
	search_fields = ['descricao']


@admin.register(FluxoDeCaixa)
class FluxoDeCaixaAdmin(admin.ModelAdmin):
	list_display = ['descricao', 'tipo', 'data_hora', 'valor']
	list_editable = ['valor']
	list_filter = ['data_hora', 'tipo']
	search_fields = ['descricao']
