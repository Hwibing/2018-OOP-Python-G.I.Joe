from MainClass import *
from Ctrl import *
import random

# Initialize Game
(agriculture, livestock, luxury, manufactured) = init()
allproduct = [agriculture, livestock, luxury, manufactured]
(news_normal, news_disaster) = readnews()
News_List = []
Day = 1
money = Finance(500000)
storage = Storage(100)


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


def pick_news(normal_number=10):
    randnews = []
    for i in range(normal_number):
        random.shuffle(news_normal)
        randnews += news_normal[0]
    '''
    if random.randint(1, 10) == 1:
        random.shuffle(news_disaster)
        randnews = randnews + news_disaster[0]
    '''
    return randnews


def getclass(name):
    if name in agriculture.productList:
        return agriculture
    if name in livestock.productList:
        return livestock
    if name in luxury.productList:
        return luxury
    if name in manufactured.productList:
        return manufactured


def sleep():
    money.nextday()
    storage.nextday()
    News_List = []
    randnews = pick_news()
    for [news, rate] in randnews:
        name = pick_random(allproduct)
        cls = getclass(name)
        cls.update(rate, name)
        News_List.append(news.replace('(?)',name))


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