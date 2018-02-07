import os
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from coinbase.wallet.client import Client
from background_task import background

from django.contrib.auth.models import User
from restmanager.models import Alert


def sendMail(email, message):
    msg = MIMEMultipart()
    msg['From'] = os.environ.get('CRYPTO_MAIL_ADDRESS')
    msg['To'] = email
    msg['Subject'] = os.environ.get('CRYPTO_MAIL_SUBJECT')

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP(os.environ.get('CRYPTO_MAIL_SMTP_SERVER'), os.environ.get('CRYPTO_MAIL_SMTP_PORT'))
    server.starttls()
    server.login(os.environ.get('CRYPTO_MAIL_LOGIN'), os.environ.get('CRYPTO_MAIL_PASSWORD'))

    server.sendmail(os.environ.get('CRYPTO_MAIL_ADDRESS'), email, msg.as_string())
    server.quit()


def sendNotification(alert):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    message = ''
    if alert.mode == 'up':
        message = alert.crypto + ' is now above ' + str(alert.threshold) + ' ' + alert.inCurrency + ' !'
    elif alert.mode == 'down':
        message = alert.crypto + ' is now under ' + str(alert.threshold) + ' ' + alert.inCurrency + ' !'

    logger.info(message)
    logger.info(alert.user.email)
    sendMail(alert.user.email, message)


def getCryptoPrice(cp):
    client = Client(os.environ.get('COINBASE_API_KEY'), os.environ.get('COINBASE_API_SECRET'), api_version=os.environ.get('CRYPTO_API_VERSION'))

    return int(float(client.get_spot_price(currency_pair=cp)['amount']))


@background
def checkCryptoState(currency_pair):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    alerts = Alert.objects.all().filter(currency_pair=currency_pair)

    if alerts.count() != 0:
        price = getCryptoPrice(currency_pair)
        for alert in alerts:
            debug = '# Debug : ' + str(alert.id) + ' - alert price : ' + str(alert.threshold) + ' - online price : ' + str(price)
            logger.info(debug)
            if alert.mode == 'up':
                if alert.threshold < price:
                    sendNotification(alert)
                    alert.delete()
            elif alert.mode == 'down':
                if alert.threshold > price:
                    sendNotification(alert)
                    alert.delete()
