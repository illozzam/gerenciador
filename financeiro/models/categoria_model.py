from django.db import models


class TermoCategoria(models.Model):
    termo = models.CharField(max_length=50)

    def __str__(self):
        return self.termo


class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField(null=True, blank=True)
    termos = models.ManyToManyField(TermoCategoria, null=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"
