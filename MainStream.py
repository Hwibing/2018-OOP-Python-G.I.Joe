from MainClass import *
from Ctrl import *
import random


# Initialize Game
def gamerestart():
    global agriculture, livestock, luxury, manufactured, allproduct, news_normal, news_disaster, info_global, info_specific, Next_Update, News_List, Day, money, storage, Info_Cost
    (agriculture, livestock, luxury, manufactured) = init()
    allproduct = [agriculture, livestock, luxury, manufactured]
    (news_normal, news_disaster) = readnews()
    (info_global, info_specific) = readinfo()
    Next_Update = []
    News_List = []
    Day = 1
    money = Finance(500000)
    storage = Storage(100)
    Info_Cost = 25000

gamerestart()


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
        names += list(i.productList.keys())

    random.shuffle(names)
    names = names[:number]
    return names


def pick_news(newstype, normal_number=10):
    randnews = []
    for i in range(normal_number):
        random.shuffle(newstype)
        randnews += [newstype[0]]
    '''
    if random.randint(1, 10) == 1:
        random.shuffle(news_disaster)
        randnews = randnews + news_disaster[0]
    '''
    return randnews


def getclass(name):
    name = str(name)
    global agriculture, livestock, luxury, manufactured
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
    global News_List
    News_List.clear()

    randnews = pick_news(news_normal)
    for [news, rate] in randnews:
        name = pick_random(allproduct)
        cls = getclass(name[0])
        cls.update(rate, name)
        News_List.append(news.replace('(?)', name[0]))

    if random.randint(1, 10) <= 1:  # 10% 확률로 disaster event 발생
        disastertypes = list(news_disaster.keys())
        random.shuffle(disastertypes)
        news_type = disastertypes[0]


        randnews = pick_news(news_disaster[news_type], 1)
        randnews = randnews[0]

        if news_type == 'a':
            News_List.append(randnews[0])
            agriculture.update(randnews[1], list(agriculture.productList.keys()))

        if news_type == 'al':
            News_List.append(randnews[0])
            agriculture.update(randnews[1], list(agriculture.productList.keys()))
            livestock.update(randnews[1], list(livestock.productList.keys()))

        if news_type == 'e':
            name = pick_random(allproduct)
            cls = getclass(name[0])
            cls.update(randnews[1], name)
            News_List.append(randnews[0].replace('(?)', name[0]))

        if news_type == 'l':
            News_List.append(randnews[0])
            livestock.update(randnews[1], list(livestock.productList.keys()))

        if news_type == 'm':
            News_List.append(randnews[0])
            manufactured.update(randnews[1], list(manufactured.productList.keys()))

    # UPDATE INFO PRICES
    for [rate, products] in Next_Update:
        cls = getclass(products[0])
        cls.update(rate, products)
    
    # Random Bad Event
    thief_event=(random.randint(1,100)<=1)
    if thief_event:
        money.money=0
    return (thief_event,)


def getinfo():
    if random.randint(1,10) >= 2:
        newinfo = pick_news(info_specific, 1)
        newinfo = newinfo[0]
        name = pick_random(allproduct)
        Next_Update.append([newinfo[1], name])
        return newinfo[0].replace('(?)', name[0])
    else:
        newinfo = pick_news(info_global, 1)
        newinfo = newinfo[0]
        Next_Update.append([newinfo[1], list(agriculture.productList.keys())])
        Next_Update.append([newinfo[1], list(livestock.productList.keys())])
        Next_Update.append([newinfo[1], list(luxury.productList.keys())])
        Next_Update.append([newinfo[1], list(manufactured.productList.keys())])
        return newinfo[0]






# Usage notes FROM here
if __name__=="__main__":
    '''
    agriculture.printproductlist()
    buy('감자', agriculture, 10)
    sell('감자', agriculture, 10)
    sleep()
    status()
    '''