from django.db import models
from financeiro.models import Categoria


class ContasAReceber(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    data = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=50, verbose_name="descrição")
    recebido = models.BooleanField(default=False)

    def __str__(self):
        return self.descricao + " - R$ " + str(self.valor)

    class Meta:
        ordering = ["data", "descricao"]
        verbose_name = "contas a receber"
        verbose_name_plural = "contas a receber"
