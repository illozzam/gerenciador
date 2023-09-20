from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.views import View


class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        template = "base.html" if request.user.is_authenticated else "login.html"
        return render(request, template, {})

    def post(self, request):
        template = "login.html"
        user_authenticated = authenticate(
            username=request.POST.get("user"), password=request.POST.get("password")
        )

        if user_authenticated:
            if user_authenticated.is_active:
                login(request, user_authenticated)
                template = "base.html"
            else:
                messages.error(request, "Conta desabilitada :(")
        else:
            messages.error(request, "Usuário ou senha incorretos. Tente novamente.")

        return render(request, template)
