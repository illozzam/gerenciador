from django.contrib import admin

from .models import Chave


@admin.register(Chave)
class ChaveAdmin(admin.ModelAdmin):
    list_display = ["chave", "data_hora", "verificada"]
