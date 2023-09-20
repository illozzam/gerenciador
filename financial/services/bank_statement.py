import codecs
import csv
from datetime import datetime
from typing import List

from financial.models import CashFlow, FinancialTerm
from main.models import Config


class BankStatementService:
    @classmethod
    def __fill_categories(cls, transactions: List[CashFlow]) -> List[CashFlow]:
        for term in FinancialTerm.objects.all():
            for transaction in transactions:
                if term.term in transaction.description.split(" "):
                    transaction.category = term.category
                    continue
        return transactions

    @classmethod
    def __update_last_bank_statement_date(
        cls, transactions: List[CashFlow], last_date: datetime.date
    ) -> None:
        try:
            if transactions[-1].date > last_date:
                Config.objects.filter(variable="ultima_data_extrato_bancario").update(
                    value=transactions[-1].date.isoformat()
                )
        except IndexError:
            raise IndexError(
                "Nenhuma movimentação encontrada após a última data cadastrada"
            )

    @classmethod
    def extract(cls, file) -> List[CashFlow]:
        reader = csv.reader(codecs.iterdecode(file, "utf-8"), delimiter=";")
        last_date = datetime.date(
            datetime.fromisoformat(
                Config.objects.get(variable="ultima_data_extrato_bancario").value
            )
        )
        try:
            transactions = cls.__fill_categories(
                list(
                    map(
                        lambda t: CashFlow(
                            date=datetime.date(datetime.strptime(t[0], "%d/%m/%Y")),
                            description=t[1],
                            value=abs(float(t[2].replace(".", "").replace(",", "."))),
                            type="E"
                            if float(t[2].replace(".", "").replace(",", ".")) > 0
                            else "S",
                        ),
                        [
                            transaction
                            for transaction in list(reader)
                            if len(transaction) == 4
                            and transaction[0] != "DATA LANÇAMENTO"
                            and datetime.date(
                                datetime.strptime(transaction[0], "%d/%m/%Y")
                            )
                            > last_date
                        ],
                    )
                )
            )
            cls.__update_last_bank_statement_date(transactions, last_date)
        except IndexError:
            raise IndexError(
                "Nenhuma movimentação encontrada após a última data cadastrada"
            )
        except Exception as erro:
            raise Exception(erro)

        return transactions
