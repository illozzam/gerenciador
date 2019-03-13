#coding: utf-8
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views import View

import os
from django.conf import settings

from datetime import datetime
import pytz

from .models import *

from django.core.mail import EmailMessage

########################################## CRONS ##############################################################
from django_cron import CronJobBase, Schedule

class EnviarEmails(CronJobBase):
	tempo = 1 #Executar o código do() a cada 1 minuto
	schedule = Schedule(run_every_mins = tempo)
	code = 'principal.views.EnviarEmails'

	def do(self):
		consultorias = Consultoria.objects.filter(
			enviado = False,
			dataHoraEnvio__lte = timezone.now()
		)

		for consultoria in consultorias:
			email = EmailMessage(
				subject = consultoria.empresa,
				body = consultoria.mensagem,
				from_email = '"Julyanna Veras" <administracao@mazzollisistemas.com.br>',
				to = [consultoria.email],
				bcc = ['mazzolli@mazzollisistemas.com.br'],
				reply_to = ['administracao@mazzollisistemas.com.br'],
				headers = {}
			)
			email.content_subtype = 'html'
			email.send()

			consultoria.enviado = True
			consultoria.save()
########################################## /CRONS #############################################################

class LoginView(View):
	dados = {}
	template_name = 'login.html'

	def get(self, request, **kwargs):
		if request.user.is_authenticated():
			self.template_name = 'base.html'
		return render(request, self.template_name, self.dados)

	def post(self, request, **kwargs):
		entrada = authenticate(
			username = request.POST.get('usuario'),
			password = request.POST.get('senha')
		)

		if entrada is not None:
			if entrada.is_active:
				login(request, entrada)
				self.template_name = 'base.html'
			else:
				self.template_name = 'login.html'
				self.dados['aviso'] = 'Conta desabilitada :('
		else:
			self.dados['aviso'] = 'Usuário ou senha incorretos :('

		return render(request, self.template_name, self.dados)

@method_decorator(login_required, name = 'dispatch')
class TelaView(View):
	template_name = 'base.html'
	tela = 'inicial'
	dados = {}

	def get(self, request, **kwargs):
		if self.tela == 'inicial':
			self.template_name = 'base.html'

		#Clientes
		elif self.tela == 'telaAdicionarCliente':
			self.template_name = 'telas/adicionarCliente.html'
			self.dados['estados'] = Estado.objects.all()

		elif self.tela == 'telaBuscarCliente':
			self.template_name = 'telas/buscarCliente.html'

		#Contratos
		elif self.tela == 'telaAdicionarContrato':
			self.template_name = 'telas/adicionarContrato.html'
			self.dados['clientes'] = Cliente.objects.all()
			self.dados['servicos'] = Servico.objects.all()
			self.dados['modulos'] = Modulo.objects.all()

		elif self.tela == 'telaBuscarContrato':
			self.template_name = 'telas/buscarContrato.html'
			self.dados['clientes'] = Cliente.objects.all()

		#Consultorias
		elif self.tela == 'telaAdicionarConsultoria':
			self.dados['ramosAtividade'] = RamoConsultoria.objects.all()
			self.dados['consultoriasHoje'] = Consultoria.objects.filter(
				usuario = request.user.usuario_set.first(),
				dataHoraEnvio__contains = timezone.now().date()
			).count()
			self.template_name = 'telas/adicionarConsultoria.html'

		elif self.tela == 'telaCriarConsultoria':
			self.dados['ramosAtividade'] = RamoConsultoria.objects.all()
			self.dados['consultoriasHoje'] = Consultoria.objects.filter(
				usuario = request.user.usuario_set.first(),
				dataHoraEnvio__contains = timezone.now().date()
			).count()
			self.template_name = 'telas/criarConsultoria.html'

		elif self.tela == 'telaBuscarConsultoria':
			self.template_name = 'telas/buscarConsultorias.html'

		#Mensagens
		elif self.tela == 'telaMensagensEntrada':
			self.template_name = 'telas/mensagensEntrada.html'
			self.dados['mensagens'] = Mensagem.objects.filter(destinatario = request.user.usuario_set.first()).order_by('-dataHoraEnvio')

		elif self.tela == 'telaNovaMensagem':
			self.template_name = 'telas/novaMensagem.html'
			self.dados['usuarios'] = Usuario.objects.all()

		elif self.tela == 'telaMensagem':
			self.dados['mensagem'] = Mensagem.objects.get(id = int(self.kwargs['idMensagem']))

			#Se o usuário não tiver permissão para visualizar a mensagem, redireciona para a tela principal
			if self.dados['mensagem'].remetente == request.user.usuario_set.first() or self.dados['mensagem'].destinatario == request.user.usuario_set.first():
				if self.dados['mensagem'].destinatario == request.user.usuario_set.first():
					self.dados['mensagem'].ler()
				self.template_name = 'telas/mensagem.html'
			else:
				return redirect('/')

		elif self.tela == 'telaMensagensEnviadas':
			self.dados['mensagens'] = Mensagem.objects.filter(
				remetente = request.user.usuario_set.first()
			).order_by('-dataHoraEnvio')
			self.template_name = 'telas/mensagensEnviadas.html'

		#Agenda de tarefas
		elif self.tela == 'telaTarefas':
			self.template_name = 'telas/tarefas.html'
			self.dados['tarefas'] = Tarefa.objects.filter(
				usuarioDestino = request.user.usuario_set.first(),
				status = 'A'
			).order_by('prioridade', '-data', 'titulo')

		#Financeiro
		elif self.tela == 'telaContasAReceber':
			self.template_name = 'telas/contasAReceber.html'
			self.dados['contas'] = ContasAReceber.objects.all()

		elif self.tela == 'telaContasAPagar':
			self.template_name = 'telas/contasAPagar.html'
			self.dados['contas'] = ContasAPagar.objects.all()

		elif self.tela == 'telaTesouraria':
			self.template_name = 'telas/tesouraria.html'

		elif self.tela == 'telaPerfilUsuario':
			self.template_name = 'telas/perfilusuario.html'

		return render(request, self.template_name, self.dados)

#Mensagens
@method_decorator(login_required, name = 'dispatch')
class VerificarMensagensView(View):
	dados = {}
	def get(self, request, **kwargs):
		self.dados['mensagens'] = list(
			Mensagem.objects.filter(
				destinatario = request.user.usuario_set.first(),
				lida = False
			).order_by('-dataHoraEnvio').values(
				'id',
				'remetente__usuario__first_name',
				'remetente__usuario__last_name',
				'remetente__facebook',
				'dataHoraEnvio',
				'assunto'
			)
		)
		return JsonResponse(self.dados, safe = False)

@method_decorator(login_required, name = 'dispatch')
class ApagarMensagemView(View):
	def get(self, request, **kwargs):
		pass

