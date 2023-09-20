from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("/authentication/login")
