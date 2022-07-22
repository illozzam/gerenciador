from principal.models import Config
from financeiro.models import Categoria, TermoCategoria


class Inicio:
    @staticmethod
    def dados_iniciais():
        print("Criando config...")
        Config.objects.create(
            variavel="ultima_data_extrato_bancario", valor="1900-01-01"
        )

        print("Criando categorias...")
        cat = Categoria.objects.create(nome="Deslocamento")
        TermoCategoria.objects.create(termo="*UBER", categoria=cat)
        TermoCategoria.objects.create(termo="uber", categoria=cat)

        cat = Categoria.objects.create(nome="Recarga de Celular")
        TermoCategoria.objects.create(termo="RECARGA CELULAR", categoria=cat)

        cat = Categoria.objects.create(nome="Delivery")
        TermoCategoria.objects.create(termo="19468242", categoria=cat)

        cat = Categoria.objects.create(nome="Suprimentos")
        TermoCategoria.objects.create(
            termo="SDB COM DE ALIMENTOS PALHOCA", categoria=cat
        )

        cat = Categoria.objects.create(nome="Luz")
        TermoCategoria.objects.create(termo="Luz", categoria=cat)

        cat = Categoria.objects.create(nome="Água SAMAE")
        TermoCategoria.objects.create(termo="SAMAE", categoria=cat)

        cat = Categoria.objects.create(nome="Apartamento")
        TermoCategoria.objects.create(termo="00360305", categoria=cat)

        cat = Categoria.objects.create(nome="Salários")
        TermoCategoria.objects.create(termo="37880206", categoria=cat)

        cat = Categoria.objects.create(nome="Internet")
        TermoCategoria.objects.create(termo="Internet", categoria=cat)
        TermoCategoria.objects.create(termo="INTERNET", categoria=cat)

        cat = Categoria.objects.create(nome="MEI")
        TermoCategoria.objects.create(termo="MEI Julyanna", categoria=cat)
        TermoCategoria.objects.create(termo="MEI JULYANNA", categoria=cat)
        TermoCategoria.objects.create(termo="MEI", categoria=cat)

        cat = Categoria.objects.create(nome="ClinCard")
        TermoCategoria.objects.create(termo="Clincard", categoria=cat)
        TermoCategoria.objects.create(termo="CLINCARD", categoria=cat)
        TermoCategoria.objects.create(termo="ClinCard", categoria=cat)
        TermoCategoria.objects.create(termo="19540550", categoria=cat)

        cat = Categoria.objects.create(nome="Feira")
        TermoCategoria.objects.create(termo="DIRETO DOS VERDES VALE", categoria=cat)

        cat = Categoria.objects.create(nome="Reserva")
        TermoCategoria.objects.create(termo="18236120", categoria=cat)


Inicio.dados_iniciais()
