from django.test import Client, TestCase
from principal.tests.factories import UsuarioFactory


class ContasAPagarTestCase(TestCase):
    def setUp(self):
        self.cliente = Client()
        usuario = UsuarioFactory()
        self.usuario = usuario.cadastra()
        self.dados_usuario = usuario.dados()

    def test_carregando_tela_com_usuario_deslogado(self):
        resposta = self.cliente.get("/financeiro/contas-a-pagar/")
        self.assertEqual(resposta.status_code, 302)

    def test_carregando_tela_com_usuario_logado(self):
        self.cliente.login(
            username=self.dados_usuario["username"],
            password=self.dados_usuario["password"],
        )
        resposta = self.cliente.get("/financeiro/contas-a-pagar/")
        self.assertEqual(resposta.status_code, 200)

    # def test_cadastrando_conta_a_pagar(self):
    #     self.cliente.login(
    #         username=self.dados_usuario['username'],
    #         password=self.dados_usuario['password']
    #     )
    #     dados_conta = {
    #         'codigo_barras': '0' * 48,
    #         'data': '2021-09-10',
    #         'valor': '100',
    #         'descricao': 'Teste de conta a pagar',
    #     }
    #     resposta = self.cliente.put('/financeiro/contas-a-pagar/', data=dados_conta)
    #     self.assertEqual(resposta.status_code, 200)
