from django.db import models


class Chave(models.Model):
    data_hora = models.DateTimeField(auto_now_add=True)
    chave = models.CharField(max_length=43)
    senha = models.CharField(max_length=43)
    verificada = models.BooleanField(default=False)

    def __str__(self):
        return self.chave
