from django.test import Client, TestCase
from principal.tests.factories import UsuarioFactory


class ContasAPagarTestCase(TestCase):
    def setUp(self):
        self.cliente = Client()
        usuario = UsuarioFactory()
        self.usuario = usuario.cadastra()
        self.dados_usuario = usuario.dados()

    def test_carregando_tela_com_usuario_deslogado(self):
        resposta = self.cliente.get('/financeiro/contas-a-pagar/')
        self.assertEqual(resposta.status_code, 302)

    def test_carregando_tela_com_usuario_logado(self):
        self.cliente.login(
            username=self.dados_usuario['username'],
            password=self.dados_usuario['password']
        )
        resposta = self.cliente.get('/financeiro/contas-a-pagar/')
        self.assertEqual(resposta.status_code, 200)
