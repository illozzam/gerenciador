from django.db import models


class Config(models.Model):
    variable = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=400, null=True, blank=True)

    def __str__(self):
        return self.variable

    class Meta:
        verbose_name = "configuração"
        verbose_name_plural = "configurações"
        ordering = ["variable"]
