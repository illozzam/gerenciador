import codecs
import csv
from datetime import datetime
from typing import List

from financeiro.models import FluxoDeCaixa, TermoCategoria
from principal.models import Config


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
    def __atualiza_ultima_data_extrato_bancario(
        cls, movimentacoes: List[FluxoDeCaixa], ultima_data: datetime.date
    ) -> None:
        try:
            if movimentacoes[-1].data > ultima_data:
                Config.objects.filter(variavel="ultima_data_extrato_bancario").update(
                    valor=movimentacoes[-1].data.isoformat()
                )
        except IndexError:
            raise IndexError("Nenhuma movimentação encontrada após a última data cadastrada")

    @classmethod
    def extrair(cls, arquivo) -> List[FluxoDeCaixa]:
        leitor = csv.reader(codecs.iterdecode(arquivo, "utf-8"), delimiter=";")
        ultima_data = datetime.date(
            datetime.fromisoformat(
                Config.objects.get(variavel="ultima_data_extrato_bancario").valor
            )
        )
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
                            if len(transacao) == 4
                            and transacao[0] != "DATA LANÇAMENTO"
                            and datetime.date(
                                datetime.strptime(transacao[0], "%d/%m/%Y")
                            )
                            > ultima_data
                        ],
                    )
                )
            )
            cls.__atualiza_ultima_data_extrato_bancario(movimentacoes, ultima_data)
        except IndexError:
            raise IndexError("Nenhuma movimentação encontrada após a última data cadastrada")
        except Exception as erro:
            raise Exception(erro)

        return movimentacoes
