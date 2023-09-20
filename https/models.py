from django.db import models


class HTTPSKey(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=43)
    password = models.CharField(max_length=43)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.key
