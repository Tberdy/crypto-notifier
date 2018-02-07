from django.apps import AppConfig
from background_task import background


class CoinbaseBotConfig(AppConfig):
    name = 'coinbase_bot'

    @background(schedule=0)
    def runBot():
        print('sell !')
