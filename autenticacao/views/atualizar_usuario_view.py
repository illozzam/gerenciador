from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class AtualizarUsuarioView(LoginRequiredMixin, View):
    dados = {}

    def post(self, request):
        contexto = {}
        try:
            usuario = request.user
            if request.POST.get("email") != usuario.email:
                usuario.email = request.POST.get("email")
                usuario.save()
            if request.POST.get("senha"):
                if request.POST.get("senha") == request.POST.get("senha2"):
                    usuario.set_password(request.POST.get("senha"))
                    usuario.save()
                else:
                    raise ValidationError
            logout(request)
            contexto["status"] = 200
        except ValidationError:
            contexto["status"] = 401
        except:
            contexto["status"] = 500
        return JsonResponse(contexto)
