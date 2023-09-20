from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class UpdateUserView(LoginRequiredMixin, View):
    def post(self, request):
        context = {}
        try:
            user = request.user
            if request.POST.get("email") != user.email:
                user.email = request.POST.get("email")
                user.save()
            if request.POST.get("password"):
                if request.POST.get("password") == request.POST.get("password_confirmation"):
                    user.set_password(request.POST.get("password"))
                    user.save()
                else:
                    raise ValidationError
            logout(request)
            context["status"] = 200
        except ValidationError:
            context["status"] = 401
        except:
            context["status"] = 500
        return JsonResponse(context)
