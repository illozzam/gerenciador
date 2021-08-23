from django.contrib.auth.models import User
from faker import Faker
from principal.models import Usuario


class UsuarioFactory:
    fake = Faker('pt_BR')

    def __init__(self):
        self.first_name = self.fake.name().split(' ')[0]
        self.last_name = self.fake.name().split(' ')[1]
        self.username = f'{self.first_name.lower()}.{self.last_name.lower()}'
        self.email = f'{self.username}@yopmail.com'
        self.password = self.fake.password()
        self.telefone = self.fake.phone_number()
        self.cargo = 'TESTE'
        self.facebook = 'TESTE'

    def dados(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'telefone': self.telefone,
            'cargo': self.cargo,
            'facebook': self.facebook,
        }

    def cadastra(self):
        usuario_django = User.objects.create_user(username=self.username, email=self.email)
        usuario_django.first_name = self.first_name
        usuario_django.last_name = self.last_name
        usuario_django.set_password(self.password)
        usuario_django.save()

        usuario_aplicacao = Usuario.objects.create(usuario=usuario_django, telefone=self.telefone, facebook=self.facebook, cargo=self.cargo)
        return usuario_aplicacao
