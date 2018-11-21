if __name__ == '__main__':
    print("HELLO WORLD :: BASE_CLASS MODULE")


# Define Class
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def print_price(self):
        print(self.price)


class Expire_Product(Product):
    def __init__(self, name, price, expire):
        super().__init__(name, price)
        self.expire = expire
        #print(self.name,self.expire,self.price)

class Agriculture_Product(Expire_Product):
    pass


class Livestock_Product(Expire_Product):
    pass


class Luxury_Product(Product):
    pass


class Manufactured_Product(Product):
    pass



