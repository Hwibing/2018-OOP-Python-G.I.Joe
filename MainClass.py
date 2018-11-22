if __name__ == '__main__':
    print("HELLO WORLD :: BASE_CLASS MODULE")


# Define Class

class Settings:
    def __init__(self, money):
        self.money = money

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
            print(name)
            print(self.productList[name])
            self.productList[name] = int(self.productList[name]*(percent/100+1))


# idx 0 --> price idx 1 --> expire
class ExpireProduct(Product):

    def append(self, name, price, expire):
        self.productList[name] = [price, expire]

