if __name__ == '__main__':
    print("MainClass")


class GameSettings:
    pass


class Finance:
    def __init__(self, money):
        self.money = money
        self.loan = 0
        self.bank = 0
        pass

class Storage:
    """
    사고팔 수 있는 게임 속 아이템들을 저장할 수 있는 창고 클래스입니다.
    __init__ : 클래스를 정의할 때 창고의 최대크기를 지정합니다.
    overflow : 창고에 추가할 아이템의 개수를 매개변수로 넘겼을 때 창고가 넘치면 True 그렇지 않다면 False를 반환합니다
    buy : 아이템의 이름, 아이템의 클래스, 개수를 매개변수로 넘기면 창고에 추가
        성공시 0 return, 실패시 -1 return
        (만약 해당 아이템을 추가할 시 창고에 overflow 가 발생할 경우 실패 -> returns -1)
    sell : 아이템의 이름, 개수를 매개변수로 넘기면 창고에서 해당 아이템을 개수만큼 삭제
        (유통기한이 있는 경우 유통기한이 적게 남은 것 부터 삭제)
    nextday : 감소되는 유통기한인 정수 (DEFAULT = 1)를 입력해주면 해당 창고에 존재하는 유통기한이 존재하는 물품들의 유통기한을 입력값 만큼 줄임
        ++  self.freezer 가 True 로 설정될 경우 (DEFAULT = FALSE) 입력값에 관계없이 무조건 유통기한 하루씩 감소 (냉장고 기능 구현)
    """

    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.quantity = 0
        self.warehouse = {}
        self.warehouse_expire = {}
        self.freezer = False

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
        if self.freezer: dec = 1
        for name in list(self.warehouse_expire.keys()):
            for idx in range(len(self.warehouse_expire)): # size of list
                self.warehouse_expire[name][idx][1] -= dec
                if self.warehouse_expire[name][idx][1] <= 0:
                    self.quantity -= self.warehouse_expire[name][idx][0]
                    self.warehouse[name] -= self.warehouse_expire[name][idx][0]
                    self.warehouse_expire[name].remove([self.warehouse_expire[name][idx][0], self.warehouse_expire[name][idx][1]])
            if self.warehouse[name] == 0:
                del self.warehouse_expire[name]
                del self.warehouse[name]


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