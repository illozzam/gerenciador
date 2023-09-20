from django.db import models


class BillsToReceive(models.Model):
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=50, verbose_name="descrição")
    received = models.BooleanField(default=False)

    def __str__(self):
        return self.description + " - R$ " + str(self.value)

    class Meta:
        ordering = ["date", "description"]
        verbose_name = "contas a receber"
        verbose_name_plural = "contas a receber"
