from django.contrib.auth.models import User
from faker import Faker


class UserFactory:
    fake = Faker("pt_BR")

    def __init__(self):
        self.first_name = self.fake.name().split(" ")[0]
        self.last_name = self.fake.name().split(" ")[1]
        self.username = f"{self.first_name.lower()}.{self.last_name.lower()}"
        self.email = f"{self.username}@yopmail.com"
        self.password = self.fake.password()

    def data(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "password": self.password,
        }

    def sign_up(self):
        django_user = User.objects.create_user(username=self.username, email=self.email)
        django_user.first_name = self.first_name
        django_user.last_name = self.last_name
        django_user.set_password(self.password)
        django_user.save()
        return django_user
