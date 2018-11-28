import sys
from abc import abstractmethod

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import (QAction, QApplication, QHBoxLayout, QLabel,
                             QLineEdit, QListWidget, QMainWindow, QMessageBox,
                             QPushButton, QVBoxLayout, QWidget)

from MainStream import *

'''
Game Main Code
'''

(agriculture, livestock, luxury, manufactured) = init()
News_List = ["News1", "New2", "New3"]  # 뉴스 목록
Day = 1


# functions


def getclass(name):
    if name in agriculture.productList:
        return agriculture
    if name in livestock.productList:
        return livestock
    if name in luxury.productList:
        return luxury
    if name in manufactured.productList:
        return manufactured


def place_in_layout(layout, details, arrange="spread"):
    """
    레이아웃과 담을 것들을 받아 배치합니다. (Stretch 이용)
    :parameter layout: 레이아웃입니다.
    :parameter details: 레이아웃에 담을 것들의 iterable 객체입니다.
    :parameter arrange: 배치 방식입니다. 
    :return: None
    :Exception: 담을 내용 오류/유효하지 않은 배치 방식
    """
    arrange = arrange.lower()  # 소문자화(비교를 위해)
    if arrange not in ("spread", "center", "front", "back", "wing_f", "wing_b", "dispersion"):  # 배치 방식이 다음 중 없으면?
        raise Exception("Invalid arrangement.")  # 예외 발생

    """
    spread: 고르게 분산
    center: 중심으로 쏠림
    front: 앞으로 쏠림 / back: 뒤로 쏠림
    wing_f, wing_b: 양쪽으로 갈라짐, 홀수 개 위젯일 때 가운데 것을 f는 앞에, b는 뒤에 붙임
    """
    # 이하는 크게 신경쓰지 않아도 됨(배치 방법에 따라 위젯 적절히 나열하기)
    if "wing" in arrange:
        l = len(details)//2
        is_odd = (len(details) % 2 == 1)
        for i in range(l):
            try:
                layout.addWidget(details[i])
            except Exception:
                layout.addLayout(details[i])
        if is_odd and "f" in arrange:
            try:
                layout.addWidget(details[l])
            except Exception:
                layout.addLayout(details[i])
        layout.addStretch(1)
        if is_odd and "b" in arrange:
            try:
                layout.addWidget(details[l])
            except Exception:
                layout.addLayout(details[l])
        for i in range(l):
            try:
                layout.addWidget(details[i+l+(1 if is_odd else 0)])
            except Exception:
                layout.addLayout(details[i+l+(1 if is_odd else 0)])
    else:
        if arrange in ("spread", "back", "center"):
            layout.addStretch(1)
        if not arrange == "dispersion":
            for w in details:
                try:
                    layout.addWidget(w)
                except Exception:
                    layout.addLayout(w)
                if arrange == "spread":
                    layout.addStretch(1)
            if arrange in ("front", "center"):
                layout.addStretch(1)
        else:
            for i in range(len(details)):
                w = details[i]
                try:
                    layout.addWidget(w)
                except Exception:
                    layout.addLayout(w)
                if i < len(details)-1:
                    layout.addStretch(1)

    return


