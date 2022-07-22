from django.db import models
from financeiro.models import Categoria


class ContasAPagar(models.Model):
    data_hora_cadastro = models.DateTimeField(auto_now_add=True)
    data = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=50, verbose_name="descrição")
    codigo_barras = models.CharField(
        max_length=59, null=True, blank=True, verbose_name="Código de Barras"
    )
    pago = models.BooleanField(default=False)

    def __str__(self):
        return self.descricao + " - R$ " + str(self.valor)

    class Meta:
        ordering = ["data", "descricao"]
        verbose_name = "contas a pagar"
        verbose_name_plural = "contas a pagar"
