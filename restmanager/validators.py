from rest_framework.exceptions import ValidationError
from django.utils.datastructures import MultiValueDictKeyError


def validateUserData(data, ):
    try:
        data['username']
        data['email']
        data['password']
    except MultiValueDictKeyError:
        raise ValidationError('User API require username, email and password field')


def validateAlertData(data):
    try:
        data['crypto']
        data['inCurrency']
        data['mode']
        data['threshold']
    except MultiValueDictKeyError:
        raise ValidationError('Alert API require crypto, inCurrency, mode and threshold field')

    if data['crypto'] != 'BTC' and data['crypto'] != 'LTC' and data['crypto'] != 'BCH' and data['crypto'] != 'ETH' and data['crypto'] != 'ETC':
        raise ValidationError('crypto field must be a valid crypto currency')

    if data['inCurrency'] != 'USD' and data['inCurrency'] != 'EUR':
        raise ValidationError('inCurrency field must be a valid base currency (USD or EUR)')