def YN_question(window, question_name, question_str):
    """
    QMessagebox로 예/아니오를 물어봅니다.
    :parameter window: 어디 창에서 질문을 띄울 건지
    :parameter question_name: 질문 창 이름
    :parameter question_str: 질문 내용
    :return: bool타입의 대답(True: Yes, False: No)
    """
    ans = QMessageBox.question(window, question_name, question_str,
                               QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
    return (ans == QMessageBox.Yes)


# Classes


class Wind(QWidget):
    """
    창 클래스입니다. QWidget을 상속합니다.
    Wind 클래스를 만들면 창이 띄워집니다.
    """

    def __init__(self, name):
        """
        생성자입니다. 
        띄울 창의 이름을 결정하며, 끝날 때 setup을 호출합니다.
        :parameter name: 창의 이름입니다.
        """
        super().__init__()  # 상위 클래스의 생성자 호출
        self.name = name  # 창의 이름 정하기
        self.strong = False  # 되묻지 않고 닫을지에 대한 여부
        self.design()  # 디자인
        self.setup()  # 셋업

    # 디자인 메소드는 반드시 오버라이드해야 합니다. (추상 메소드)
    @abstractmethod
    def design(self):
        """
        창을 디자인합니다. 
        하는 일: 레이아웃, 버튼/텍스트 띄우기
        """
        pass

    def setup(self):
        """
        창을 세팅하고 띄웁니다.
        하는 일: 창의 제목 설정, 창 보이기, 창 위치/크기 설정
        """
        self.setWindowTitle(self.name)  # 창의 제목 지정
        self.show()  # 보이기

    def closeEvent(self, QCloseEvent):  # 창 닫기 이벤트(X자 누르거나 .close() 호출 시)
        if self.strong:  # 만약 되묻지 않기로 했다면?
            QCloseEvent.accept()  # 그냥 CloseEvent 수용
        else:  # 되묻기
            # 메시지박스로 물어보기(Y/N), 그 결과를 ans에 저장
            self.ans = YN_question(
                self, "Confirm", "Do you want to close this window?")
            if self.ans:
                QCloseEvent.accept()  # CloseEvent 수용
            else:
                QCloseEvent.ignore()  # CloseEvent 거절

    def strong_close(self, QCloseEvent):  # 강하게 닫기(물어봄 X)
        self.strong = True  # 안 되묻기로 한 뒤
        self.close()  # 닫는다(그냥 종료)


class Main_wind(Wind):
    """
    메인 윈도우입니다. Wind를 상속합니다.
    게임 플레이의 중추입니다.
    Main window에서 모든 부가 창으로 이동할 수 있습니다.
    """

    def design(self):
        # 상위 클래스로부터 오버라이드합니다.
        self.Products = QListWidget()  # 물품 목록
        self.showProducts()  # 물품 리스트 출력

        self.Products.setFixedSize(500, 400)  # 크기 고정
        self.Products.itemSelectionChanged.connect(self.selectionChanged_event)

        self.Info_text = Text("Your Money: {}\nDay: {}".format(
            money.money, Day), self)  # 잔고
        Bank_button = Link_button(
            "Bank", "Bank", self, Bank_Wind, "Bank")  # 은행
        Storage_button = Link_button(
            "Storage", "Storage", self, Storage_wind, "Storage")  # 창고용량

        self.item_info = QVBoxLayout()  # 물품 정보 및 매매
        self.item_name = Text("Select an item", self)  # 초기 텍스트1
        self.item_price = Text("from left.", self)  # 초기 텍스트2
        Buy_button = Basic_button("Buy", "Buy selected goods.", self)
        Sell_button = Basic_button("Sell", "Sell selected goods.", self)
        Buy_button.clicked.connect(self.buy_item)
        Sell_button.clicked.connect(self.sell_item)

        self.numCount = QLineEdit(self)
        self.numCount.setPlaceholderText("Insert quantity. (int)")
        place_in_layout(self.item_info, (self.item_name,
                                         self.item_price, Buy_button, self.numCount, Sell_button), "wing_b")

        News_button = Link_button(
            "News", "Show recent news.", self, News_wind, "News")  # 뉴스 버튼
        Next_day_button = Push_button("Sleep", "Next day", self)  # '다음 날' 버튼
        Next_day_button.clicked.connect(self.next_day)
        End_button = Quit_button(
            "Quit", "Changes will not be saved.", self)  # '끝내기' 버튼

        top_box = QHBoxLayout()  # 상부
        place_in_layout(top_box, (self.Info_text, Bank_button, Storage_button))

        mid_box = QHBoxLayout()  # 중간
        place_in_layout(mid_box, (self.Products, self.item_info))

        bottom_box = QHBoxLayout()  # 하부
        place_in_layout(
            bottom_box, (News_button, Next_day_button, End_button), "wing_b")

        vbox = QVBoxLayout()
        place_in_layout(vbox, (top_box, mid_box, bottom_box), arrange="spread")

        self.setLayout(vbox)

    def setup(self):
        self.move(100, 100)  # 위치
        self.setFixedSize(800, 600)  # 크기(고정)
        super().setup()

    def showProducts(self):
        self.Products.addItem("물품-----요금(τ)----유통기한(일)")
        self.Products.addItem("----------[농산물]-----------")
        for (name, [price, date]) in list(agriculture.productList.items()):
            self.Products.addItem(name+"\t"+str(price)+"\t"+str(date))
        self.Products.addItem("----------[축/수산물]-----------")
        for (name, [price, date]) in list(livestock.productList.items()):
            self.Products.addItem(name+"\t"+str(price)+"\t"+str(date))

        self.Products.addItem("----------[공산품]-----------")
        for (name, price) in list(manufactured.productList.items()):
            self.Products.addItem(name+"\t"+str(price))
        self.Products.addItem("----------[사치품]-----------")
        for (name, price) in list(luxury.productList.items()):
            self.Products.addItem(name+"\t"+str(price))

    def selectionChanged_event(self):
        k = str(self.Products.currentItem().text())
        if "-" in k:
            return
        k = k.split("\t")
        self.current_item_name = str(k[0].strip("\t"))
        self.current_item_price = str(int(k[1].strip("\t").replace("\t", "")))
        self.item_name.setText(self.current_item_name)
        self.item_price.setText(self.current_item_price)
        self.update()

    def buy_item(self):
        try:
            self.num = self.numCount.text()
            self.num = int(self.num)
            if self.num<=0:
                return
        except ValueError:
            return
        else:
            try:
                ans = YN_question(self, "Confirm", "Are you sure to buy?\nTotal Price: %d Tau" % (
                    self.num*int(self.current_item_price)))
            except AttributeError:
                return
            if ans:
                try:
                    if self.num<=0:
                        return
                    buy(self.current_item_name, getclass(
                        self.current_item_name), self.num)
                except AttributeError:
                    pass
                else:
                    self.Info_text.setText("Your Money: {}\nDay: {}".format(
                        money.money, Day))  # 잔고
                    self.update()
            else:
                pass

    def sell_item(self):
        try:
            self.num = self.numCount.text()
            self.num = int(self.num)
            if self.num<=0:
                return
        except ValueError:
            return
        else:
            try:
                ans = YN_question(self, "Confirm", "Are you sure to buy?\nTotal Price: %d Tau" % (
                    self.num*int(self.current_item_price)))
            except AttributeError:
                pass
            else:
                if ans:
                    sell(self.current_item_name, getclass(
                        self.current_item_name), self.num)
                    self.Info_text.setText("Your Money: {}\nDay: {}".format(
                        money.money, Day))  # 잔고
                    self.update()
                else:
                    pass

    def next_day(self):
        ans = YN_question(self, "Sleep confirm", "Sleep and move on next day.")
        if ans:
            global Day
            Day += 1
            sleep()
            self.Info_text.setText(
                "Your Money: {}\nDay: {}".format(money.money, Day))  # 잔고
            self.update()
        else:
            pass


class Intro_wind(Wind):
    """
    프로그램을 작동하자마자 뜨는 창입니다. Wind를 상속합니다.
    게임 시작/종료 버튼만 존재합니다. 게임 시작을 누르면 게임이 열리고, 게임 종료를 누르면 끝납니다.
    """

    def design(self):
        # 상위 클래스로부터 오버라이드합니다.
        _start_btn = Moveto_button(
            "Start", "Start game.", self, Main_wind, "Main")  # 게임 시작 버튼
        _start_hbox = QHBoxLayout()
        place_in_layout(_start_hbox, (_start_btn,), "center")
        _quit_btn = Quit_button("Quit", "Quit game.", self)  # 종료 버튼
        _quit_hbox = QHBoxLayout()
        place_in_layout(_quit_hbox, (_quit_btn,), "center")

        _vmid_box = QVBoxLayout()
        place_in_layout(_vmid_box, (_start_hbox, _quit_hbox))  # 버튼 수직 레이아웃

        self.setLayout(_vmid_box)  # 배치

    def setup(self):
        self.move(300, 300)  # 창 위치
        self.setFixedSize(200, 150)  # 창 크기(고정)
        super().setup()


class List_wind(Wind):
    """
    리스트와 닫기 버튼이 있는 창입니다. Wind를 상속합니다.
    """

    def design(self):
        # 상위 클래스로부터 오버라이드합니다.
        _vbox = QVBoxLayout()  # 수직 레이아웃
        self.List = QListWidget()  # 리스트
        _vbox.addWidget(self.List)  # 수직 레이아웃에 리스트 추가
        _hbox = QHBoxLayout()  # 수평 레이아웃
        place_in_layout(
            _hbox, (Close_button("Close", "Close this window.", self),), "center")  # 수평 레이아웃에 닫기 버튼 추가
        _vbox.addLayout(_hbox)  # 수직 레이아웃에 수평 레이아웃 추가
        self.setLayout(_vbox)  # 수직 레이아웃 배치

    def setup(self):
        self.setFixedSize(600, 400)  # 창 크기 고정
        super().setup()


class Bank_Wind(List_wind):
    """
    버튼으로 메뉴를 만들어둔 창입니다. List_wind를 상속합니다.
    """

    def design(self):
        # 상위 클래스로부터 오버라이드합니다.
        _vbox = QVBoxLayout()
        _hbox_1 = QHBoxLayout()
        self.buttons = QVBoxLayout()
        _hbox_2 = QHBoxLayout()

        self.button1 = Push_button("Save", "Save", self)
        self.button2 = Push_button("Loan", "Loan", self)
        self.button3 = Push_button("????", "????", self)
        place_in_layout(self.buttons, (self.button1,
                                       self.button2, self.button3))

        self.List = QListWidget()
        _hbox_1.addWidget(self.List)
        _hbox_1.addLayout(self.buttons)

        place_in_layout(
            _hbox_2, (Close_button("Close", "Close this window.", self),), "center")
        _vbox.addLayout(_hbox_1)
        _vbox.addLayout(_hbox_2)

        self.setLayout(_vbox)


class News_wind(List_wind):
    """
    뉴스를 띄우는 창입니다. List_Wind를 상속합니다. 
    """

    def design(self):
        # 상위 클래스로부터 오버라이드합니다.
        super().design()
        global News_List
        for i in News_List:
            self.List.addItem(i)


class Storage_wind(List_wind):
    """
    창고를 띄우는 창입니다. List_wind를 상속합니다.
    """

    def design(self):
        # status()
        # 상위 클래스로부터 오버라이드합니다.
        super().design()
        self.List.addItem('이름:\t수량:\t유통기한:')
        self.List.addItem('-'*40)
        for (name, data) in list(storage.warehouse.items()):
            if not isinstance(getclass(name), ExpireProduct):
                # print(name, data)
                self.List.addItem(name + '\t' + str(data))
        for (name, datelist) in list(storage.warehouse_expire.items()):
            for [number, date] in datelist:
                self.List.addItem(name + '\t' + str(number) + '\t' + str(date))


class Push_button(QPushButton):
    """
    버튼 클래스입니다. QPushButton을 상속합니다.
    """

    def __init__(self, name, tooltip, window):
        """
        생성자입니다. __init__이 끝날 때 utility_set을 호출합니다.
        :parameter name: 버튼의 이름(내용)입니다.
        :parameter tooltip: 버튼의 툴팁입니다. (마우스 올리면 나오는 내용)
        """
        super().__init__(name, window)  # 상위 클래스의 생성자 호출
        self.design(tooltip)  # 디자인하기
        self.utility_set(window)  # 기능 설정

    def design(self, tooltip):
        """
        버튼을 디자인합니다.
        하는 일: 버튼 툴팁 설정, 위치/크기 조정
        :parameter tooltip: 버튼 툴팁(마우스 올리면 나타나는 거)입니다.
        """
        self.setToolTip(tooltip)  # 툴팁 설정
        self.setFixedSize(self.sizeHint())  # 글씨에 따라 버튼 크기 조정

    # utility_set은 반드시 오버라이드해야 함
    @abstractmethod
    def utility_set(self, window):
        pass


class Basic_button(Push_button):
    """
    아무 기능이 없는 버튼 클래스입니다. Push_button을 상속합니다. 
    """

    def utility_set(self, window):
        pass


class Link_button(Push_button):
    """
    눌리면 새 창을 띄우는 버튼 클래스입니다. Push_button을 상속합니다.
    """

    def __init__(self, name, tooltip, window, link_class, link_name):
        """
        상위 클래스로부터 오버라이드합니다.
        :parameter link_class: 띄울 창의 클래스입니다.
        :parameter link_name: 띄울 창의 정보입니다. (이름)
        """
        self.linkage_info = (link_class, link_name)  # 띄울 창의 정보를 튜플로 만들기
        super().__init__(name, tooltip, window)  # 상위 클래스의 생성자 호출

    def utility_set(self, window):
        # 상위 클래스로부터 오버라이드합니다.
        # try except 제거 시 2번 클릭됨
        # https://stackoverflow.com/questions/46747317/when-a-qpushbutton-is-clicked-it-fires-twice
        try:
            self.clicked.disconnect()
        except Exception:
            pass
        self.clicked.connect(self.open_new_window)

    def open_new_window(self):
        """
        새 창을 여는 메소드입니다.
        """
        self.link = self.linkage_info[0](self.linkage_info[1])


class Moveto_button(Link_button):
    """
    눌리면 다른 창으로 이동하는 버튼 클래스입니다. Link_button을 상속합니다.
    """

    def __init__(self, name, tooltip, window, link_class, link_name):
        # 상위 클래스로부터 오버라이드합니다.
        self.window = window  # 지금 창!
        super().__init__(name, tooltip, window, link_class, link_name)  # 상위 클래스의 생성자 호출

    def open_new_window(self):
        # 상위 메소드로부터 오버라이드합니다.
        super().open_new_window()
        self.window.strong_close(QCloseEvent)


class Close_button(Push_button):
    """
    창을 닫을 때 쓰는 버튼 클래스입니다. Push_button을 상속합니다. 
    """

    def utility_set(self, window):
        # 상위 클래스로부터 오버라이드합니다.
        self.clicked.connect(window.strong_close)  # 호출하는 window를 닫습니다. (강하게)


class Quit_button(Close_button):
    """
    프로그램을 종료할 때 버튼 클래스입니다. Close_button을 상속합니다. 
    """

    def utility_set(self, window):
        # 상위 클래스로부터 오버라이드합니다.
        self.clicked.connect(
            QCoreApplication.instance().quit)  # 버튼을 누르면 다 종료되도록


class Text(QLabel):
    """
    텍스트입니다. QLabel을 상속합니다.
    """

    def __init__(self, text, window):
        """
        생성자입니다. 끝날 때 setup을 호출합니다. 
        :parameter text: 나타낼 텍스트
        :parameter window: 텍스트를 띄울 창
        """
        super().__init__(text, window)  # 상위 클래스의 생성자 호출

    def setup(self):
        # 텍스트를 세팅하고 띄웁니다. 크기는 글자에 맞추어 고정됩니다.
        self.setFixedSize(self.sizeHint())  # 크기 설정
        self.show()


def game_start():
    app = QApplication(sys.argv)  # application 객체 생성하기 위해 시스템 인수 넘김
    intro = Intro_wind("Intro")
    sys.exit(app.exec_())  # 이벤트 처리를 위한 루프 실행(메인 루프), 루프가 끝나면 프로그램도 종료


game_start()
