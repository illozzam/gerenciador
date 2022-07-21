from django.db import models
from django.utils import timezone
from financeiro.models import Categoria


class FluxoDeCaixa(models.Model):
    tipos_fluxo = [
        ["E", "Entrada"],
        ["S", "Saída"],
    ]

    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, null=True, blank=True
    )
    tipo = models.CharField(max_length=1, choices=tipos_fluxo)
    data = models.DateField(default=timezone.now())
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=50, verbose_name="descrição")

    def __str__(self):
        return self.descricao + " - R$ " + str(self.valor)

    class Meta:
        ordering = ["categoria", "-data", "descricao"]
        verbose_name = "fluxo de caixa"
        verbose_name_plural = "fluxos de caixa"
