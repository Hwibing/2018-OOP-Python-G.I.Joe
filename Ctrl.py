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