@method_decorator([login_required, csrf_exempt], name = 'dispatch')
class EnviarMensagemView(View):
	dados = {}

	def post(self, request, **kwargs):
		try:
			Mensagem.objects.create(
				remetente = request.user.usuario_set.first(),
				destinatario = Usuario.objects.get(id = int(request.POST.get('destinatario'))),
				assunto = request.POST.get('assunto'),
				texto = request.POST.get('texto')
			)
			self.dados['status'] = 1
		except:
			self.dados['status'] = 0
		return JsonResponse(self.dados, safe = False)

#Agenda de Tarefas
@method_decorator([login_required, csrf_exempt], name = 'dispatch')
class AdicionarTarefaView(View):
	'''
	Retorno:
	0 - Erro genérico
	1 - Sucesso
	2 - Usuário não encontrado
	'''
	dados = {}
	def post(self, request, **kwargs):
		try:
			#Verifica se o usuário adicionou a tarefa para si mesmo ou para outro
			titulo = request.POST.get('titulo')
			if titulo[0] == '@':
				#Outro usuário
				titulo = titulo[1:].split(':')
				if User.objects.filter(username = titulo[0].replace(' ', '')).exists():
					usuarioDestino = User.objects.get(username = titulo[0].replace(' ', '')).usuario_set.first()
					if titulo[1][0] == ' ':
						titulo = titulo[1][1:]
					else:
						titulo = titulo[1]
				else:
					return JsonResponse({'status': 2}, safe = False)
			else:
				#Si mesmo
				usuarioDestino = request.user.usuario_set.first()
				titulo = request.POST.get('titulo')

			tarefa = Tarefa.objects.create(
				usuarioOrigem = request.user.usuario_set.first(),
				usuarioDestino = usuarioDestino,
				titulo = titulo,
				prioridade = request.POST.get('prioridade'),
				descricao = request.POST.get('descricao')
			)

			if request.POST.get('data'):
				tarefa.data = datetime.strptime(request.POST.get('data'), '%d/%m/%Y')
				tarefa.save()

			self.dados['status'] = 1
			self.dados['tarefas'] = list(
				Tarefa.objects.filter(
					usuarioDestino = request.user.usuario_set.first(),
					status = 'A'
				).order_by('prioridade', '-data', 'titulo').values(
					'id',
					'data',
					'titulo',
					'prioridade',
					'descricao',
					'status'
				)
			)
		except:
			self.dados['status'] = 0
		return JsonResponse(self.dados, safe = False)

@method_decorator(login_required, name = 'dispatch')
class ExcluirTarefaView(View):
	'''
	Retorna:
	0 - Erro genérico
	1 - Sucesso
	2 - Não informado um idTarefa
	3 - Tarefa não pertence ao usuário
	'''
	dados = {}
	def get(self, request, **kwargs):
		try:
			if 'idTarefa' in request.GET:
				tarefa = Tarefa.objects.get(id = int(request.GET.get('idTarefa')))
				if tarefa.usuarioDestino == request.user.usuario_set.first():
					Tarefa.objects.get(id = int(request.GET.get('idTarefa'))).delete()
					self.dados['tarefas'] = list(
						Tarefa.objects.filter(
							usuarioDestino = request.user.usuario_set.first(),
							status = 'A'
						).order_by('prioridade', '-data', 'titulo').values(
							'id',
							'data',
							'titulo',
							'prioridade',
							'descricao',
							'status'
						)
					)
					self.dados['status'] = 1
				else:
					self.dados['status'] = 3
			else:
				self.dados['status'] = 2
		except:
			self.dados['status'] = 0
		return JsonResponse(self.dados, safe = False)

@method_decorator(login_required, name = 'dispatch')
class ConcluirTarefaView(View):
	'''
	Retorna:
	0 - Erro genérico
	1 - Sucesso
	2 - Não foi informado um idTarefa
	3 - A tarefa não pertence ao usuário
	'''
	dados = {}
	def get(self, request, **kwargs):
		try:
			if 'idTarefa' in request.GET:
				tarefa = Tarefa.objects.get(id = int(request.GET.get('idTarefa')))
				if tarefa.usuarioDestino == request.user.usuario_set.first():
					tarefa.status = 'C'
					tarefa.save()
					self.dados['tarefas'] = list(
						Tarefa.objects.filter(
							usuarioDestino = request.user.usuario_set.first(),
							status = 'A'
						).order_by('prioridade', '-data', 'titulo').values(
							'id',
							'data',
							'titulo',
							'prioridade',
							'descricao',
							'status'
						)
					)
					self.dados['status'] = 1
				else:
					self.dados['status'] = 3
			else:
				self.dados['status'] = 2
		except:
			self.dados['status'] = 0
		return JsonResponse(self.dados, safe = True)

@method_decorator(login_required, name = 'dispatch')
class AlterarPrioridadeTarefaView(View):
	'''
	Formato: /tarefas/prioridade/alterar/?idTarefa=XXX&prioridade=1
	Retorna:
	0 - Erro genérico
	1 - Sucesso
	2 - Não informado um idTarefa ou prioridade
	3 - A tarefa não pertence ao usuário
	'''

	dados = {}
	def get(self, request, **kwargs):
		try:
			if 'idTarefa' in request.GET and 'prioridade' in request.GET:
				tarefa = Tarefa.objects.get(id = int(request.GET.get('idTarefa')))
				if tarefa.usuarioDestino == request.user.usuario_set.first():
					tarefa.prioridade = request.GET.get('prioridade')
					tarefa.save()

					self.dados['tarefas'] = list(
						Tarefa.objects.filter(
							usuarioDestino = request.user.usuario_set.first(),
							status = 'A'
						).order_by('prioridade', '-data', 'titulo').values(
							'id',
							'data',
							'titulo',
							'prioridade',
							'descricao',
							'status'
						)
					)
					self.dados['status'] = 1
				else:
					self.dados['status'] = 3
			else:
				self.dados['status'] = 2
		except:
			self.dados['status'] = 0
		return JsonResponse(self.dados, safe = False)

@method_decorator(login_required, name = 'dispatch')
class DadosTarefaView(View):
	'''
	Retorna:
	0 - Erro genérico
	1 - Sucesso
	2 - Tarefa não pertence ao usuário
	'''
	dados = {}
	def get(self, request, **kwargs):
		try:
			if Tarefa.objects.get(id = int(request.GET.get('idTarefa'))).usuarioDestino == request.user.usuario_set.first():
				self.dados['tarefa'] = list(
					Tarefa.objects.filter(
						id = int(request.GET.get('idTarefa'))
					).order_by('prioridade', '-data', 'titulo').values(
						'id',
						'data',
						'titulo',
						'prioridade',
						'descricao'
					)
				)
			self.dados['status'] = 1
		except:
			self.dados['status'] = 0
		return JsonResponse(self.dados, safe = False)

