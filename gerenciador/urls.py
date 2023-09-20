from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include(("main.urls", "main"), namespace="main")),
    path("", include(("https.urls", "https"), namespace="https")),
    path(
        "authentication/",
        include(("authentication.urls", "authentication"), namespace="authentication"),
    ),
    path(
        "financial/",
        include(("financial.urls", "financial"), namespace="financial"),
    ),
    path("admin/", admin.site.urls),
]
