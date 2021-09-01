from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from principal.models import Config


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
	list_display = ['variavel', 'valor']
	list_editable = ['valor']
