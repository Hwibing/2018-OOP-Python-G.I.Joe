if __name__ == '__main__':
    print("HELLO WORLD :: BASE_CLASS MODULE")


# Define Class

class GameSettings:
    def __init__(self, money):
        self.money = money


class Storage:
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.quantity = 0
        self.warehouse = {}
        self.warehouse_expire = {}

    def overflow(self, add):
        if self.quantity + add > self.maxsize: return True
        else: return False

    def buy(self, name, product, number):
        if not self.overflow(number):
            self.quantity += number
            if isinstance(product, ExpireProduct):
                if name not in self.warehouse_expire:
                    self.warehouse_expire[name] = [[number, product.productList[name][1]]]
                else:
                    if self.warehouse_expire[name][0][1] == product.productList[name][1]:
                        self.warehouse_expire[name][0][0] += number
                    else:
                        self.warehouse_expire[name].append([number, product.productList[name][1]])

            if name not in self.warehouse:
                self.warehouse[name] = 0
            self.warehouse[name] += number

        else:
            print('Error: STORAGE OVERFLOW')
            return -1

        self.printstorage()
        return 0

    def sell(self, name, number):
        if name not in self.warehouse:
            print('Error: NOT ENOUGH ITEMS')
            return -1
        else:
            if self.warehouse[name] >= number:
                self.warehouse[name] -= number
                self.quantity -= number
                if self.warehouse[name] == 0:
                    del self.warehouse[name]
            else:
                print('Error: NOT ENOUGH ITEMS')
                return -1

        if name in self.warehouse_expire:
            for [count, expire] in self.warehouse_expire[name]:
                self.warehouse_expire[name].remove([count, expire])
                if count > number:
                    self.warehouse_expire[name].append([count-number, expire])
                    break
                else: number -= count
        return 0

    def nextday(self, dec=1):
        for name in list(self.warehouse_expire.keys()):
            for idx in range(len(self.warehouse_expire)): # size of list
                self.warehouse_expire[name][idx][1] -= dec
                if self.warehouse_expire[name][idx][1] <= 0:
                    self.warehouse_expire[name].remove([self.warehouse_expire[name][idx][0], self.warehouse_expire[name][idx][1]])
                    self.quantity -= self.warehouse_expire[name][idx][0]





    def printstorage(self):
        print(self.warehouse)
        print(self.warehouse_expire)
        print()





class Product:
    def __init__(self, type):
        self.type = type
        self.productList = {}

    def append(self, name, price):
        self.productList[name] = price

    def printlist(self):
        print(self.productList)

    def update(self, percent, products):
        for name in products:
            #print(name)
            #print(self.productList[name])
            self.productList[name] = int(self.productList[name]*(percent/100+1))

# idx 0 --> price idx 1 --> expire
class ExpireProduct(Product):

    def append(self, name, price, expire):
        self.productList[name] = [price, expire]

    def update(self, percent, products):
        for name in products:
            self.productList[name] = [int(self.productList[name][0] * (percent / 100 + 1)), self.productList[name][1]]