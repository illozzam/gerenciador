from django.test import Client, TestCase
from main.tests.factories import UserFactory


class BillsToPayTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        user = UserFactory()
        self.user = user.sign_up()
        self.user_data = user.data()

    def test_loading_screen_with_logged_out_user(self):
        response = self.client.get("/financial/bills-to-pay/")
        self.assertEqual(response.status_code, 302)

    def test_loading_screen_with_logged_in_user(self):
        self.client.login(
            username=self.user_data["username"],
            password=self.user_data["password"],
        )
        response = self.client.get("/financeiro/contas-a-pagar/")
        self.assertEqual(response.status_code, 200)
