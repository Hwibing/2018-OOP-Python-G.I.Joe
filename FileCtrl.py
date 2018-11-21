

import MainClass

'''
 initialize product prices by file
 returns pricelist
'''
def init_price():

    # name of price files
    files = ['prices_agriculture', 'prices_livestock', 'prices_luxury', 'prices_manufactured']

    default_expire_date = 7

    products = {}

    for f_name in files:

        type = f_name.split('_')[1]
        pricelist = []

        f_name = "./prices/" + f_name
        f = open(f_name, 'r')
        while True:
            newline = f.readline()
            if not newline:
                break

            try:
                newline = newline.split(' ')
                name = newline[0]
                price = str(newline[1]).split('/')[0]

            except IndexError as e:
                continue

            if type == 'agriculture':
                new = MainClass.Agriculture_Product(name, price, default_expire_date)
                pricelist.append(new)

            elif type == 'livestock':
                new = MainClass.Livestock_Product(name, price, default_expire_date)
                pricelist.append(new)

            elif type == 'luxury':
                new = MainClass.Agriculture_Product(name, price, default_expire_date)
                pricelist.append(new)
            elif type == 'agriculture':
                new = MainClass.Agriculture_Product(name, price, default_expire_date)
                pricelist.append(new)

            if __name__ == '__main__':
                print(type, name, price)

        f.close()

        products[type] = pricelist

    return products

print(init_price())
