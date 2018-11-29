import MainClass

def readprice(myclass, filename):

    #print(type(myclass))
    #print(myclass)

    f = open("./prices/" + filename, 'r', encoding="UTF-8")
    while True:
        newline = f.readline()
        if not newline:
            break
        try:
            newline = newline.split(' ')
            name = newline[0]
            price = int(str(newline[1]).split('/')[0])
            if isinstance(myclass, MainClass.ExpireProduct):
                expired = int(str(newline[2]).split('d')[0])
                myclass.append(name, price, expired)
            else: myclass.append(name, price)
        except IndexError as e:
            continue


def readnews():
    # READ NORMAL NEWS
    news_normal = []
    f = open('./news/news_normal', 'r', encoding="UTF-8")
    while True:
        newline = f.readline()
        if not newline:
            break
        news_normal.append([newline.split('/')[0], int(newline.split('/')[1])])

    # READ DISASTER NEWS
    news_disaster = {}
    news_agri = []
    f = open('./news/news_agri', 'r', encoding="UTF-8")
    while True:
        newline = f.readline()
        if not newline:
            break
        news_agri.append([newline.split('/')[0], int(newline.split('/')[1])])

    news_agri_live = []
    f = open('./news/news_agri+live', 'r', encoding="UTF-8")
    while True:
        newline = f.readline()
        if not newline:
            break
        news_agri_live.append([newline.split('/')[0], int(newline.split('/')[1])])

    news_event = []
    f = open('./news/news_event', 'r', encoding="UTF-8")
    while True:
        newline = f.readline()
        if not newline:
            break
        news_event.append([newline.split('/')[0], int(newline.split('/')[1])])

    news_live = []
    f = open('./news/news_live', 'r', encoding="UTF-8")
    while True:
        newline = f.readline()
        if not newline:
            break
        news_live.append([newline.split('/')[0], int(newline.split('/')[1])])

    news_manu = []
    f = open('./news/news_manu', 'r', encoding="UTF-8")
    while True:
        newline = f.readline()
        if not newline:
            break
        news_manu.append([newline.split('/')[0], int(newline.split('/')[1])])

    news_disaster['a'] = news_agri
    news_disaster['al'] = news_agri_live
    news_disaster['e'] = news_event
    news_disaster['l'] = news_live
    news_disaster['m'] = news_manu

    return (news_normal, news_disaster)


def readinfo():
    f = open('./info/info_global', 'r', encoding="UTF-8")
    info_global = []
    while True:
        newline = f.readline()
        if not newline:
            break
        info_global.append([newline.split('/')[0], int(newline.split('/')[1])])

    f = open('./info/info_specific', 'r', encoding="UTF-8")
    info_specific = []
    while True:
        newline = f.readline()
        if not newline:
            break
        info_specific.append([newline.split('/')[0], int(newline.split('/')[1])])

    '''
    print(info_global)
    print(info_specific)
    '''

    return (info_global, info_specific)


def init():
    cls = []
    agriculture = MainClass.ExpireProduct('agriculture')
    cls.append(agriculture)
    livestock = MainClass.ExpireProduct('livestock')
    cls.append(livestock)
    luxury = MainClass.Product('luxury')
    cls.append(luxury)
    manufactured = MainClass.Product('manufactured')
    cls.append(manufactured)

    for c in cls:
        readprice(c, 'prices_'+str(c.type))
        #c.printlist()

    return tuple(cls)
