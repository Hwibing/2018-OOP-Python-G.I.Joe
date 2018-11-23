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

import MainClass

s = MainClass.Storage(10)
s.buy('감자', agriculture, 1)
s.buy('감자', agriculture, 2)
s.buy('감자', agriculture, 3)
s.buy('시계', luxury, 1)



