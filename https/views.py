from django.http import HttpResponse
from django.views import View

from .models import Chave


class PrincipalView(View):
    def get(self, request, **kwargs):
        if Chave.objects.filter(chave=self.kwargs["chave"]).exists():
            chave = Chave.objects.get(chave=self.kwargs["chave"])
            saida = "{}.{}".format(self.kwargs["chave"], chave.senha)

            chave.verificada = True
            chave.save()
        else:
            saida = "0"
        return HttpResponse(saida)
