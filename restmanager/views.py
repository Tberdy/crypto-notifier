from django.contrib.auth.models import User
from restmanager.models import Alert
from rest_framework import viewsets
from rest_framework.response import Response
from restmanager.serializers import UserSerializer, AlertSerializer

from rest_framework import authentication, permissions
from rest_framework.decorators import api_view, detail_route
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    @detail_route(methods=['GET'])
    def dev(self, request, *args, **kwargs):
        return Response({'args': args, 'kwargs': kwargs})


class AlertViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows alerts to be viewed or edited.
    """
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

    def list(self, request, user_pk=None):
        queryset = self.queryset.filter(user=user_pk)
        serializer = AlertSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, user_pk=None):
        queryset = self.queryset.filter(user=user_pk)
        alert = get_object_or_404(queryset, pk=pk)
        serializer = AlertSerializer(alert, context={'request': request})
        return Response(serializer.data)

    def create(self, request, user_pk=None):
        print(request.data)
        alert = Alert()
        alert.currency = request.data['currency']
        alert.mode = request.data['mode']
        alert.threshold = request.data['threshold']
        alert.user = User.objects.get(pk=user_pk)
        alert.save()
        serializer = AlertSerializer(alert, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None, user_pk=None):
        alert = Alert.objects.get(pk=pk)
        alert.currency = request.data['currency']
        alert.mode = request.data['mode']
        alert.threshold = request.data['threshold']
        alert.save()

        serializer = AlertSerializer(alert, context={'request': request})
        return Response(serializer.data)
