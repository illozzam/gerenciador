import codecs
import csv
from typing import List, Dict
from datetime import datetime
from financeiro.models import TermoCategoria, FluxoDeCaixa


class ExtratoBancarioService:
    @classmethod
    def __preenche_categorias(
        cls, movimentacoes: List[FluxoDeCaixa]
    ) -> List[FluxoDeCaixa]:
        for termo in TermoCategoria.objects.all():
            for movimentacao in movimentacoes:
                if termo.termo in movimentacao.descricao.split(" "):
                    movimentacao.categoria = termo.categoria
                    continue
        return movimentacoes

    @classmethod
    def extrair(cls, arquivo) -> List[FluxoDeCaixa]:
        leitor = csv.reader(codecs.iterdecode(arquivo, "utf-8"), delimiter=";")
        try:
            movimentacoes = cls.__preenche_categorias(
                list(
                    map(
                        lambda t: FluxoDeCaixa(
                            data=datetime.date(datetime.strptime(t[0], "%d/%m/%Y")),
                            descricao=t[1],
                            valor=abs(float(t[2].replace(".", "").replace(",", "."))),
                            tipo="E"
                            if float(t[2].replace(".", "").replace(",", ".")) > 0
                            else "S",
                        ),
                        [
                            transacao
                            for transacao in list(leitor)
                            if len(transacao) == 4 and transacao[0] != "DATA LANÇAMENTO"
                        ],
                    )
                )
            )
        except Exception as erro:
            raise Exception(erro)

        return movimentacoes
