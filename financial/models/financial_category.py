from django.db import models


class FinancialCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"


class FinancialTerm(models.Model):
    term = models.CharField(max_length=50)
    category = models.ForeignKey(FinancialCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.term

    class Meta:
        verbose_name = "termo de categoria"
        verbose_name_plural = "termos de categoria"
