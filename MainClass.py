if __name__ == '__main__':
    print("HELLO WORLD :: BASE_CLASS MODULE")


# Define Class
class Product:
    productList = {}

    def append(self, name, price):
        self.productList[name] = price

    def printlist(self):
        print(self.productList)


class ExpireProduct(Product):

    def append(self, name, price, expire):
        self.productList[name] = [price, expire]
    pass


class AgricultureProduct(ExpireProduct):
    pass


class LivestockProduct(ExpireProduct):
    pass


class LuxuryProduct(Product):
    pass


class ManufacturedProduct(Product):
    pass

