from django.urls import path
from main.views import ScreenView

urlpatterns = [
    path("", ScreenView.as_view(screen="inicial"), name="inicial"),
]
