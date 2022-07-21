from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.views import View


class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        template = "base.html" if request.user.is_authenticated else "login.html"
        return render(request, template, {})

    def post(self, request):
        template = "login.html"
        entrada = authenticate(
            username=request.POST.get("usuario"), password=request.POST.get("senha")
        )

        if entrada:
            if entrada.is_active:
                login(request, entrada)
                template = "base.html"
            else:
                messages.error(request, "Conta desabilitada :(")
        else:
            messages.error(request, "Usuário ou senha incorretos. Tente novamente.")

        return render(request, template)
