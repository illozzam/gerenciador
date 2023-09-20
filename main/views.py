from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class ScreenView(LoginRequiredMixin, View):
    screen = "inicial"

    def get(self, request):
        if self.screen == "inicial":
            template = "base.html"

        elif self.screen == "user-profile":
            template = "screens/user-profile.html"

        return render(request, template)
