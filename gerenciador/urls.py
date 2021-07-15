#coding: utf-8
from django.urls import re_path, include
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

from principal.views import (TelaView, LoginView, LogoutView,
							ListarCidadesView, AtualizarUsuarioView,
							VerificarMensagensView, ApagarMensagemView, EnviarMensagemView,
							AdicionarTarefaView, ExcluirTarefaView, ConcluirTarefaView, DadosTarefaView, AlterarPrioridadeTarefaView,
							CadastrarClienteView, BuscarClienteView, DadosClienteView, ExcluirClienteView,
							ProximoNumeroContratoView, CadastrarContratoView, BuscarContratoView, DetalhesContratoView,
							CadastrarContasAPagarView, EditarContasAPagarView, ExcluirContasAPagarView, ReportarPagamentoView,
							CadastrarContasAReceberView, EditarContasAReceberView, ExcluirContasAReceberView, ReportarRecebimentoView,
							CadastrarTesourariaView, PesquisarTesourariaView, ExcluirTesourariaView,
							CadastrarRamoAtividadeView, CadastrarConsultoriaView, BuscarConsultoriaView, DadosConsultoriaView, CriarConsultoriaView, UploadPrintSiteView)

urlpatterns = [
	re_path(r'^$', TelaView.as_view(tela = 'inicial'), name='inicial'),
	re_path(r'^login/$', LoginView.as_view(), name='paginaLogin'),
	re_path(r'^logout/$', LogoutView.as_view(), name='logout'),

	#Telas
	re_path(r'^telas/adicionarCliente/$', TelaView.as_view(tela = 'telaAdicionarCliente'), name='telaAdicionarCliente'),
	re_path(r'^telas/buscarCliente/$', TelaView.as_view(tela = 'telaBuscarCliente'), name='telaBuscarCliente'),
	re_path(r'^telas/adicionarConsultoria/$', TelaView.as_view(tela = 'telaAdicionarConsultoria'), name='telaAdicionarConsultoria'),
	re_path(r'^telas/criarConsultoria/$', TelaView.as_view(tela = 'telaCriarConsultoria'), name='telaCriarConsultoria'),
	re_path(r'^telas/buscarConsultoria/$', TelaView.as_view(tela = 'telaBuscarConsultoria'), name='telaBuscarConsultoria'),
	re_path(r'^telas/verConsultoria/(?P<idConsultoria>[0-9]+)/$', TelaView.as_view(tela = 'telaVerConsultoria'), name='telaVerConsultoria'),
	re_path(r'^telas/mensagens/entrada/$', TelaView.as_view(tela = 'telaMensagensEntrada'), name='telaMensagensEntrada'),
	re_path(r'^telas/mensagens/enviadas/$', TelaView.as_view(tela = 'telaMensagensEnviadas'), name='telaMensagensEnviadas'),
	re_path(r'^telas/mensagens/nova/$', TelaView.as_view(tela = 'telaNovaMensagem'), name='telaNovaMensagem'),
	re_path(r'^telas/mensagem/(?P<idMensagem>[0-9]+)/$', TelaView.as_view(tela = 'telaMensagem'), name='telaMensagem'),
	re_path(r'^telas/financeiro/contasapagar/$', TelaView.as_view(tela = 'telaContasAPagar'), name='telaContasAPagar'),
	re_path(r'^telas/financeiro/contasareceber/$', TelaView.as_view(tela = 'telaContasAReceber'), name='telaContasAReceber'),
	re_path(r'^telas/financeiro/tesouraria/$', TelaView.as_view(tela = 'telaTesouraria'), name='telaTesouraria'),
	re_path(r'^telas/contratos/adicionar/$', TelaView.as_view(tela = 'telaAdicionarContrato'), name='telaAdicionarContrato'),
	re_path(r'^telas/contratos/buscar/$', TelaView.as_view(tela = 'telaBuscarContrato'), name='telaBuscarContrato'),
	re_path(r'^telas/tarefas/$', TelaView.as_view(tela = 'telaTarefas'), name='telaTarefas'),
	re_path(r'^telas/usuario/perfil/$', TelaView.as_view(tela = 'telaPerfilUsuario'), name='telaPerfilUsuario'),

	#Funções do Sistema
	#Geral
	re_path(r'^listarCidades/$', ListarCidadesView.as_view(), name='funcaoListarCidades'),
	re_path(r'^usuario/atualizar/$', AtualizarUsuarioView.as_view(), name='funcaoAtualizarUsuario'),

	#Mensagens
	re_path(r'^mensagens/verificar/$', VerificarMensagensView.as_view(), name='verificarMensagens'),
	re_path(r'^mensagens/apagar/$', ApagarMensagemView.as_view(), name='apagarMensagem'),
	re_path(r'^mensagem/enviar/$', EnviarMensagemView.as_view(), name='enviarMensagem'),

	#Tarefas
	re_path(r'^tarefas/adicionar/$', AdicionarTarefaView.as_view(), name='adicionarTarefa'),
	re_path(r'^tarefas/excluir/$', ExcluirTarefaView.as_view(), name='excluirTarefa'),
	re_path(r'^tarefas/concluir/$', ConcluirTarefaView.as_view(), name='concluirTarefa'),
	re_path(r'^tarefas/dados/$', DadosTarefaView.as_view(), name='dadosTarefa'),
	re_path(r'^tarefas/prioridade/alterar/$', AlterarPrioridadeTarefaView.as_view(), name='alterarPrioridadeTarefa'),

	#Clientes
	re_path(r'^cliente/cadastrar/$', CadastrarClienteView.as_view(), name='cadastrarCliente'),
	re_path(r'^cliente/buscar/$', BuscarClienteView.as_view(), name='buscarCliente'),
	re_path(r'^cliente/dados/(?P<idCliente>[0-9]+)', DadosClienteView.as_view(), name = 'dadosCliente'),
	re_path(r'^cliente/excluir/(?P<idCliente>[0-9]+)', ExcluirClienteView.as_view(), name = 'excluirCliente'),

	#Contratos
	re_path(r'^contrato/proximoNumero/$', ProximoNumeroContratoView.as_view(), name='proximoNumeroContrato'),
	re_path(r'^contrato/cadastrar/$', CadastrarContratoView.as_view(), name='cadastrarContrato'),
	re_path(r'^contrato/buscar/$', BuscarContratoView.as_view(), name='buscarContrato'),
	re_path(r'^contrato/detalhes/$', DetalhesContratoView.as_view(), name='detalhesContrato'),

	#Financeiro
	re_path(r'^financeiro/contasapagar/cadastrar/$', CadastrarContasAPagarView.as_view(), name='cadastrarContasAPagar'),
	re_path(r'^financeiro/contasapagar/editar/$', EditarContasAPagarView.as_view(), name='editarContasAPagar'),
	re_path(r'^financeiro/contasapagar/excluir/$', ExcluirContasAPagarView.as_view(), name='excluirContasAPagar'),
	re_path(r'^financeiro/contasapagar/reportarPagamento/$', ReportarPagamentoView.as_view(), name='reportarPagamento'),
	re_path(r'^financeiro/contasareceber/cadastrar/$', CadastrarContasAReceberView.as_view(), name='cadastrarContasAReceber'),
	re_path(r'^financeiro/contasareceber/editar/$', EditarContasAReceberView.as_view(), name='editarContasAReceber'),
	re_path(r'^financeiro/contasareceber/excluir/$', ExcluirContasAReceberView.as_view(), name='excluirContasAReceber'),
	re_path(r'^financeiro/contasareceber/reportarRecebimento/$', ReportarRecebimentoView.as_view(), name='reportarRecebimento'),
	re_path(r'^financeiro/tesouraria/cadastrar/$', CadastrarTesourariaView.as_view(), name='cadastrarTesouraria'),
	re_path(r'^financeiro/tesouraria/pesquisar/$', PesquisarTesourariaView.as_view(), name='pesquisarTesouraria'),
	re_path(r'^financeiro/tesouraria/excluir/(?P<tesouraria_id>[0-9]+)/$', ExcluirTesourariaView.as_view(), name='excluirTesouraria'),

	#Consultorias
	re_path(r'^consultoria/cadastrarRamoAtividade/$', CadastrarRamoAtividadeView.as_view(), name = 'cadastrarRamoAtividade'),
	re_path(r'^consultoria/cadastrar/$', CadastrarConsultoriaView.as_view(), name = 'cadastrarConsultoria'),
	re_path(r'^consultoria/buscar/$', BuscarConsultoriaView.as_view(), name = 'buscarConsultoria'),
	re_path(r'^consultoria/dados/(?P<consultoria_id>[0-9]+)/$', DadosConsultoriaView.as_view(), name = 'dadosConsultoria'),
	re_path(r'^consultoria/criar/$', CriarConsultoriaView.as_view(), name = 'criarConsultoria'),
	re_path(r'^consultoria/uploadPrintSite/$', UploadPrintSiteView.as_view(), name = 'uploadPrintSite'),

	re_path(r'^admin/', admin.site.urls),

	re_path(r'^summernote/', include('django_summernote.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
