from MainClass import *
from Ctrl import *


def buy(name, cls, number):
    if storage.quantity + number <= storage.maxsize:
        if money.buy(name, cls, number):
            if storage.buy(name, cls, number):
                return True
            else:
                return False
        else:
            return False
    else:
        print('Storage Overflow')
        return False


def sell(name, cls, number):
    if storage.sell(name, number):
        if money.sell(name, cls, number):
            return True
        else:
            return False
    else:
        return False


def sleep():
    money.nextday()
    storage.nextday()


def status():
    print('money : {}'.format(money.money))
    storage.printstorage()


# Initialize Game
(agriculture, livestock, luxury, manufactured) = init()
money = Finance(500000)
storage = Storage(100)
agriculture.printproductlist()

# Usage notes FROM here
if __name__=="__main__":
    buy('감자', agriculture, 10)
    sell('감자', agriculture, 10)
    sleep()
    status()