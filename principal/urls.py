from django.urls import path
from principal.views import (AtualizarUsuarioView, LoginView, LogoutView,
                             TelaView)

urlpatterns = [
    path('usuario/perfil/', TelaView.as_view(tela='usuario-perfil'), name='usuario-perfil'),
    path('usuario/atualizar/', AtualizarUsuarioView.as_view(), name='usuario-atualizar'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('', TelaView.as_view(tela='inicial'), name='inicial'),
]
