from django.db import models


class Config(models.Model):
    variavel = models.CharField(max_length=50, unique=True)
    valor = models.CharField(max_length=400, null=True, blank=True)

    def __str__(self):
        return self.variavel

    class Meta:
        verbose_name = "configuração"
        verbose_name_plural = "configurações"
        ordering = ["variavel"]
