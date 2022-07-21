from django.contrib.admin import ModelAdmin, TabularInline, register
from financeiro.models import Categoria, TermoCategoria


class TermoCategoriaAdmin(TabularInline):
    model = TermoCategoria
    extra = 0


@register(Categoria)
class CategoriaAdmin(ModelAdmin):
    inlines = [TermoCategoriaAdmin]
    list_display = ["nome", "descricao"]
    search_fields = ["nome", "descricao"]
    ordering = ["nome"]
    save_on_top = True
