from django.urls import re_path
from https.views import HTTPSView

urlpatterns = [
    re_path(
        r"^.well-known/acme-challenge/(?P<key>[a-zA-Z0-9-_.]+)/$",
        HTTPSView.as_view(),
    ),
]
