from django.contrib.auth.models import User
from crypto_rest.models import Alert
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class AlertSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Alert
        fields = ('url', 'user', 'currency', 'mode', 'threshold')
