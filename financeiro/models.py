from django.db import models
from django.utils import timezone


class ContasAPagar(models.Model):
	data_hora_cadastro = models.DateTimeField(auto_now_add=True)
	data = models.DateField()
	valor = models.DecimalField(max_digits=10, decimal_places=2)
	descricao = models.CharField(max_length=50, verbose_name='descrição')
	codigo_barras = models.CharField(max_length=59, null=True, blank=True, verbose_name='Código de Barras')
	pago = models.BooleanField(default=False)

	def __str__(self):
		return self.descricao + ' - R$ ' + str(self.valor)


	class Meta:
		ordering=['data', 'descricao']
		verbose_name='contas a pagar'
		verbose_name_plural='contas a pagar'


class ContasAReceber(models.Model):
	data = models.DateField()
	valor = models.DecimalField(max_digits=10, decimal_places=2)
	descricao = models.CharField(max_length=50, verbose_name='descrição')
	recebido = models.BooleanField(default=False)

	def __str__(self):
		return self.descricao + ' - R$ ' + str(self.valor)

	class Meta:
		ordering = ['data', 'descricao']
		verbose_name = 'contas a receber'
		verbose_name_plural = 'contas a receber'


class FluxoDeCaixa(models.Model):
	tipos_fluxo = [
		['E', 'Entrada'],
		['S', 'Saída'],
	]

	tipo = models.CharField(max_length=1, choices=tipos_fluxo)
	data_hora = models.DateTimeField(default=timezone.now, verbose_name='Data e Hora')
	valor = models.DecimalField(max_digits=10, decimal_places=2)
	descricao = models.CharField(max_length=50, verbose_name='descrição')

	def __str__(self):
		return self.descricao + ' - R$ ' + str(self.valor)

	class Meta:
		ordering = ['-data_hora', 'descricao']
		verbose_name = 'fluxo de caixa'
		verbose_name_plural = 'fluxos de caixa'
