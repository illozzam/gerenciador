from django.urls import path

from .views import (
    ContasAPagarView,
    ContasAReceberView,
    ExtratoBancarioView,
    FluxoDeCaixaView,
)

urlpatterns = [
    path("contas-a-pagar/", ContasAPagarView.as_view(), name="contas-a-pagar"),
    path("contas-a-receber/", ContasAReceberView.as_view(), name="contas-a-receber"),
    path("fluxo-de-caixa/", FluxoDeCaixaView.as_view(), name="fluxo-de-caixa"),
    path("extrato-bancario/", ExtratoBancarioView.as_view(), name="extrato-bancario"),
]
