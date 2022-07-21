from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class TelaView(LoginRequiredMixin, View):
    tela = "inicial"

    def get(self, request):
        if self.tela == "inicial":
            template = "base.html"

        elif self.tela == "usuario-perfil":
            template = "telas/usuario-perfil.html"

        return render(request, template)
