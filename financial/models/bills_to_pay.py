from django.db import models


class BillsToPay(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=50, verbose_name="descrição")
    barcode = models.CharField(
        max_length=59, null=True, blank=True, verbose_name="Código de Barras"
    )
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.description + " - R$ " + str(self.value)

    class Meta:
        ordering = ["date", "description"]
        verbose_name = "contas a pagar"
        verbose_name_plural = "contas a pagar"
