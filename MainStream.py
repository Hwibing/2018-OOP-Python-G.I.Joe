from MainClass import *
from Ctrl import *


def buy(name, cls, number):
    if money.buy(name, cls, number):
        if storage.buy(name, cls, number):
            return True
        else:
            return False
    else:
        return False


def sell(name, cls, number):
    if storage.sell(name, number):
        if money.sell(name, cls, number):
            return True
        else:
            return False
    else:
        return False

def status():
    print('money : {}'.format(money.money))
    storage.printstorage()


# Initialize Game
(agriculture, livestock, luxury, manufactured) = init()
money = Finance(500000)
storage = Storage(100)



