from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.CharField(max_length=10)
    inCurrency = models.CharField(max_length=10)
    mode = models.CharField(max_length=20)
    threshold = models.IntegerField()
    timeframe = models.IntegerField()
    currency_pair = models.CharField(max_length=10)
