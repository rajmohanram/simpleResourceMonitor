from django.db import models


# model: HTTP endpoint
class Endpoint(models.Model):
    name = models.CharField(max_length=30, unique=True)
    url = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

