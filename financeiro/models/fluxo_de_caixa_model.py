from django.db import models
from django.utils import timezone


class FluxoDeCaixa(models.Model):
    tipos_fluxo = [
        ["E", "Entrada"],
        ["S", "Saída"],
    ]

    tipo = models.CharField(max_length=1, choices=tipos_fluxo)
    data_hora = models.DateTimeField(default=timezone.now, verbose_name="Data e Hora")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=50, verbose_name="descrição")

    def __str__(self):
        return self.descricao + " - R$ " + str(self.valor)

    class Meta:
        ordering = ["-data_hora", "descricao"]
        verbose_name = "fluxo de caixa"
        verbose_name_plural = "fluxos de caixa"
