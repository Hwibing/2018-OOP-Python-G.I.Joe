from MainClass import *
from Ctrl import *
import random


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


def pick_random(classlist, number=1):
    names = []
    for i in classlist:
        names + list(i.productList.keys())

    random.shuffle(names)
    names = names[:number]
    return names

'''
def pick_news(normal_number=10):
    random.shuffle(news_normal)
    randnews = news_normal[:normal_number]
    if random.randint(1, 10) == 1:
        random.shuffle(news_disaster)
        randnews = randnews + news_disaster[0]
    return randnews
'''

# Initialize Game
(agriculture, livestock, luxury, manufactured) = init()
#(news_normal, news_disaster) = readnews()
News_List = []
Day = 1
money = Finance(500000)
storage = Storage(100)

# Usage notes FROM here
if __name__=="__main__":
    '''
    agriculture.printproductlist()
    buy('감자', agriculture, 10)
    sell('감자', agriculture, 10)
    sleep()
    status()
    '''
    print(pick_news())