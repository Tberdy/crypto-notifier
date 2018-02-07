from background_task.models import Task
from coinbase_bot.utils import checkCryptoState
from restmanager.models import Alert


def doesTaskExist(currency_pair):
    return (Task.objects.filter(verbose_name=currency_pair).count() != 0)


def createTask(currency_pair):
    if not doesTaskExist(currency_pair):
        checkCryptoState(currency_pair, verbose_name=currency_pair, repeat=5)


def deleteTask(currency_pair):
    Task.objects.filter(verbose_name=currency_pair).delete()


def cleanupTasks(currency_pair):
    nb = Alert.objects.filter(currency_pair=currency_pair).count()
    if nb == 0:
        deleteTask(currency_pair)
