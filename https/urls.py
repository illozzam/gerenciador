from django.urls import re_path

from .views import PrincipalView

urlpatterns = [
    re_path(r'^.well-known/acme-challenge/(?P<chave>[a-zA-Z0-9-_.]+)/$', PrincipalView.as_view(), name='principal'),
]
