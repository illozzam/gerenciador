from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


class LoginView(View):
	template_name = 'login.html'

	def get(self, request, **kwargs):
		template = 'base.html' if request.user.is_authenticated else 'login.html'
		return render(request, template, {})

	def post(self, request, **kwargs):
		template = 'login.html'
		entrada = authenticate(
			username = request.POST.get('usuario'),
			password = request.POST.get('senha')
		)

		if entrada:
			if entrada.is_active:
				login(request, entrada)
				template = 'base.html'
			else:
				messages.error(request, 'Conta desabilitada :(')
		else:
			messages.error(request, 'Usuário ou senha incorretos. Tente novamente.')

		return render(request, template, {})


class TelaView(LoginRequiredMixin, View):
	tela = 'inicial'

	def get(self, request, **kwargs):
		if self.tela == 'inicial':
			template = 'base.html'

		elif self.tela == 'usuario-perfil':
			template = 'telas/usuario-perfil.html'

		return render(request, template, {})


@method_decorator(csrf_exempt, name = 'dispatch')
class AtualizarUsuarioView(LoginRequiredMixin, View):
	dados = {}
	def post(self, request, **kwargs):
		contexto = {}
		try:
			usuario = request.user
			if request.POST.get('email') != usuario.email:
				usuario.email = request.POST.get('email')
				usuario.save()
			if request.POST.get('senha'):
				if request.POST.get('senha') == request.POST.get('senha2'):
					usuario.set_password(request.POST.get('senha'))
					usuario.save()
				else:
					raise ValidationError
			logout(request)
			contexto['status'] = 200
		except ValidationError:
			contexto['status'] = 401
		except:
			contexto['status'] = 500
		return JsonResponse(contexto)


class LogoutView(LoginRequiredMixin, View):
	def get(self, request, **kwargs):
		logout(request)
		return redirect('/login')
