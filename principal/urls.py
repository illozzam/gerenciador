from django.urls import path
from principal.views import TelaView

urlpatterns = [
    path("", TelaView.as_view(tela="inicial"), name="inicial"),
]
