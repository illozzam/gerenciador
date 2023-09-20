from django.contrib.auth.models import User

from financial.models import FinancialCategory, FinancialTerm
from main.models import Config


class Inicio:
    def __init__(self):
        configs = [
            Config.objects.create(
                variavel="ultima_data_extrato_bancario", valor="1900-01-01"
            )
        ]

        categorias = [
            FinancialCategory.objects.create(nome="Deslocamento"),
            FinancialCategory.objects.create(nome="Recarga de Celular"),
            FinancialCategory.objects.create(nome="Delivery"),
            FinancialCategory.objects.create(nome="Suprimentos"),
            FinancialCategory.objects.create(nome="Luz"),
            FinancialCategory.objects.create(nome="Água SAMAE"),
            FinancialCategory.objects.create(nome="Apartamento"),
            FinancialCategory.objects.create(nome="Salários"),
            FinancialCategory.objects.create(nome="Internet"),
            FinancialCategory.objects.create(nome="MEI"),
            FinancialCategory.objects.create(nome="ClinCard"),
            FinancialCategory.objects.create(nome="Feira"),
            FinancialCategory.objects.create(nome="Reserva"),
        ]

        termos_categorias = [
            FinancialTerm.objects.create(termo="*UBER", categoria=categorias[0]),
            FinancialTerm.objects.create(termo="uber", categoria=categorias[0]),
            FinancialTerm.objects.create(
                termo="RECARGA CELULAR", categoria=categorias[1]
            ),
            FinancialTerm.objects.create(termo="19468242", categoria=categorias[2]),
            FinancialTerm.objects.create(
                termo="SDB COM DE ALIMENTOS", categoria=categorias[3]
            ),
            FinancialTerm.objects.create(termo="Luz", categoria=categorias[4]),
            FinancialTerm.objects.create(termo="SAMAE", categoria=categorias[5]),
            FinancialTerm.objects.create(termo="00360305", categoria=categorias[6]),
            FinancialTerm.objects.create(termo="37880206", categoria=categorias[7]),
            FinancialTerm.objects.create(termo="Internet", categoria=categorias[8]),
            FinancialTerm.objects.create(termo="INTERNET", categoria=categorias[8]),
            FinancialTerm.objects.create(
                termo="MEI Julyanna", categoria=categorias[9]
            ),
            FinancialTerm.objects.create(
                termo="MEI JULYANNA", categoria=categorias[9]
            ),
            FinancialTerm.objects.create(termo="MEI", categoria=categorias[9]),
            FinancialTerm.objects.create(termo="Clincard", categoria=categorias[10]),
            FinancialTerm.objects.create(termo="ClinCard", categoria=categorias[10]),
            FinancialTerm.objects.create(termo="CLINCARD", categoria=categorias[10]),
            FinancialTerm.objects.create(termo="19540550", categoria=categorias[10]),
            FinancialTerm.objects.create(
                termo="DIRETO DOS VERDES VALE", categoria=categorias[11]
            ),
            FinancialTerm.objects.create(termo="18236120", categoria=categorias[12]),
        ]

        User.objects.create_superuser(
            username="mazzolli",
            password="p4ssw0rd",
            email="ricarm@gmail.com",
            first_name="Ricardo",
            last_name="Mazzolli",
        )


if not Config.objects.filter(variavel="ultima_data_extrato_bancario").exists():
    Inicio()
else:
    print("Inicio já foi executado")
