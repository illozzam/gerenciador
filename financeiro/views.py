import json
from datetime import datetime
from urllib.parse import parse_qs

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import ContasAPagar, ContasAReceber, FluxoDeCaixa


@method_decorator(csrf_exempt, name='dispatch')
class ContasAPagarView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        template = 'financeiro/contas_a_pagar.html'
        contexto = {
            'contas': ContasAPagar.objects.all(),
        }
        return render(request, template, contexto)

    def put(self, request, **kwargs):
        payload = parse_qs(request.body.decode())
        resposta = dict()

        if payload.get('codigo_barras'):
            codigo_barras = payload['codigo_barras'][0].replace(' ', '').replace('.', '').replace('-', '')
            codigo_barras = codigo_barras.replace(' ', '').replace('.', '').replace('-', '')
            for digito in range(4, len(codigo_barras) + 12, 5):
                codigo_barras = codigo_barras[0:digito] + ' ' + codigo_barras[digito:]
            if len(codigo_barras) == 60: codigo_barras = codigo_barras[:-1]
        else:
            codigo_barras = ''

        dados_cadastro = {
            'usuario': request.user.usuario_set.first(),
            'data': datetime.strptime(payload['data'][0], '%Y-%m-%d'),
            'valor': float(payload['valor'][0].replace(',', '.')),
            'descricao': payload['descricao'][0],
            'codigo_barras': codigo_barras,
        }
        conta = ContasAPagar.objects.create(**dados_cadastro)

        resposta['conta'] = serialize('json', [conta])
        resposta['status'] = 200
        return JsonResponse(resposta, safe=False)

    def post(self, request, **kwargs):
        resposta = dict()

        if request.POST.get('acao') == 'alterar-data':
            conta = ContasAPagar.objects.get(id = request.POST['id_conta'])
            conta.data = request.POST.get('data')
            conta.save()
            resposta['status'] = 200
        elif request.POST.get('acao') == 'reportar-pagamento':
            conta = ContasAPagar.objects.get(id = request.POST['id_conta'])
            conta.pago = True
            conta.save()

            FluxoDeCaixa.objects.create(
                tipo = 'S',
                descricao = conta.descricao,
                valor = conta.valor
            )

            resposta['status'] = 200
        return JsonResponse(resposta)

    def delete(self, request, **kwargs):
        resposta = dict()
        if 'id_conta' in request.GET.keys():
            if ContasAPagar.objects.filter(id=request.GET.get('id_conta')).exists():
                ContasAPagar.objects.get(id=request.GET.get('id_conta')).delete()
                resposta['status'] = 200
            else:
                resposta['status'] = 404
        else:
            resposta['status'] = 400
        return JsonResponse(resposta)


@method_decorator(csrf_exempt, name='dispatch')
class ContasAReceberView(LoginRequiredMixin, View):
    def alterar_data(self, id_conta, data):
        conta = ContasAReceber.objects.get(id=id_conta)
        conta.data = data
        conta.save()
        return 200

    def reportar_recebimento(self, id_conta):
        conta = ContasAReceber.objects.get(id=id_conta)
        conta.recebido = True
        conta.save()

        FluxoDeCaixa.objects.create(
            tipo = 'E',
            descricao = conta.descricao,
            valor = conta.valor
        )
        return 200

    def get(self, request, **kwargs):
        template = 'financeiro/contas_a_receber.html'
        contexto = {
            'contas': ContasAReceber.objects.all(),
        }
        return render(request, template, contexto)

    def put(self, request, **kwargs):
        payload = parse_qs(request.body.decode())
        resposta = dict()

        conta = ContasAReceber.objects.create(
            data = datetime.strptime(payload['data'][0], '%Y-%m-%d'),
            valor = float(payload['valor'][0].replace(',', '.')),
            descricao = payload['descricao'][0]
        )

        resposta['conta'] = serialize('json', [conta])
        resposta['status'] = 200
        return JsonResponse(resposta)

    def post(self, request, **kwargs):
        resposta = dict()

        if ContasAReceber.objects.filter(id=request.POST.get('id_conta')).exists():
            if request.POST.get('acao') == 'alterar-data':
                resposta['status'] = self.alterar_data(request.POST.get('id_conta'), request.POST.get('data'))
                return JsonResponse(resposta)
            elif request.POST.get('acao') == 'reportar-recebimento':
                resposta['status'] = self.reportar_recebimento(request.POST.get('id_conta'))
        else:
            resposta['status'] = 404
        return JsonResponse(resposta)

    def delete(self, request, **kwargs):
        payload = parse_qs(request.body.decode())
        resposta = dict()
        if ContasAReceber.objects.filter(id=payload['id_conta'][0]).exists():
            ContasAReceber.objects.get(id=payload['id_conta'][0]).delete()
            resposta['status'] = 200
        else:
            resposta['status'] = 404
        return JsonResponse(resposta)


class FluxoDeCaixaView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        #Tela
        template = 'financeiro/fluxo_de_caixa.html'
        return render(request, template, {})

        #Pesquisar fluxo de caixa
        try:
            d1 = datetime.strptime(request.GET.get('dataInicial'), '%Y-%m-%d')
            d2 = datetime.strptime(request.GET.get('dataFinal'), '%Y-%m-%d')
            dataInicial = datetime(d1.year, d1.month, d1.day, 0, 0)
            dataFinal = datetime(d2.year, d2.month, d2.day, 23, 59)

            self.dados['saldoAnterior'] = 0
            for movimentacao in Tesouraria.objects.filter(dataHora__lte = dataInicial):
                if movimentacao.tipo == 'E':
                    self.dados['saldoAnterior'] += float(movimentacao.valor)
                else:
                    self.dados['saldoAnterior'] -= float(movimentacao.valor)

            self.dados['movimentacoes'] = list(
                Tesouraria.objects.filter(
                    dataHora__gte = dataInicial,
                    dataHora__lte = dataFinal
                ).values(
                    'id',
                    'tipo',
                    'dataHora',
                    'valor',
                    'descricao'
                )
            )
            self.dados['status'] = 1
        except:
            self.dados['status'] = 0
        return JsonResponse(self.dados, safe = False)

    def put(self, request, **kwargs):
        try:
            Tesouraria.objects.create(
                tipo = request.POST.get('tipo'),
                dataHora = datetime.strptime(request.POST.get('dataHora'), '%d/%m/%Y %H:%M'),
                valor = float(request.POST.get('valor').replace(',', '.')),
                descricao = request.POST.get('descricao')
            )
            self.dados['status'] = 1
        except:
            self.dados['status'] = 0
        return JsonResponse(self.dados, safe = False)

    def delete(self, request, **kwargs):
        if Tesouraria.objects.filter(id = self.kwargs['tesouraria_id']).exists():
            try:
                Tesouraria.objects.get(id = self.kwargs['tesouraria_id']).delete()
                self.dados['status'] = 1
            except:
                self.dados['status'] = 2
        else:
            self.dados['status'] = 0
        return JsonResponse(self.dados, safe = False)