#Clientes
@method_decorator([login_required, csrf_exempt], name = 'dispatch')
class CadastrarClienteView(View):
	def post(self, request, **kwargs):
		try:
			cliente = Cliente.objects.create(
				tipo = request.POST.get('tipo'),
				nome = request.POST.get('nome'),
				sobrenome = request.POST.get('sobrenome'),
				cpf = request.POST.get('cpf'),
				razaoSocial = request.POST.get('razaoSocial'),
				responsavel = request.POST.get('responsavel'),
				cnpj = request.POST.get('cnpj'),
				email = request.POST.get('email'),
				telefone = request.POST.get('telefone'),
				cep = request.POST.get('cep'),
				endereco = request.POST.get('endereco'),
				numero = request.POST.get('numero'),
				complemento = request.POST.get('complemento'),
				bairro = request.POST.get('bairro'),
				cidade = Cidade.objects.get(id = int(request.POST.get('cidade')))
			)

			saida = {
				'status': 1,
			}
		except Exception as erro:
			saida = {
				'erro': erro,
				'status': 0,
			}
		return JsonResponse(saida)

@method_decorator(login_required, name = 'dispatch')
class ExcluirClienteView(View):
	def get(self, request, **kwargs):
		saida = {}
		try:
			Cliente.objects.get(id = int(self.kwargs['idCliente'])).delete()
			saida['status'] = 1
		except:
			saida['status'] = 0
		return JsonResponse(saida)

@method_decorator(login_required, name = 'dispatch')
class BuscarClienteView(View):
	def get(self, request, **kwargs):
		termo = request.GET.get('cliente')

		if termo[0].isdigit():
			resultado = list(
				Cliente.objects.filter(cpf__contains = termo).values('tipo', 'id', 'nome', 'sobrenome', 'telefone', 'email')
			) + list(
				Cliente.objects.filter(cnpj__contains = termo).values('tipo', 'id', 'razaoSocial', 'responsavel', 'telefone', 'email')
			)
		else:
			resultado = list(
				Cliente.objects.filter(nome__icontains = termo).values('tipo', 'id', 'nome', 'sobrenome', 'telefone', 'email')
			) + list(
				Cliente.objects.filter(sobrenome__icontains = termo).values('tipo', 'id', 'nome', 'sobrenome', 'telefone', 'email')
			) + list(
				Cliente.objects.filter(razaoSocial__icontains = termo).values('tipo', 'id', 'razaoSocial', 'responsavel', 'telefone', 'email')
			) + list(
				Cliente.objects.filter(responsavel__icontains = termo).values('tipo', 'id', 'razaoSocial', 'responsavel', 'telefone', 'email')
			)

		return JsonResponse(resultado, safe = False)

@method_decorator(login_required, name = 'dispatch')
class DadosClienteView(View):
	'''
	Retorna todos os dados do cliente em formato JSON
	'''
	dados = {}
	def get(self, request, **kwargs):
		self.dados['cliente'] = list(
			Cliente.objects.filter(
				id = int(self.kwargs['idCliente'])
			).values(
				'tipo',
				'nome',
				'sobrenome',
				'cpf',
				'razaoSocial',
				'responsavel',
				'cnpj',
				'email',
				'telefone',
				'cep',
				'endereco',
				'numero',
				'complemento',
				'bairro',
				'cidade__nome',
				'cidade__estado__uf',
			)
		)

		self.dados['contratos'] = list(
			Contrato.objects.filter(
				cliente = Cliente.objects.get(id = int(self.kwargs['idCliente']))
			).values(
				'dataHoraInclusao',
				'numero',
				'servico__nome',
				'valor',
				'qtdadeParcelas',
				'diaPagamento',
				'vigencia',
			)
		)
		return JsonResponse(self.dados, safe = False)

@method_decorator(login_required, name = 'dispatch')
class ListarCidadesView(View):
	def get(self, request, **kwargs):
		return JsonResponse(
			list(
				Cidade.objects.filter(
					estado = Estado.objects.get(
						uf = request.GET.get('estado')
					)
				).values('id', 'nome')
			),
			safe = False
		)

@method_decorator([login_required, csrf_exempt], name = 'dispatch')
class AtualizarUsuarioView(View):
	dados = {}
	def post(self, request, **kwargs):
		try:
			self.dados['status'] = 200
			usuario = request.user.usuario_set.first()
			if request.POST.get('email') != usuario.usuario.email:
				usuario.usuario.email = request.POST.get('email')
				usuario.usuario.save()
			if request.POST.get('senha'):
				if request.POST.get('senha') == request.POST.get('senha2'):
					usuario.usuario.set_password(request.POST.get('senha'))
					usuario.usuario.save()
				else:
					self.dados['status'] = 400
			if usuario.telefone != request.POST.get('telefone'):
				usuario.telefone = request.POST.get('telefone')
				usuario.save()
			if usuario.facebook != request.POST.get('facebook'):
				usuario.facebook = request.POST.get('facebook')
				usuario.save()
		except:
			self.dados['status'] = 500
		return JsonResponse(self.dados)

#Contratos
@method_decorator(login_required, name = 'dispatch')
class ProximoNumeroContratoView(View):
	'''
	Gera a numeração para o próximo contrato. Entrada por GET e retorno em JSON
	'''
	dados = {}
	def get(self, request, **kwargs):
		if Contrato.objects.all():
			ultimoNumero = Contrato.objects.all().last().numero
		else:
			ultimoNumero = '{}/{}'.format(str(timezone.now().year), '000')
		ultimoNumero = ultimoNumero.split('/')
		if str(timezone.now().year) == ultimoNumero[0]:
			self.dados['numero'] = '{}/{:0>3}'.format(str(timezone.now().year), str(int(ultimoNumero[1]) + 1))
		else:
			self.dados['numero'] = '{}/{}'.format(str(timezone.now().year), '001')
		return JsonResponse(self.dados, safe = False)

@method_decorator([csrf_exempt, login_required], name = 'dispatch')
class CadastrarContratoView(View):
	dados = {}
	def post(self, request, **kwargs):
		try:
			if request.POST.get('vigencia') == '':
				vigencia = 0
			else:
				vigencia = int(request.POST.get('vigencia'))

			contrato = Contrato.objects.create(
				numero = request.POST.get('numero'),
				cliente = Cliente.objects.get(id = int(request.POST.get('cliente'))),
				servico = Servico.objects.get(id = int(request.POST.get('servico'))),
				vigencia = vigencia,
				valor = float(request.POST.get('valor').replace(',', '.')),
				qtdadeParcelas = int(request.POST.get('parcelas')),
				diaPagamento = int(request.POST.get('diaPagamento')),
				observacoes = request.POST.get('observacoes')
			)

			for modulo in request.POST.getlist('modulos[]'):
				contrato.modulos.add(Modulo.objects.get(id = int(modulo)))
				contrato.save()

			self.dados['status'] = 1
		except:
			self.dados['status'] = 0
		return JsonResponse(self.dados, safe = False)

