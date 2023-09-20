from django.db import models
from django.utils import timezone
from financial.models import FinancialCategory


class CashFlow(models.Model):
    types_flow = [
        ["E", "Entrada"],
        ["S", "Saída"],
    ]

    category = models.ForeignKey(
        FinancialCategory, on_delete=models.CASCADE, null=True, blank=True
    )
    type = models.CharField(max_length=1, choices=types_flow)
    date = models.DateField(default=timezone.now())
    value = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200, verbose_name="descrição")

    def __str__(self):
        return self.description + " - R$ " + str(self.value)

    class Meta:
        ordering = ["category", "-date", "description"]
        verbose_name = "fluxo de caixa"
        verbose_name_plural = "fluxos de caixa"
