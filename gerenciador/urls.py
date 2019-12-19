#coding: utf-8
"""gerenciador URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

from principal.views import *

urlpatterns = [
	url(r'^$', TelaView.as_view(tela = 'inicial'), name='inicial'),
	url(r'^login/$', LoginView.as_view(), name='paginaLogin'),
	url(r'^logout/$', LogoutView.as_view(), name='logout'),

	#Telas
	url(r'^telas/adicionarCliente/$', TelaView.as_view(tela = 'telaAdicionarCliente'), name='telaAdicionarCliente'),
	url(r'^telas/buscarCliente/$', TelaView.as_view(tela = 'telaBuscarCliente'), name='telaBuscarCliente'),
	url(r'^telas/adicionarConsultoria/$', TelaView.as_view(tela = 'telaAdicionarConsultoria'), name='telaAdicionarConsultoria'),
	url(r'^telas/criarConsultoria/$', TelaView.as_view(tela = 'telaCriarConsultoria'), name='telaCriarConsultoria'),
	url(r'^telas/buscarConsultoria/$', TelaView.as_view(tela = 'telaBuscarConsultoria'), name='telaBuscarConsultoria'),
	url(r'^telas/mensagens/entrada/$', TelaView.as_view(tela = 'telaMensagensEntrada'), name='telaMensagensEntrada'),
	url(r'^telas/mensagens/enviadas/$', TelaView.as_view(tela = 'telaMensagensEnviadas'), name='telaMensagensEnviadas'),
	url(r'^telas/mensagens/nova/$', TelaView.as_view(tela = 'telaNovaMensagem'), name='telaNovaMensagem'),
	url(r'^telas/mensagem/(?P<idMensagem>[0-9]+)/$', TelaView.as_view(tela = 'telaMensagem'), name='telaMensagem'),
	url(r'^telas/financeiro/contasapagar/$', TelaView.as_view(tela = 'telaContasAPagar'), name='telaContasAPagar'),
	url(r'^telas/financeiro/contasareceber/$', TelaView.as_view(tela = 'telaContasAReceber'), name='telaContasAReceber'),
	url(r'^telas/financeiro/tesouraria/$', TelaView.as_view(tela = 'telaTesouraria'), name='telaTesouraria'),
	url(r'^telas/contratos/adicionar/$', TelaView.as_view(tela = 'telaAdicionarContrato'), name='telaAdicionarContrato'),
	url(r'^telas/contratos/buscar/$', TelaView.as_view(tela = 'telaBuscarContrato'), name='telaBuscarContrato'),
	url(r'^telas/tarefas/$', TelaView.as_view(tela = 'telaTarefas'), name='telaTarefas'),
	url(r'^telas/usuario/perfil/$', TelaView.as_view(tela = 'telaPerfilUsuario'), name='telaPerfilUsuario'),

	#Funções do Sistema
	#Geral
	url(r'^listarCidades/$', ListarCidadesView.as_view(), name='funcaoListarCidades'),
	url(r'^usuario/atualizar/$', AtualizarUsuarioView.as_view(), name='funcaoAtualizarUsuario'),

	#Mensagens
	url(r'^mensagens/verificar/$', VerificarMensagensView.as_view(), name='verificarMensagens'),
	url(r'^mensagens/apagar/$', ApagarMensagemView.as_view(), name='apagarMensagem'),
	url(r'^mensagem/enviar/$', EnviarMensagemView.as_view(), name='enviarMensagem'),

	#Tarefas
	url(r'^tarefas/adicionar/$', AdicionarTarefaView.as_view(), name='adicionarTarefa'),
	url(r'^tarefas/excluir/$', ExcluirTarefaView.as_view(), name='excluirTarefa'),
	url(r'^tarefas/concluir/$', ConcluirTarefaView.as_view(), name='concluirTarefa'),
	url(r'^tarefas/dados/$', DadosTarefaView.as_view(), name='dadosTarefa'),
	url(r'^tarefas/prioridade/alterar/$', AlterarPrioridadeTarefaView.as_view(), name='alterarPrioridadeTarefa'),

	#Clientes
	url(r'^cliente/cadastrar/$', CadastrarClienteView.as_view(), name='cadastrarCliente'),
	url(r'^cliente/buscar/$', BuscarClienteView.as_view(), name='buscarCliente'),
	url(r'^cliente/dados/(?P<idCliente>[0-9]+)', DadosClienteView.as_view(), name = 'dadosCliente'),
	url(r'^cliente/excluir/(?P<idCliente>[0-9]+)', ExcluirClienteView.as_view(), name = 'excluirCliente'),

	#Contratos
	url(r'^contrato/proximoNumero/$', ProximoNumeroContratoView.as_view(), name='proximoNumeroContrato'),
	url(r'^contrato/cadastrar/$', CadastrarContratoView.as_view(), name='cadastrarContrato'),
	url(r'^contrato/buscar/$', BuscarContratoView.as_view(), name='buscarContrato'),
	url(r'^contrato/detalhes/$', DetalhesContratoView.as_view(), name='detalhesContrato'),

	#Financeiro
	url(r'^financeiro/contasapagar/cadastrar/$', CadastrarContasAPagarView.as_view(), name='cadastrarContasAPagar'),
	url(r'^financeiro/contasapagar/editar/$', EditarContasAPagarView.as_view(), name='editarContasAPagar'),
	url(r'^financeiro/contasapagar/excluir/$', ExcluirContasAPagarView.as_view(), name='excluirContasAPagar'),
	url(r'^financeiro/contasapagar/reportarPagamento/$', ReportarPagamentoView.as_view(), name='reportarPagamento'),
	url(r'^financeiro/contasareceber/cadastrar/$', CadastrarContasAReceberView.as_view(), name='cadastrarContasAReceber'),
	url(r'^financeiro/contasareceber/editar/$', EditarContasAReceberView.as_view(), name='editarContasAReceber'),
	url(r'^financeiro/contasareceber/excluir/$', ExcluirContasAReceberView.as_view(), name='excluirContasAReceber'),
	url(r'^financeiro/contasareceber/reportarRecebimento/$', ReportarRecebimentoView.as_view(), name='reportarRecebimento'),
	url(r'^financeiro/tesouraria/cadastrar/$', CadastrarTesourariaView.as_view(), name='cadastrarTesouraria'),
	url(r'^financeiro/tesouraria/pesquisar/$', PesquisarTesourariaView.as_view(), name='pesquisarTesouraria'),
	url(r'^financeiro/tesouraria/excluir/(?P<tesouraria_id>[0-9]+)/$', ExcluirTesourariaView.as_view(), name='excluirTesouraria'),

	#Consultorias
	url(r'^consultoria/cadastrarRamoAtividade/$', CadastrarRamoAtividadeView.as_view(), name = 'cadastrarRamoAtividade'),
	url(r'^consultoria/cadastrar/$', CadastrarConsultoriaView.as_view(), name = 'cadastrarConsultoria'),
	url(r'^consultoria/buscar/$', BuscarConsultoriaView.as_view(), name = 'buscarConsultoria'),
	url(r'^consultoria/dados/(?P<consultoria_id>[0-9]+)/$', DadosConsultoriaView.as_view(), name = 'dadosConsultoria'),
	url(r'^consultoria/criar/$', CriarConsultoriaView.as_view(), name = 'criarConsultoria'),
	url(r'^consultoria/uploadPrintSite/$', UploadPrintSiteView.as_view(), name = 'uploadPrintSite'),

	url(r'^admin/', admin.site.urls),

	url(r'^summernote/', include('django_summernote.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