@method_decorator(login_required, name = 'dispatch')
class BuscarContratoView(View):
	def get(self, request, **kwargs):
		if 'cliente' in request.GET:
			cliente = Cliente.objects.get(id = int(request.GET.get('cliente')))
		else:
			cliente = None
		if 'numero' in request.GET:
			numero = request.GET.get('numero').replace('-', '/')
		else:
			numero = None

		if numero and cliente:
			return JsonResponse(
				list(
					Contrato.objects.filter(
						numero = numero,
						cliente = cliente
					).values(
						'id',
						'numero',
						'cliente__tipo',
						'cliente__nome',
						'cliente__sobrenome',
						'cliente__razaoSocial',
						'cliente__cpf',
						'cliente__cnpj',
						'cliente__email',
						'servico__nome',
						'valor'
					)
				), safe = False
			)
		elif numero and not cliente:
			return JsonResponse(
				list(
					Contrato.objects.filter(
						numero = numero
					).values(
						'id',
						'numero',
						'cliente__tipo',
						'cliente__nome',
						'cliente__sobrenome',
						'cliente__razaoSocial',
						'cliente__cpf',
						'cliente__cnpj',
						'cliente__email',
						'servico__nome',
						'valor'
					)
				), safe = False
			)
		elif not numero and cliente:
			return JsonResponse(
				list(
					Contrato.objects.filter(
						cliente = cliente
					).values(
						'id',
						'numero',
						'cliente__tipo',
						'cliente__nome',
						'cliente__sobrenome',
						'cliente__razaoSocial',
						'cliente__cpf',
						'cliente__cnpj',
						'cliente__email',
						'servico__nome',
						'valor'
					)
				), safe = False
			)

@method_decorator(login_required, name = 'dispatch')
class DetalhesContratoView(View):
	def get(self, request, **kwargs):
		return JsonResponse(
			list(
				Contrato.objects.filter(
					id = int(request.GET.get('idContrato'))
				).values(
					'numero',
					'cliente__tipo',
					'cliente__nome',
					'cliente__sobrenome',
					'cliente__razaoSocial',
					'cliente__responsavel',
					'cliente__cnpj',
					'cliente__cpf',
					'servico__nome',
					'modulos__nome',
					'valor',
					'qtdadeParcelas',
					'dataHoraInclusao',
					'diaPagamento',
					'vigencia',
					'observacoes'
				)
			), safe = False
		)

#Financeiro
@method_decorator([login_required, csrf_exempt], name = 'dispatch')
class CadastrarContasAPagarView(View):
	dados = {}
	def post(self, request, **kwargs):
		try:
			#Formata o código de barras
			if 'codigoBarras' in request.POST:
				codigoBarras = request.POST.get('codigoBarras').replace(' ', '').replace('.', '').replace('-', '')
				codigoBarras = codigoBarras.replace(' ', '').replace('.', '').replace('-', '')
				for digito in range(4, len(codigoBarras) + 12, 5):
					codigoBarras = codigoBarras[0:digito] + ' ' + codigoBarras[digito:]
				if len(codigoBarras) == 60: codigoBarras = codigoBarras[:-1]
			else:
				codigoBarras = ''

			conta = ContasAPagar.objects.create(
				usuario = request.user.usuario_set.first(),
				data = request.POST.get('data'),
				valor = float(request.POST.get('valor').replace(',', '.')),
				descricao = request.POST.get('descricao'),
				codigoBarras = codigoBarras
			)

			self.dados['status'] = 1
			self.dados['conta'] = {
				'id': conta.id,
				'data': conta.data,
				'valor': float(conta.valor),
				'descricao': conta.descricao,
				'codigoBarras': conta.codigoBarras,
			}
		except:
			self.dados['status'] = 0
		return JsonResponse(self.dados, safe = False)

@method_decorator([login_required, csrf_exempt], name = 'dispatch')
class EditarContasAPagarView(View):
	'''
	Recebe: id, data
	Retorna: status
	'''
	dados = {}
	def post(self, request, **kwargs):
		try:
			conta = ContasAPagar.objects.get(id = int(request.POST.get('id')))
			conta.data = request.POST.get('data')
			conta.save()
			self.dados['status'] = 1
		except:
			self.dados['status'] = 0
		return JsonResponse(self.dados, safe = False)

@method_decorator(login_required, name = 'dispatch')
class ExcluirContasAPagarView(View):
	dados = {}
	def get(self, request, **kwargs):
		try:
			conta = ContasAPagar.objects.get(id = int(request.GET.get('idConta')))
			conta.delete()
			self.dados['status'] = 1
		except:
			self.dados['status'] = 0
		return JsonResponse(self.dados, safe = False)

@method_decorator(login_required, name = 'dispatch')
class ReportarPagamentoView(View):
	dados = {}
	def get(self, request, **kwargs):
		try:
			conta = ContasAPagar.objects.get(id = int(request.GET.get('idConta')))
			conta.pago = True
			conta.save()

			Tesouraria.objects.create(
				tipo = 'S',
				descricao = conta.descricao,
				valor = conta.valor
			)

			self.dados['status'] = 1
		except:
			self.dados['status'] = 0
		return JsonResponse(self.dados, safe = False)

@method_decorator([login_required, csrf_exempt], name = 'dispatch')
class CadastrarContasAReceberView(View):
	dados = {}
	def post(self, request, **kwargs):
		try:
			conta = ContasAReceber.objects.create(
				data = request.POST.get('data'),
				valor = float(request.POST.get('valor').replace(',', '.')),
				descricao = request.POST.get('descricao')
			)

			self.dados['status'] = 1
			self.dados['conta'] = {
				'id': conta.id,
				'data': conta.data,
				'valor': float(conta.valor),
				'descricao': conta.descricao,
			}
		except:
			self.dados['status'] = 0
		return JsonResponse(self.dados, safe = False)

@method_decorator([login_required, csrf_exempt], name = 'dispatch')
class EditarContasAReceberView(View):
	'''
	Recebe: id, data
	Retorna: status
	'''
	dados = {}
	def post(self, request, **kwargs):
		try:
			conta = ContasAReceber.objects.get(id = int(request.POST.get('id')))
			conta.data = request.POST.get('data')
			conta.save()
			self.dados['status'] = 1
		except:
			self.dados['status'] = 0
		return JsonResponse(self.dados, safe = False)

@method_decorator(login_required, name = 'dispatch')
class ExcluirContasAReceberView(View):
	dados = {}
	def get(self, request, **kwargs):
		try:
			conta = ContasAReceber.objects.get(id = int(request.GET.get('idConta')))
			conta.delete()
			self.dados['status'] = 1
		except:
			self.dados['status'] = 0
		return JsonResponse(self.dados, safe = False)

