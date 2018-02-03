from django.db import models
from django.contrib.auth.models import User


class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=255)
    mode = models.CharField(max_length=255)
    threshold = models.IntegerField()
