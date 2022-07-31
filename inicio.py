from django.contrib.auth.models import User

from financeiro.models import Categoria, TermoCategoria
from principal.models import Config


class Inicio:
    def __init__(self):
        configs = [
            Config.objects.create(
                variavel="ultima_data_extrato_bancario", valor="1900-01-01"
            )
        ]

        categorias = [
            Categoria.objects.create(nome="Deslocamento"),
            Categoria.objects.create(nome="Recarga de Celular"),
            Categoria.objects.create(nome="Delivery"),
            Categoria.objects.create(nome="Suprimentos"),
            Categoria.objects.create(nome="Luz"),
            Categoria.objects.create(nome="Água SAMAE"),
            Categoria.objects.create(nome="Apartamento"),
            Categoria.objects.create(nome="Salários"),
            Categoria.objects.create(nome="Internet"),
            Categoria.objects.create(nome="MEI"),
            Categoria.objects.create(nome="ClinCard"),
            Categoria.objects.create(nome="Feira"),
            Categoria.objects.create(nome="Reserva"),
        ]

        termos_categorias = [
            TermoCategoria.objects.create(termo="*UBER", categoria=categorias[0]),
            TermoCategoria.objects.create(termo="uber", categoria=categorias[0]),
            TermoCategoria.objects.create(
                termo="RECARGA CELULAR", categoria=categorias[1]
            ),
            TermoCategoria.objects.create(termo="19468242", categoria=categorias[2]),
            TermoCategoria.objects.create(
                termo="SDB COM DE ALIMENTOS", categoria=categorias[3]
            ),
            TermoCategoria.objects.create(termo="Luz", categoria=categorias[4]),
            TermoCategoria.objects.create(termo="SAMAE", categoria=categorias[5]),
            TermoCategoria.objects.create(termo="00360305", categoria=categorias[6]),
            TermoCategoria.objects.create(termo="37880206", categoria=categorias[7]),
            TermoCategoria.objects.create(termo="Internet", categoria=categorias[8]),
            TermoCategoria.objects.create(termo="INTERNET", categoria=categorias[8]),
            TermoCategoria.objects.create(
                termo="MEI Julyanna", categoria=categorias[9]
            ),
            TermoCategoria.objects.create(
                termo="MEI JULYANNA", categoria=categorias[9]
            ),
            TermoCategoria.objects.create(termo="MEI", categoria=categorias[9]),
            TermoCategoria.objects.create(termo="Clincard", categoria=categorias[10]),
            TermoCategoria.objects.create(termo="ClinCard", categoria=categorias[10]),
            TermoCategoria.objects.create(termo="CLINCARD", categoria=categorias[10]),
            TermoCategoria.objects.create(termo="19540550", categoria=categorias[10]),
            TermoCategoria.objects.create(
                termo="DIRETO DOS VERDES VALE", categoria=categorias[11]
            ),
            TermoCategoria.objects.create(termo="18236120", categoria=categorias[12]),
        ]

        User.objects.create_superuser(
            username="mazzolli",
            password="p4ssw0rd",
            email="ricarm@gmail.com",
            first_name="Ricardo",
            last_name="Mazzolli",
        )


Inicio()