@method_decorator([csrf_exempt, login_required], name = 'dispatch')
class ReportarRecebimentoView(View):
	dados = {}
	def post(self, request, **kwargs):
		try:
			boleto = request.POST.get('boleto')
			conta = ContasAReceber.objects.get(id = int(request.POST.get('idConta')))
			conta.recebido = True
			conta.save()

			Tesouraria.objects.create(
				tipo = 'E',
				descricao = conta.descricao,
				valor = conta.valor
			)

			if boleto == 'true':
				taxaBoleto = float(conta.valor) * float(Config.objects.get(variavel = 'taxaBoleto').valor)
				if taxaBoleto < 2.5:
					taxaBoleto = 2.5
				Tesouraria.objects.create(
					tipo = 'S',
					descricao = 'Taxas boleto - %s' % conta.descricao,
					valor = float(taxaBoleto)
				)

			self.dados['status'] = 1
		except:
			self.dados['status'] = 0
		return JsonResponse(self.dados, safe = False)

@method_decorator([login_required, csrf_exempt], name = 'dispatch')
class CadastrarTesourariaView(View):
	dados = {}
	def post(self, request, **kwargs):
		try:
			Tesouraria.objects.create(
				tipo = request.POST.get('tipo'),
				dataHora = datetime.strptime(request.POST.get('dataHora'), '%d/%m/%Y %H:%M'),
				valor = float(request.POST.get('valor').replace(',', '.')),
				descricao = request.POST.get('descricao')
			)
			self.dados['status'] = 1
		except:
			self.dados['status'] = 0
		return JsonResponse(self.dados, safe = False)

@method_decorator(login_required, name = 'dispatch')
class PesquisarTesourariaView(View):
	dados = {}
	def get(self, request, **kwargs):
		#try:
		d1 = datetime.strptime(request.GET.get('dataInicial'), '%Y-%m-%d')
		d2 = datetime.strptime(request.GET.get('dataFinal'), '%Y-%m-%d')
		dataInicial = datetime(d1.year, d1.month, d1.day, 0, 0)
		dataFinal = datetime(d2.year, d2.month, d2.day, 23, 59)

		self.dados['saldoAnterior'] = 0
		for movimentacao in Tesouraria.objects.filter(dataHora__lte = dataInicial):
			if movimentacao.tipo == 'E':
				self.dados['saldoAnterior'] += float(movimentacao.valor)
			else:
				self.dados['saldoAnterior'] -= float(movimentacao.valor)

		self.dados['movimentacoes'] = list(
			Tesouraria.objects.filter(
				dataHora__gte = dataInicial,
				dataHora__lte = dataFinal
			).values(
				'tipo',
				'dataHora',
				'valor',
				'descricao'
			)
		)
		self.dados['status'] = 1
		#except:
		#	self.dados['status'] = 0
		return JsonResponse(self.dados, safe = False)


#Consultorias
@method_decorator([csrf_exempt, login_required], name = 'dispatch')
class CadastrarRamoAtividadeView(View):
	'''
	Cadastra um novo ramo de atividade. Se sucesso, retorna o id e o nome do novo ramo.
	'''
	dados = {}
	def post(self, request, **kwargs):
		try:
			ramoAtividade = RamoConsultoria.objects.create(nome = request.POST.get('nome'))
			self.dados['status'] = 1
			self.dados['ramo'] = {
				'id': ramoAtividade.id,
				'nome': ramoAtividade.nome,
			}
		except:
			self.dados['status'] = 0
		return JsonResponse(self.dados)

@method_decorator([csrf_exempt, login_required], name = 'dispatch')
class CadastrarConsultoriaView(View):
	dados = {}
	def post(self, request, **kwargs):
		try:
			if request.POST.get('ramoAtividade') == '0':
				ramoAtividade = None
			else:
				ramoAtividade = RamoConsultoria.objects.get(id = int(request.POST.get('ramoAtividade')))

			consultoria = Consultoria.objects.create(
				usuario = request.user.usuario_set.first(),
				ramoAtividade = ramoAtividade,
				empresa = request.POST.get('empresa'),
				dominio = request.POST.get('dominio'),
				email = request.POST.get('email'),
				mensagem = request.POST.get('mensagem'),
				observacoes = request.POST.get('observacoes')
			)

			self.dados['status'] = 1
			self.dados['consultoriasHoje'] = Consultoria.objects.filter(
				usuario = request.user.usuario_set.first(),
				dataHoraEnvio__contains = timezone.now().date()
			).count()
		except:
			self.dados['status'] = 0
		return JsonResponse(self.dados)

@method_decorator(login_required, name = 'dispatch')
class BuscarConsultoriaView(View):
	dados = {}
	def get(self, request, **kwargs):
		try:
			if request.GET.get('dataEnvio') == '':
				self.dados['consultorias'] = list(
					Consultoria.objects.filter(empresa__icontains = request.GET.get('empresa')).values(
						'id',
						'empresa',
						'dominio',
						'email',
						'dataHoraInclusao',
						'dataHoraEnvio'
					)
				)
			elif request.GET.get('empresa') == '':
				self.dados['consultorias'] = list(
					Consultoria.objects.filter(dataHoraEnvio__contains = datetime.strptime(
						request.GET.get('dataEnvio'),
						'%d/%m/%Y'
					).date()).values(
						'id',
						'empresa',
						'dominio',
						'email',
						'dataHoraInclusao',
						'dataHoraEnvio'
					)
				)
			else:
				self.dados['consultorias'] = list(
					Consultoria.objects.filter(dataHoraEnvio__contains = datetime.strptime(
						request.GET.get('dataEnvio'),
						'%d/%m/%Y'
					).date())
					.filter(
						empresa__icontains = request.GET.get('empresa')
					).values(
						'id',
						'empresa',
						'dominio',
						'email',
						'dataHoraInclusao',
						'dataHoraEnvio'
					)
				)
			self.dados['status'] = 1
		except:
			self.dados['status'] = 0
		return JsonResponse(self.dados, safe = False)

@method_decorator(login_required, name = 'dispatch')
class DadosConsultoriaView(View):
	dados = {}
	def get(self, request, **kwargs):
		self.dados['status'] = 1
		self.dados['consultoria'] = list(
			Consultoria.objects.filter(id = int(self.kwargs['consultoria_id'])).values(
				'id',
				'usuario__usuario__username',
				'dataHoraInclusao',
				'ramoAtividade',
				'empresa',
				'dominio',
				'email',
				'mensagem',
				'observacoes'
			)
		)
		return JsonResponse(self.dados)

