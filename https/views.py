from django.http import HttpResponse
from django.views import View
from https.models import HTTPSKey


class HTTPSView(View):
    def get(self, request, **kwargs):
        if HTTPSKey.objects.filter(chave=self.kwargs["key"]).exists():
            key = HTTPSKey.objects.get(chave=self.kwargs["key"])
            output = "{}.{}".format(self.kwargs["key"], key.password)

            key.verificada = True
            key.save()
        else:
            output = "0"
        return HttpResponse(output)
