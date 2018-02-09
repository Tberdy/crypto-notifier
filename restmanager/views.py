from django.contrib.auth.models import User
from restmanager.models import Alert
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from restmanager.serializers import UserSerializer, AlertSerializer
from restmanager.utils import createTask, cleanupTasks
from restmanager.validators import validateUserData, validateAlertData

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError


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

    def create(self, request):
        validateUserData(request.data)
        user = User.objects.filter(username=request.data['username'])
        if user:
            raise ValidationError('Username already exists')

        user = User.objects.create_user(request.data['username'], request.data['email'], request.data['password'])
        user.save()

        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        validateUserData(request.data)
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        user.username = request.data['username']
        user.email = request.data['email']
        user.set_password(request.data['password'])
        user.save()

        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        user.delete()

        return Response({})


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
        validateAlertData(request.data)
        alert = Alert()
        alert.crypto = request.data['crypto']
        alert.inCurrency = request.data['inCurrency']
        alert.mode = request.data['mode']
        alert.threshold = request.data['threshold']

        if alert.mode == 'timeframe':
            alert.timeframe = request.data['timeframe']
        else:
            alert.timeframe = 0

        alert.currency_pair = alert.crypto + '-' + alert.inCurrency
        alert.user = User.objects.get(pk=user_pk)
        alert.save()

        createTask(alert.currency_pair)

        serializer = AlertSerializer(alert, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None, user_pk=None):
        validateAlertData(request.data)
        alert = Alert.objects.get(pk=pk)

        old_currency_pair = alert.currency_pair
        new_currency_pair = request.data['crypto'] + '-' + request.data['inCurrency']

        alert.crypto = request.data['crypto']
        alert.inCurrency = request.data['inCurrency']
        alert.mode = request.data['mode']
        alert.threshold = request.data['threshold']

        if alert.mode == 'timeframe':
            alert.timeframe = request.data['timeframe']
        else:
            alert.timeframe = 0

        alert.currency_pair = new_currency_pair
        alert.save()

        if old_currency_pair != new_currency_pair:
            cleanupTasks(old_currency_pair)
            createTask(new_currency_pair)

        serializer = AlertSerializer(alert, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, pk=None, user_pk=None):
        alert = Alert.objects.get(pk=pk)
        currency_pair = alert.currency_pair

        alert.delete()
        cleanupTasks(currency_pair)

        return Response({})


@api_view(['POST'])
@permission_classes(())
def register(request):
    validateUserData(request.data)
    user = User.objects.filter(username=request.data['username'])
    if user:
        raise ValidationError('Username already exists')

    user = User.objects.create_user(request.data['username'], request.data['email'], request.data['password'])
    user.save()

    serializer = UserSerializer(user, context={'request': request})
    return Response(serializer.data)


class login(APIView):
    permission_classes = ()
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'id': user.id, 'email': user.email, 'username': user.username})
