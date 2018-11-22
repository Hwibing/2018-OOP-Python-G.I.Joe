'''
import MainClass


a = MainClass.Product('agriculture')


def myf(cls):
    if isinstance(cls,MainClass.ExpireProduct):
        #print('yes')
    #print(type(cls))



myf(a)

s = ['18\n']
print(int(s))


def myf(percent, *args):
    print('percent')
    print(percent)
    for i in args:
        print(i)


myf(10, 'n1','n2','n3')
'''

import random
import Ctrl

(agriculture, livestock, luxury, manufactured) = Ctrl.init()
luxury.printlist()
pl = list(luxury.productList.keys())
random.shuffle(pl)
print(pl)
luxury.update(100, pl[0:2])
luxury.printlist()



