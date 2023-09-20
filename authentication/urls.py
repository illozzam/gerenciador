from django.urls import path
from main.views import ScreenView
from authentication.views import LoginView, LogoutView, UpdateUserView


urlpatterns = [
    path(
        "user/profile/",
        ScreenView.as_view(screen="user-profile"),
        name="user-profile",
    ),
    path(
        "user/update/", UpdateUserView.as_view(), name="user-update"
    ),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
