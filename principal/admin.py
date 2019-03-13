#coding: utf-8
from django.contrib import admin
from principal.models import *
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
	list_display = ['variavel', 'valor']
	list_editable = ['valor']

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
	list_display = ['nomeUsuario', 'thumbnail', 'telefone']

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
	list_display = ['nome', 'uf', 'ordem']
	list_editable = ['ordem']

@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
	list_display = ['nome', 'estado', 'ordem']
	list_editable = ['ordem']

@admin.register(RamoConsultoria)
class RamoConsultoriaAdmin(admin.ModelAdmin):
	list_display = ['nome']

@admin.register(Consultoria)
class ConsultoriaAdmin(admin.ModelAdmin):
	list_display = ['empresa', 'enviado', 'dominio', 'dataHoraInclusao', 'dataHoraEnvio']
	list_filter = ['ramoAtividade', 'usuario', 'dataHoraInclusao', 'dataHoraEnvio']
	search_fields = ['empresa', 'dominio', 'email']

@admin.register(Mensagem)
class MensagemAdmin(SummernoteModelAdmin):
	list_display = ['remetente', 'destinatario', 'dataHoraEnvio', 'lida']

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

@admin.register(Tesouraria)
class TesourariaAdmin(admin.ModelAdmin):
	list_display = ['descricao', 'tipo', 'dataHora', 'valor']
	list_editable = ['valor']
	list_filter = ['dataHora', 'tipo']
	search_fields = ['descricao']

@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
	list_display = ['numero', 'cliente', 'servico', 'valor']

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
	list_display = ['nome', 'valor']
	list_editable = ['valor']

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
	list_display = ['nome', 'valor']
	list_editable = ['valor']

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
	list_display = ['usuarioOrigem', 'usuarioDestino', 'dataHoraInclusao', 'titulo', 'prioridade', 'status']
	list_editable = ['prioridade', 'status']
	list_filter = ['status', 'prioridade', 'data', 'usuarioDestino']

admin.site.register(Cliente)