@method_decorator([login_required, csrf_exempt], name = 'dispatch')
class CriarConsultoriaView(View):
	dados = {}
	def post(self, request, **kwargs):
		if request.POST.get('opcao') == 'comSite':
			texto = '''
				Olá!<br><br>
				Meu nome é Julyanna e trabalho na área do Marketing Digital. Em poucas palavras, meu trabalho é garantir que a pessoa que acessa o seu site tenha uma experiência tão boa que, se ela não se tornar seu cliente, ficará com aquela sensação de que falta algo em sua vida! Hoje, estamos fazendo algumas consultorias gratuitas e o seu negócio foi contemplado.<br><br>
				[PRINT DO SITE]
			'''.format(request.POST.get('printSite'))
		elif request.POST.get('opcao') == 'consultoriaSEO':
			texto = '''
				Olá!<br><br>
				Meu nome é Julyanna e conheci a empresa de vocês através do Facebook. Trabalho com Marketing Digital. Meu trabalho é planejar cuidadosamente a experiência do seu cliente com o contato da sua marca desde o momento em que ele está "buscando o que ou onde comprar" até realizar a compra efetivamente.<br><br>
				Levando em conta que, segundo o IBGE (dados de 2015), 80% das vendas de uma empresa iniciam com pesquisas na Internet, é fundamental que o seu cliente tenha a melhor experiência possível quando encontrar vocês. Esse primeiro encontro pode ocorrer através do Facebook e se sua página estiver de acordo com os princípios do Marketing Digital esse visitante pode se tornar seu cliente mais facilmente.<br><br>
				Sendo assim, analisamos a página da sua empresa e vamos lhe dar algumas dicas de como melhor se posicionar nesta ferramenta.<br><br>
				O Facebook, ao ser utilizado por empresas, tem a finalidade de estabelecer laços e contato com os clientes de maneira direta e frequente mas, para isso, é necessário que a página seja constantemente atualizada e mostrando ao seu cliente que você está disponível para ele. Seu cliente precisa ser lembrado que um dia Curtiu a sua página e de que você existe!
			'''

		if request.POST.get('opcao') == 'comSite':
			if 'semHTTPS' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Atualmente, um dos critérios que o Google considera para fazer o ranqueamento dos sites é a ativação do protocolo de segurança HTTPS. Esse protocolo criptografa as informações entre o navegador do seu cliente e o servidor onde o seu site está hospedado, tornando a conexão mais segura contra pessoas mal intencionadas que possam roubar informações. Mas, mais do que isso, as novas versões do Google Chrome e do Firefox já estão mostrando a mensagem "Não Seguro" para sites que não possuem esse protocolo ativado e o seu é um deles. É de extrema importância que você preste atenção nisso!
				'''

		if request.POST.get('opcao') == 'comSite':
			if 'naoResponsivo' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Um ponto preocupante é que o seu site não é responsivo, ou seja, compatível com celulares e tablets. Faça o teste: Pegue um celular e tente acessar o seu site por ele. Consegue ler o que está escrito? Hoje, com toda a Internet migrando para dispositivos móveis, ter um site que não se adapta ao tamanho da tela do dispositivo é garantir que a maior parte das pessoas não terão uma boa impressão ao acessar sua página. Além disso, os sites que não são responsivos perdem posições no ranqueamento do Google. Na Mazzolli Sistemas não cobramos nenhum adicional por essa tecnologia.
				'''
			if 'naoPossuiUrlsAmigaveis' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Uma coisa muito importante em um site hoje, por causa da velocidade e praticidade que a Internet proporciona, é ele ter URLs amigáveis. Se eu sou seu possível cliente e quero informações da página de sem a necessidade de passar pela página inicial para isso, teria que digitar na barra de endereço: %s". E se, ao invés disso, vocês tivessem a mesma página disponível no endereço: "%s/%s"? Qualquer coisa que deixe o acesso mais prático é importante!''' % (
					request.POST.get('urlPaginaAvulsa').encode('utf-8'),
					request.POST.get('dominio').encode('utf-8'),
					request.POST.get('nomePaginaAvulsa').encode('utf-8').lower()
				)
			if 'semAnalytics' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Identificamos que o seu site não está conectado ao Analytics do Google, esta é uma ferramenta de grande auxílio para os administradores porque é ela que mede a quantidade de acessos que vocês tem em sua página, qual o comportamento do usuário ao acessá-la e o perfil das pessoas que entram no seu site.
				'''
			else:
				texto += '''<br><br>
				Identificamos que o seu site está conectado ao Analytics do Google, o que é ótimo pois esta é uma ferramenta de grande auxílio para os administradores porque é ela que mede a quantidade de acessos que vocês tem em sua página, qual o comportamento do usuário ao acessá-la e o perfil das pessoas que entram no seu site.
				'''
			if 'margemMuitoGrande' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Falando sobre o layout do seu site, este não aproveita todo o "espaço em branco" da página (que são as áreas laterais onde não há texto e imagens). Desta forma os textos ficam muito agrupados, a fonte do mesmo fica pequena e dificulta a leitura.
				'''
			if 'siteSemLogotipo' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Uma das coisas responsável pela identidade visual de uma empresa - ou de um profissional particular - é o logotipo dela. O logotipo profissionaliza a atividade e auxilia na divulgação do serviço prestado ou produtos vendidos pela empresa ou profissional. Hoje, seu site não possui logotipo e desta maneira, sua identidade visual fica comprometida, fazendo com que seu site perca personalidade.
				'''
			if 'imagensBaixaDefinicao' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Seu site apresenta algumas imagens em baixa definição. Uma imagem em baixa definição apresenta o aspecto pixelado que compromete a experiência do cliente no seu site. Sugerimos que essas imagens sejam substituídas por outras na resolução correta e que elas sejam compactadas para não atrapalhar a velocidade de carregamento do site, fazendo assim com que vocês percam posicionamento no Google.
				'''
			if 'semMapaGoogle' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Hoje, com as vantagens que o Google oferece - principalmente no que tange a localização, pessoas e conteúdo - ele é uma ferramenta de uso obrigatório e que facilita muito a vida de empresas e seus clientes. Neste contexto o Mapa do Google serve ao seu propósito e está presente em diversos sites. No entanto, para o visitante, quanto mais rápido as informações aparecerem pra ele melhor será, mais rápido ele atingirá o seu objetivo e mais satisfeito ficará. Assim, o Mapa do Google deveria aparecer diretamente na página (aconselhamos que esteja na de Contato) e não estar em um link externo ouaté mesmo em uma imagem, pelos benefícios que ele gera ao visitante.
				'''
			if 'emailNaoPersonalizado' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Ter um e-mail nos servidores do %s passa uma impressão amadora que não condiz com o objetivo do site. O ideal sempre é ter um e-mail como, no caso de vocês, "contato@%s". Esse tipo de configuração é bastante simples e faz toda a diferença.
				''' % (request.POST.get('servidorAtualEmail').encode('utf-8'), request.POST.get('dominio').encode('utf-8'))
			if 'semFormularioContato' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Apesar do telefone e endereço estarem visíveis, não há formulário de contato no site. Isso é um problema para muitas pessoas que já estão acostumadas a entrar em contato com empresas através de seus sites, muito útil quando você não quer fazer uma ligação ou quando não pode fazê-la. Então por que não facilitar o contato dessas pessoas disponibilizando essa opção no seu site?
				'''
			if 'logotipoDesfocado' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				O logotipo auxilia na formação da identidade visual da empresa e por este motivo é um dos itens mais importantes em um site. O logotipo que está no site, neste momento, está em baixa definição e aparece com aspecto desfocado. Este fato diminui o impacto positivo que o visitante teria ao acessar o site.
				'''
			if 'menusDemaisConfusos' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Um dos critérios para analisar se um site está adequado é a Navegabilidade - se o visitante consegue navegar pelo site em todas as suas áreas e se encontra facilmente, e com rapidez, aquilo que necessita. há muitos menus, o que deixa o visitante confuso, impactando bastante no potencial de marketing da sua empresa.
				'''
			if 'homeCarregada' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				A primeira página que aparece quando o site é acessado é a Home. Esta área é responsável por apresentar uma rápida introdução sobre a empresa (quem é ela, o que faz, logotipo e identidade visual além do Menu). A Home atual do site da empresa está com muito conteúdo, passando a impressão de que a empresa é desorganizada. Nesse caso, recomendamos reorganizar o menu para incluir essas informações em páginas internas e, com isso, deixar a página inicial mais limpa.
				'''
			if 'depoimentosSemDepoimentos' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Sempre aconselhamos que haja uma área no site com depoimentos de clientes pois isso aumenta a credibilidade da empresa. Só que ter esta área no site sem nenhum depoimento passa uma impressão negativa sobre a empresa. O melhor, neste caso, é juntar alguns depoimentos e só depois disso habilitar esta área no site.
				'''
			if 'naoSobreEmpresa' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Não há uma página falando sobre a empresa no site. Essa página é importante para que novos clientes possam conhecer mais sobre a história do seu estabelecimento. Isso causa uma empatia maior, já que a história está diretamente relacionada com o estilo da empresa.
				'''
			if 'siteFlash' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Além disso, o fato do seu site ser baseado em imagens e Flash (que é uma tecnologia ultrapassada para criar animações) impede que o Google indexe o conteúdo das suas páginas e, com isso, esse conteúdo não aparecerá nas buscas. Consequentemente, seu site dará menor retorno ao seu negócio.
				'''
			if 'novidadesNaoAtualizada' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Ter uma página de Novidades requer alguns cuidados e o principal deles é acrescentar novas informações com certa frequência pois isto mostra ao visitante/cliente que o site é atualizado e que a empresa está funcionando a todo vapor. Agora, se eu sou um possível cliente seu e vejo que ela não está atualizada, imediatamente vou imaginar que a empresa está inativa. Por isso, é importante manter essa área atualizada ou retirá-la do site.
				'''
			if 'semLinkFacebook' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				A empresa possui um Facebook mas não há nenhuma menção a ele no site. O Facebook é uma ferramenta de recomendação e de comunicação com os clientes e sendo assim é muito importante que o visitante do site saiba de sua existência, a visite e Curta.
				'''
			if 'facebookNaoAtualizado' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Manter o Facebook atualizado, com conteúdos exclusivos, atrai novos visitantes e fideliza aqueles que já curtiram a página, por isso é fundamental que esta esteja constantemente atualizada.
				'''
			if 'facebookPerfil' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Uma coisa que as pessoas confundem bastante é a diferença entre Perfil e Página no Facebook. O Perfil é para pessoas físicas e usado de maneira pessoal, particular. Já a Página é exclusiva para empresas, é direcionada para negócios e tem funcionalidades que o Perfil não tem, como a possibilidade de fazer propaganda no Facebook.
				'''
			if 'facebookInuteis' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				No Facebook da empresa deve haver apenas imagens e informações relevantes sobre a empresa. Sugerimos ainda dedicar uma renda para impulsionamentos de conteúdos para conseguir um número maior de visualizações da sua página. Além, é claro, de ter um link no site da empresa que redirecione para a página do Facebook.
				'''
			if 'semFacebook' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Por fim, tendo em vista a influência e alcance das redes sociais, aconselho que seja criada uma página no Facebook e/ou Twitter e que sejam constantemente atualizadas. Ela ajuda bastante na captação do público para sua página e, consequentemente, para seu negócio. Além disso, como é direcionada para fins comerciais, não possui as mesmas limitações de um perfil, por exemplo.
				'''
			if 'facebookPoucasCurtidas' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Impulsionar a página do Facebook é uma alternativa que pode ajudar a empresa a aumentar em muito o número de visitantes, curtidas e interações de pessoas interessadas em conhecer mais sobre a sua atividade. Na maior parte das vezes, o retorno é bem interessante para as vendas.
				'''
			if 'facebookOK' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Por fim, parabenizo a equipe por colocar conteúdos que são do interesse dos clientes no Facebook e por manter a página atualizada. Isso é ótimo!
				'''
			if 'referenciasMSN' in request.POST.getlist('itensAssinalados[]') and not 'referenciasOrkut' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				O MSN não existe mais desde o ano de 2013 e mantê-lo no site passa a imagem de que o mesmo não é atualizado com frequência, o que é uma péssima imagem para qualquer empresa.
				'''
			if 'referenciasOrkut' in request.POST.getlist('itensAssinalados[]') and not 'referenciasMSN' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Há ainda um link para o Orkut. Esta rede social não existe desde o ano de 2014 e mantê-la no site passa a impressão de que o mesmo não é atualizado com frequência.
				'''
			if 'referenciasMSN' in request.POST.getlist('itensAssinalados[]') and 'referenciasOrkut' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				O MSN não existe mais desde o ano de 2013 e o Orkut desde 2014. Manter links ou referências a eles no site passa a imagem de que o mesmo não é atualizado, o que é uma péssima imagem para qualquer empresa.
				'''
			if 'efeitosSonoros' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Colocar sons em sites - seja música, como efeitos ou em um vídeo que começa automaticamente - não são aconselháveis, pois ao fazer isso você restringe o público que vai gostar e acessar o seu site, uma vez que não são todas as pessoas que vão gostar de barulhos na página e não é em todo lugar que é possível acessar um site deste tipo. O melhor, então, é não utilizar este efeito no site.
				'''
			if request.POST.get('outrosComentarios'):
				texto += '''<br><br>
				%s
				''' % request.POST.get('outrosComentarios').encode('utf-8')
			texto += '''<br><br>
			Minha empresa, a Mazzolli Sistemas (www.mazzollisistemas.com.br), pode ajudá-los em tudo isso e ainda contando com um módulo administrativo para que vocês mesmos possam gerenciar o conteúdo do site sem depender da empresa que o criou. E, claro, nossa consultoria não só hoje como em qualquer momento que precisarem, sem nenhum custo adicional.<br><br>
			Fico no aguardo do seu retorno para conversarmos melhor sobre todas as possibilidades que existem para este negócio.<br><br>
			Atenciosamente,
			'''
		elif request.POST.get('opcao') == 'semSite':
			texto = '''
			Olá,<br><br>
			Conheci a empresa de vocês através do %s. Ao procurar informações sobre a empresa de vocês, algumas coisas ficaram vagas e esse é o motivo do meu e-mail.<br><br>
			Meu nome é Julyanna e trabalho na área do Marketing Digital. Como forma de ajudá-los a serem melhor e mais vistos na Internet, estou fazendo essa consultoria com algumas dicas que, mesmo pequenas, costumam ter bons resultados.<br><br>
			A questão primordial do Marketing On-line é disponibilizar em um site, com endereço fácil de ser lembrado, as informações mais pertinentes do seu negócio como telefone, e-mail para contato, horário de atendimento ou endereço da empresa, além de, em breves áreas e palavras, fazer um novo visitante conhecer o trabalho de vocês e convencê-lo a fechar negócios.<br><br>
			As redes sociais, hoje, são muito importantes para complementar o site. Elas trabalham com postagens rápidas que tem como objetivo direcionar os visitantes para o seu site e, assim, torná-los seus clientes. Sendo usadas dessa forma, essas ferramentas são muito mais eficazes na divulgação da sua empresa.<br><br>
			Outro recurso muito importante para o Marketing da sua empresa é possuir endereços de e-mail personalizados como contato@%s. Isso passa maior credibilidade e profissionalismo em seus contatos.<br><br>
			Minha empresa, a Mazzolli Sistemas, possui como foco as conversões das visitas em negócios e podemos ajudá-los tornando sua empresa mais vista e lembrada. Todos os nossos sites são completamente compatíveis com dispositivos móveis como celulares e tablets, possuem URLs amigáveis (os endereços são resumidos para que o usuário que acessar sua página possa fazê-lo de modo mais prático), um módulo administrativo onde você mesmo pode gerenciar o conteúdo das páginas e com até 9 contas de e-mails com o endereço personalizado que falei, sem cobrarmos nenhum adicional por isso.<br><br>
			Fico no aguardo do seu retorno para conversarmos sobre todas as possibilidades que existem para explorar melhor o seu nicho de mercado e procurarmos trazer mais clientes para vocês.<br><br>
			Atenciosamente,
			''' % (request.POST.get('meioComunicacao').encode('utf-8'), request.POST.get('possivelDominio').encode('utf-8'))
		elif request.POST.get('opcao') == 'consultoriaSEO':
			if 'facebookPerfilSEO' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Uma coisa que as pessoas confundem bastante é a diferença entre Perfil e Página no Facebook. O Perfil é para pessoas físicas e usado de maneira pessoal, particular. Já a Página é exclusiva para empresas, é direcionada para negócios e tem funcionalidades que o Perfil não tem, como a possibilidade de fazer propagandas e anúncios no Facebook.
				'''

			if 'semConteudoProprio' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				O conteúdo das suas postagens no Facebook deve ser original e de interesse do público. É uma boa prática dar aos seus clientes ideias para usar os seus serviços ou produtos. Isso aumenta o engajamento e ajuda o cliente a lembrar de você.
				'''
			else:
				texto += '''<br><br>
				É uma boa prática dar ideias aos seus clientes para usar os seus serviços ou produtos através das postagens. Isso aumenta o engajamento e ajuda o cliente a lembrar de você.
				'''

			if 'possuiMuitasCurtidas' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Sua página está com %s curtidas. Isso é muito bom porque leva a sua empresa mais longe e aumenta a representação de cada postagem da sua página. Mas quanta interação (comentários e compartilhamentos) esse número retorna? A quantidade é satisfatória? Aqui, impulsionamentos podem ser usados para aumentar sua visibilidade perante aqueles que já curtiram a sua página!
				''' % request.POST.get('qtdadeCurtidas').encode('utf-8')
			else:
				if not 'facebookPerfilSEO' in request.POST.getlist('itensAssinalados[]'):
					texto += '''<br><br>
					Sobre Curtidas, quanto mais pessoas Curtirem sua página mais longe sua marca chegará e mais representação você terá na Web. O Facebook possui ferramentas que podem ajudar você a aumentar esse número.
					'''

			if 'facebookNaoAtualizadoSEO' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				É importante que a página no Facebook seja atualizada com frequência pois isso mostra ao Facebook que há um conteúdo relevante sobre a sua empresa para mostrar aos usuários e os mantém engajados, fazendo com que você seja mais visto e lembrado pelo público.
				'''
			if 'conteudoNaoRelevanteSEO' in request.POST.getlist('itensAssinalados[]'):
				texto += '''<br><br>
				Manter a página atualizada é necessário para o Facebook mas é importante também verificar a qualidade das postagens. Postar coisas que não tenham relação com o seu negócio (e nem podem ter) diminui a sua significância no Facebook, o que faz com que os seus algoritmos considerem que você está praticando SPAM e, com isso, ele não indicará mais o seu negócio organicamente, além de fazer o seu público perder o interesse pelo conteúdo apresentado e, consequentemente, pela marca.
				'''
			texto += '''<br><br>
			Essas são apenas algumas dicas e nós sabemos como pode ser trabalhoso colocar tudo isso em prática. Para isso, minha empresa, a Mazzolli Sistemas, possui um serviço que pode ajudar tanto a prospectar clientes na Internet como manter as mídias sociais constantemente atualizadas.<br><br>
			Que tal marcarmos uma reunião sem compromisso para conversarmos melhor?<br><br>
			Fico aguardando sua resposta.<br><br>
			Atenciosamente,
			'''

		#Assinatura
		texto += '<br><br><a href="http://www.mazzollisistemas.com.br" target="_blank"><img src="http://mazzollisistemas.com.br/static/imagens/assinaturaJu.png" alt="Mazzolli Sistemas"></a>'

		#Cadastra o texto no banco de dados
		dataHoraEnvio = datetime.strptime(
			request.POST.get('dataHoraEnvio'),
			'%d/%m/%Y %H:%M'
		)
		zonaLocal = pytz.timezone('America/Sao_Paulo')
		dataHoraEnvio = zonaLocal.localize(dataHoraEnvio)

		Consultoria.objects.create(
			usuario = request.user.usuario_set.first(),
			dataHoraEnvio = dataHoraEnvio,
			enviado = True, #Desabilitando o envio de e-mails pelo servidor
			ramoAtividade = RamoConsultoria.objects.get(id = int(request.POST.get('ramoAtividade'))),
			empresa = request.POST.get('nomeEmpresa'),
			dominio = request.POST.get('dominio'),
			email = request.POST.get('emailEmpresa'),
			mensagem = texto,
			observacoes = request.POST.get('observacoes')
		)

		resposta = {
			'status': '1',
			'texto': texto,
		}
		return JsonResponse(resposta)

@method_decorator([login_required, csrf_exempt], name = 'dispatch')
class UploadPrintSiteView(View):
	def post(self, request, **kwargs):
		dados = {}
		try:
			with open(os.path.join(settings.MEDIA_ROOT, 'prints', request.FILES['printSite'].name), 'wb+') as arquivo:
				for chunk in request.FILES['printSite'].chunks():
					arquivo.write(chunk)
				arquivo.close()

			dados['status'] = 200
		except:
			dados['status'] = 500
		return JsonResponse(dados)

@method_decorator(login_required, name = 'dispatch')
class LogoutView(View):
	def get(self, request, **kwargs):
		logout(request)
		return redirect('/login')
