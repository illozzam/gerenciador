#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.utils import timezone

class Config(models.Model):
	variavel = models.CharField(max_length = 50, unique = True)
	valor = models.CharField(max_length = 400, null = True, blank = True)

	def __unicode__(self):
		return self.variavel

	class Meta:
		verbose_name = 'configuração'
		verbose_name_plural = 'configurações'
		ordering = ['variavel']

class Usuario(models.Model):
	usuario = models.ForeignKey(User)
	cargo = models.CharField(max_length = 200)
	facebook = models.CharField(max_length = 20, null = True, blank = True)
	telefone = models.CharField(max_length = 16, null = True, blank = True)

	def __unicode__(self):
		return self.usuario.username

	def thumbnail(self):
		if self.facebook:
			return format_html('<img src="https://graph.facebook.com/v2.10/%s/picture?type=large" height="100" alt="%s">' % (self.facebook, self.usuario.username))
		else:
			return self.usuario.username
	thumbnail.allow_tags = True

	def nomeUsuario(self):
		return self.usuario.username

	class Meta:
		verbose_name = 'usuário'
		verbose_name_plural = 'usuários'

class Mensagem(models.Model):
	remetente = models.ForeignKey(Usuario, related_name = 'remetente')
	destinatario = models.ForeignKey(Usuario, related_name = 'destinatario')
	dataHoraEnvio = models.DateTimeField(auto_now_add = True)
	dataHoraLeitura = models.DateTimeField(null = True, blank = True)
	assunto = models.CharField(max_length = 255, null = True, blank = True)
	texto = models.TextField(null = True, blank = True)
	lida = models.BooleanField(default = False)

	def __unicode__(self):
		return '%s - De %s para %s' % (
			self.dataHoraEnvio.isoformat(),
			self.remetente.usuario.username,
			self.destinatario.usuario.username
		)

	def ler(self):
		try:
			self.lida = True
			self.dataHoraLeitura = timezone.now()
			self.save()
			return True
		except:
			return False

	class Meta:
		verbose_name_plural = 'mensagens'
		ordering = ['-dataHoraEnvio']

class Tarefa(models.Model):
	prioridades = [
		['1', 'Urgente'],
		['2', 'Importante'],
		['3', 'Normal'],
		['4', 'Não Importante'],
	]

	statusPossiveis = [
		['A', 'Aberto'],
		['C', 'Concluído'],
	]

	usuarioOrigem = models.ForeignKey(Usuario, verbose_name = 'Adicionado por', related_name = 'usuarioOrigem')
	usuarioDestino = models.ForeignKey(Usuario, verbose_name = 'Usuário destino', related_name = 'usuarioDestino')
	dataHoraInclusao = models.DateTimeField(auto_now_add = True)
	data = models.DateField(null = True, blank = True)
	titulo = models.CharField(max_length = 500, verbose_name = 'Título')
	prioridade = models.CharField(max_length = 1, choices = prioridades)
	descricao = models.TextField(null = True, blank = True, verbose_name = 'Descrição')
	status = models.CharField(max_length = 1, choices = statusPossiveis, default = 'A')

class Estado(models.Model):
	nome = models.CharField(max_length = 200)
	uf = models.CharField(max_length = 2)
	ordem = models.IntegerField(default = 99)

	def __unicode__(self):
		return self.nome

	class Meta:
		ordering = ['ordem', 'uf']

class Cidade(models.Model):
	estado = models.ForeignKey(Estado)
	nome = models.CharField(max_length = 200)
	ordem = models.IntegerField(default = 999)

	def __unicode__(self):
		return self.nome

	class Meta:
		ordering = ['ordem', 'estado', 'nome']

class Cliente(models.Model):
	tiposPessoa = [
		['F', 'Física'],
		['J', 'Jurídica'],
	]

	dataHoraCadastro = models.DateTimeField(auto_now_add = True, verbose_name = 'Cadastrado em')
	tipo = models.CharField(max_length = 1, choices = tiposPessoa)
	nome = models.CharField(max_length = 200, null = True, blank = True)
	sobrenome = models.CharField(max_length = 200, null = True, blank = True)
	cpf = models.CharField(max_length = 14, null = True, blank = True, verbose_name = 'CPF')
	razaoSocial = models.CharField(max_length = 200, null = True, blank = True, verbose_name = 'Razão Social')
	responsavel = models.CharField(max_length = 200, null = True, blank = True, verbose_name = 'Responsável')
	cnpj = models.CharField(max_length = 18, null = True, blank = True, verbose_name = 'CNPJ')
	email = models.CharField(max_length = 300, verbose_name = 'E-mail')
	telefone = models.CharField(max_length = 15, null = True, blank = True)
	cep = models.CharField(max_length = 9, null = True, blank = True, verbose_name = 'CEP')
	endereco = models.CharField(max_length = 300, null = True, blank = True, verbose_name = 'Endereço')
	numero = models.CharField(max_length = 20, null = True, blank = True, verbose_name = 'Número')
	complemento = models.CharField(max_length = 30, null = True, blank = True)
	bairro = models.CharField(max_length = 50, null = True, blank = True)
	cidade = models.ForeignKey(Cidade)

	def __unicode__(self):
		if self.tipo == 'F': #Se for pessoa física
			return '%s %s' % (self.nome, self.sobrenome)
		else: #Se for pessoa jurídica
			return self.razaoSocial

	def nomeCompleto(self):
		return self.nome + ' ' + self.sobrenome

	class Meta:
		ordering = ['sobrenome', 'razaoSocial']

