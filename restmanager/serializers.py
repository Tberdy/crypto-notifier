from django.contrib.auth.models import User
from restmanager.models import Alert
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username')


class AlertSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Alert
        fields = ('id', 'crypto', 'inCurrency', 'mode', 'threshold', 'timeframe')
