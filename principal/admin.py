from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from principal.models import *


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
	list_display = ['variavel', 'valor']
	list_editable = ['valor']


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
	list_display = ['nomeUsuario', 'thumbnail', 'telefone']
