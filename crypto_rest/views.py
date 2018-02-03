from django.contrib.auth.models import User
from crypto_rest.models import Alert
from rest_framework import viewsets
from crypto_rest.serializers import UserSerializer, AlertSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class AlertViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
