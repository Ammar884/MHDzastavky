from django.db import models
from django.contrib.auth.models import User


class Station(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    identifiers = models.TextField(null=True)
    def __str__(self):
        return self.name 