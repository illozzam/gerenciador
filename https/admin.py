from django.contrib import admin
from https.models import HTTPSKey


@admin.register(HTTPSKey)
class HTTPSKeyAdmin(admin.ModelAdmin):
    list_display = ["key", "date_created", "verified"]