class Servico(models.Model):
	nome = models.CharField(max_length = 50)
	valor = models.DecimalField(max_digits = 10, decimal_places = 2)

	def __unicode__(self):
		return self.nome

class Modulo(models.Model):
	servico = models.ForeignKey(Servico)
	nome = models.CharField(max_length = 50)
	valor = models.DecimalField(max_digits = 10, decimal_places = 2)

	def __unicode__(self):
		return self.nome

class Contrato(models.Model):
	dataHoraInclusao = models.DateTimeField(auto_now_add = True)
	numero = models.CharField(max_length = 10, verbose_name = 'Número do Contrato')
	cliente = models.ForeignKey(Cliente)
	servico = models.ForeignKey(Servico, verbose_name = 'Serviço')
	modulos = models.ManyToManyField(Modulo, null = True, blank = True, verbose_name = 'Módulos')
	valor = models.DecimalField(max_digits = 10, decimal_places = 2)
	qtdadeParcelas = models.IntegerField(default = 1, verbose_name = 'Quantidade de Parcelas')
	diaPagamento = models.IntegerField(verbose_name = 'Dia dos Pagamentos', help_text = 'Número inteiro. Apenas o dia.')
	vigencia = models.IntegerField(default = 12, null = True, blank = True, verbose_name = 'Tempo de Vigência', help_text = 'Em meses')
	observacoes = models.TextField(null = True, blank = True, verbose_name = 'Observações')

	def __unicode__(self):
		if self.cliente.tipo == 'F':
			return '%s - %s %s' % (self.numero, self.cliente.nome, self.cliente.sobrenome)
		else:
			return '%s - %s' % (self.numero, self.cliente.razaoSocial)

	class Meta:
		ordering = ['numero']

class RamoConsultoria(models.Model):
	nome = models.CharField(max_length = 200)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = 'ramos de atividade'
		verbose_name_plural = 'ramos de atividade'
		ordering = ['nome']

class Consultoria(models.Model):
	usuario = models.ForeignKey(Usuario, verbose_name = 'usuário')
	dataHoraInclusao = models.DateTimeField(auto_now_add = True, verbose_name = 'Data e Hora da Inclusão')
	dataHoraEnvio = models.DateTimeField(verbose_name = 'Data e Hora do Envio', null = True, blank = True)
	enviado = models.BooleanField(default = True)
	printSite = models.ImageField(upload_to = 'prints', null = True, blank = True) #Não serve para nada
	ramoAtividade = models.ForeignKey(RamoConsultoria, null = True, blank = True, verbose_name = 'Ramo de Atividade')
	empresa = models.CharField(max_length = 255)
	dominio = models.CharField(max_length = 255, null = True, blank = True, verbose_name = 'domínio')
	email = models.CharField(max_length = 255, null = True, blank = True, verbose_name = 'e-mail')
	mensagem = models.TextField()
	observacoes = models.TextField(null = True, blank = True, verbose_name = 'observações')

	def __unicode__(self):
		return self.empresa

	class Meta:
		ordering = ['-dataHoraInclusao']

class ContasAPagar(models.Model):
	usuario = models.ForeignKey(Usuario)
	dataHoraCadastro = models.DateTimeField(auto_now_add = True)
	data = models.DateField()
	valor = models.DecimalField(max_digits = 10, decimal_places = 2)
	descricao = models.CharField(max_length = 50, verbose_name = 'descrição')
	codigoBarras = models.CharField(max_length = 59, null = True, blank = True, verbose_name = 'Código de Barras')
	pago = models.BooleanField(default = False)

	def __unicode__(self):
		return self.descricao + ' - R$ ' + str(self.valor)

	class Meta:
		ordering = ['data', 'descricao']
		verbose_name = 'contas a pagar'
		verbose_name_plural = 'contas a pagar'

class ContasAReceber(models.Model):
	data = models.DateField()
	valor = models.DecimalField(max_digits = 10, decimal_places = 2)
	descricao = models.CharField(max_length = 50, verbose_name = 'descrição')
	recebido = models.BooleanField(default = False)

	def __unicode__(self):
		return self.descricao + ' - R$ ' + str(self.valor)

	class Meta:
		ordering = ['data', 'descricao']
		verbose_name = 'contas a receber'
		verbose_name_plural = 'contas a receber'

class Tesouraria(models.Model):
	tiposTesouraria = [
		['E', 'Entrada'],
		['S', 'Saída'],
	]

	tipo = models.CharField(max_length = 1, choices = tiposTesouraria)
	dataHora = models.DateTimeField(default = timezone.now, verbose_name = 'Data e Hora')
	valor = models.DecimalField(max_digits = 10, decimal_places = 2)
	descricao = models.CharField(max_length = 50, verbose_name = 'descrição')

	def __unicode__(self):
		return self.descricao + ' - R$ ' + str(self.valor)

	class Meta:
		ordering = ['-dataHora', 'descricao']
		verbose_name = 'tesouraria'
		verbose_name_plural = 'tesouraria'
