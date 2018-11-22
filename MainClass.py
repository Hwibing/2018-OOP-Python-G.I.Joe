if __name__ == '__main__':
    print("HELLO WORLD :: BASE_CLASS MODULE")


# Define Class
class Product:
    def __init__(self, type):
        self.type = type
        self.productList = {}

    def append(self, name, price):
        self.productList[name] = price

    def printlist(self):
        print(self.productList)


# idx 0 --> price idx 1 --> expire
class ExpireProduct(Product):

    def append(self, name, price, expire):
        self.productList[name] = [price, expire]

