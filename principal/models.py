from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.html import format_html


class Config(models.Model):
	variavel = models.CharField(max_length=50, unique=True)
	valor = models.CharField(max_length=400, null=True, blank=True)

	def __str__(self):
		return self.variavel

	class Meta:
		verbose_name = 'configuração'
		verbose_name_plural = 'configurações'
		ordering = ['variavel']


class Usuario(models.Model):
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	cargo = models.CharField(max_length=200)
	facebook = models.CharField(max_length=20, null=True, blank=True)
	telefone = models.CharField(max_length=16, null=True, blank=True)

	def __str__(self):
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
