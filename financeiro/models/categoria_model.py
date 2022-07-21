from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"


class TermoCategoria(models.Model):
    termo = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.termo

    class Meta:
        verbose_name = "termo de categoria"
        verbose_name_plural = "termos de categoria"
