import sys
from abc import abstractmethod

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QCloseEvent, QIcon, QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QHBoxLayout, QLabel,
                             QLineEdit, QListWidget, QMainWindow, QMessageBox,
                             QPushButton, QVBoxLayout, QWidget)

from MainStream import *


opened_window_list = dict()  # 열려 있는 창들을 모아 놓은 딕셔너리


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
        opened_window_list[name] = self
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
        하는 일: 레이아웃, 버튼/텍스트 띄우기, 크기 결정
        """
        self.x_loc = 100
        self.y_loc = 100
        self.width = 800
        self.height = 600

    def setup(self):
        """
        창을 세팅하고 띄웁니다.
        하는 일: 창의 제목 설정, 창 보이기, 창 위치/크기 설정
        """
        self.setWindowTitle(self.name)  # 창의 제목 지정
        self.move(self.x_loc, self.y_loc)  # 창의 위치
        self.setFixedSize(self.width, self.height)  # 창의 크기
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

    def strong_close(self, QCloseEvent=None):  # 강하게 닫기(물어봄 X)
        self.strong = True  # 안 되묻기로 한 뒤
        self.close()  # 닫는다(그냥 종료)

    def refresh(self):
        """
        새로고침입니다. refresh가 호출되면 창의 정보를 다시 불러옵니다. 
        """
        self.update()


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
        self.Products.itemSelectionChanged.connect(
            self.selectionChanged_event)  # 선택 아이템이 바뀌었을 때

        self.Info_text = Text("Your Money: {}\nDay: {}".format(
            money.money, Day), self)  # 잔고
        Bank_button = Link_button(
            "Bank", "Bank", self, Bank_Wind, "Bank", self)  # 은행
        Storage_button = Link_button(
            "Storage", "Storage", self, Storage_wind, "Storage")  # 창고용량

        self.item_deal = QVBoxLayout()  # 물품 정보 및 매매
        self.item_name = Text("Select an item", self)  # 초기 텍스트1
        self.item_price = Text("from left.", self)  # 초기 텍스트2
        self.ProductImageLabel = QLabel(self)

        self.Buy_button = Basic_button(
            "Buy", "Buy selected goods.", self)  # 구입 버튼
        self.Sell_button = Basic_button(
            "Sell", "Sell selected goods.", self)  # 판매 버튼
        # 각각의 버튼에 기능 연결
        self.Buy_button.clicked.connect(self.buy_item)
        self.Sell_button.clicked.connect(self.sell_item)

        self.numCount = QLineEdit(self)  # 개수 입력하는 부분
        self.numCount.setPlaceholderText("Insert quantity(Natural)")  # 힌트 메시지
        place_in_layout(self.item_deal, (self.item_name,
                                         self.item_price, self.ProductImageLabel, self.Buy_button, self.numCount, self.Sell_button))

        self.News_button = Link_button(
            "News", "Show recent news.", self, News_wind, "News")  # 뉴스 버튼
        self.Predict_button = Link_button(
            "Predict", "Show predictions.", self, Predict_wind, "Predict", self)  # 뉴스 버튼

        Next_day_button = Basic_button("Sleep", "Next day", self)  # '다음 날' 버튼
        Next_day_button.clicked.connect(self.next_day)
        End_button = Quit_button(
            "Quit", "Changes will not be saved.", self)  # '끝내기' 버튼

        top_box = QHBoxLayout()  # 상부
        place_in_layout(top_box, (self.Info_text, Bank_button, Storage_button))

        mid_box = QHBoxLayout()  # 중간
        place_in_layout(mid_box, (self.Products, self.item_deal))

        bottom_box = QHBoxLayout()  # 하부
        place_in_layout(
            bottom_box, (self.News_button, self.Predict_button, Next_day_button, End_button), "wing_b")

        vbox = QVBoxLayout()  # 전체 레이아웃
        place_in_layout(vbox, (top_box, mid_box, bottom_box), arrange="spread")

        # 창의 위치, 크기
        self.x_loc = 150
        self.y_loc = 150
        self.width = 800
        self.height = 600
        self.setLayout(vbox)

    def showProducts(self):
        self.Products.clear()
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
        """
        리스트(물건 목록)에서 선택한 아이템이 바뀌었을 때 호출됩니다.
        하는 일: 텍스트 바꾸기, 이미지 바꾸기, 현 아이템 바꾸기
        """
        k = str(self.Products.currentItem().text())
        if "-" in k:
            return
        k = k.split("\t")

        self.current_item_name = str(k[0].strip("\t"))  # 아이템 이름
        self.current_item_price = str(
            int(k[1].strip("\t").replace("\t", "")))  # 아이템 가격
        self.item_name.setText(self.current_item_name)  # 이름을 띄우고
        self.item_price.setText(self.current_item_price)  # 가격도 띄우고

        self.item_class = getclass(self.current_item_name).type  # 물건의 클래스를 받아
        self.Image = QPixmap(
            "images/{}.png".format(self.item_class))  # 사진을 따온 뒤
        self.ProductImageLabel.setPixmap(self.Image)  # 사진을 바꿔준다

        self.update()  # 새로고침

    def buy_item(self):
        try:
            self.num = self.numCount.text()  # 입력한 텍스트를 받아와
            self.num = int(self.num)  # 정수화하는데
            if self.num <= 0:  # 0보다 작으면 리턴
                return
        except ValueError:  # 유효하지 않아도
            return  # 리턴
        else:
            try:
                ans = YN_question(self, "Confirm", "Are you sure to buy?\nTotal Price: %d Tau" % (
                    self.num*int(self.current_item_price)))  # ㄹㅇ 살거임?
            except AttributeError:  # 선택을 안했다면(current 생성 X)
                return  # 리턴
            if ans:  # 넹
                buy(self.current_item_name, getclass(
                    self.current_item_name), self.num)  # 그럼 사세요
                self.Info_text.setText("Your Money: {}\nDay: {}".format(
                    money.money, Day))  # 텍스트 업데이트
                self.update()  # 새로고침
            else:  # 아녀
                pass  # 지나가세요

    def sell_item(self):
        try:
            self.num = self.numCount.text()
            self.num = int(self.num)
            if self.num <= 0:
                return
        except ValueError:
            return
        else:
            ans = YN_question(self, "Confirm", "Are you sure to buy?\nTotal Price: %d Tau" % (
                self.num*int(self.current_item_price)))
            if ans:
                sell(self.current_item_name, getclass(
                    self.current_item_name), self.num)
                self.Info_text.setText("Your Money: {}\nDay: {}".format(
                    money.money, Day))  # 잔고
                self.update()
            else:
                pass

    def next_day(self):
        ans = YN_question(self, "Sleep confirm",
                          "Sleep and move on next day.")  # "주무시게요?"
        if ans:  # 넹
            global Day
            Day += 1  # 하루 더하기
            sleep()  # 잠자기
            self.Info_text.setText(
                "Your Money: {}\nDay: {}".format(money.money, Day))  # 텍스트 재설정
            self.refresh()  # 다시 창 띄우기
            if money.money < 0:
                QMessageBox().about(self, "Bankrupt", "You are bankrupt!")
                Quit_button.click()
            self.window_will_be_closed=opened_window_list.items()
            for (window_name, window_object) in self.window_will_be_closed:  # 지금까지 열려 있는 창 닫기(main 제외)
                if not isinstance(window_object,Main_wind):
                    window_object.strong_close()  # 닫는당
            opened_window_list.clear()  # 딕셔너리를 비우고
            opened_window_list[self.name] = self  # 자신을 넣는다
            self.News_button.click()  # 뉴스 띄우기
        else:  # 아녀
            pass  # 그럼 나중에 뵈요!

    def refresh(self):
        # 상위 클래스로부터 오버라이드합니다.
        self.Info_text.setText("Your Money: {}\nDay: {}".format(
            money.money, Day))  # 텍스트 다시 세팅
        self.showProducts()  # 사진 다시 띄우기, 리스트 다시 그거.
        super().refresh()  # 상위 클래스의 refresh 불러옴


class Intro_wind(Wind):
    """
    프로그램을 작동하자마자 뜨는 창입니다. Wind를 상속합니다.
    게임 시작/종료 버튼만 존재합니다. 게임 시작을 누르면 게임이 열리고, 게임 종료를 누르면 끝납니다.
    """

    def design(self):
        # 상위 클래스로부터 오버라이드합니다.
        self._start_btn = Moveto_button(
            "Start", "Start game.", self, Main_wind, "Main")  # 게임 시작 버튼
        self._start_hbox = QHBoxLayout()
        place_in_layout(self._start_hbox, (self._start_btn,), "center")
        self._quit_btn = Quit_button("Quit", "Quit game.", self)  # 종료 버튼
        self._quit_hbox = QHBoxLayout()
        place_in_layout(self._quit_hbox, (self._quit_btn,), "center")

        self._vmid_box = QVBoxLayout()
        place_in_layout(self._vmid_box, (self._start_hbox,
                                         self._quit_hbox))  # 버튼 수직 레이아웃

        self.setLayout(self._vmid_box)  # 배치

        # 창의 위치, 크기
        self.x_loc = 300
        self.y_loc = 300
        self.width = 200
        self.height = 150


class Popup_wind(Wind):
    """
    팝업으로 뜨는 창들입니다. 원래 창에 대한 정보를 가지고 있습니다.
    끌 때 꼭꼭!!! origin을 refresh하도록!!
    """

    def __init__(self, name, origin):
        """
        상위 클래스로부터 오버라이드합니다.
        :parameter origin: 원래 창입니다. 
        """
        self.origin = origin
        super().__init__(name)


class Bank_Wind(Popup_wind):
    """
    은행 업무를 맡는 창입니다. List_wind를 상속합니다.
    """

    def design(self):
        # 상위 클래스로부터 오버라이드합니다.
        self.vbox = QVBoxLayout()  # 수직 레이아웃(hbox들 담을 예정)
        self.hbox_1 = QHBoxLayout()  # 위에서 1번째: 버튼 모음
        self.hbox_2 = QHBoxLayout()  # 위에서 2번째: 숫자 입력하기
        self.hbox_3 = QHBoxLayout()  # 위에서 3번째: 닫기

        self.save_button = Basic_button(
            "Installment", "Instalment saving account. Cannot be closed.", self)  # 저축 버튼
        self.save_button.clicked.connect(self.save_money)  # 버튼-기능 연결(저축)
        self.loan_button = Basic_button("Loan", "Loan", self)  # 대출 버튼
        self.loan_button.clicked.connect(self.get_loan)  # 버튼-기능 연결(대출)
        self.pay_button = Basic_button(
            "Payoff", "Loan payoff", self)  # 대출 갚기 버튼
        self.pay_button.clicked.connect(self.pay_for_loan)  # 버튼-기능 연결(갚기)
        place_in_layout(self.hbox_1, (self.save_button,
                                      self.loan_button, self.pay_button))

        self.money_amount = QLineEdit()  # 돈 입력하는 곳
        self.money_amount.setPlaceholderText("type money...")  # 텍스트 힌트
        place_in_layout(self.hbox_2, (self.money_amount,), "center")
        place_in_layout(self.hbox_3, (Close_button(
            "Close", "Close bank.", self),), "center")

        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hbox_1)
        self.vbox.addLayout(self.hbox_2)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hbox_3)
        self.setLayout(self.vbox)

        # 창의 크기, 위치
        self.x_loc = 225
        self.y_loc = 250
        self.width = 500
        self.height = 200

    # 저축하기 함수
    def save_money(self):
        try:
            self.save_amount = int(self.money_amount.text())  # 저축 금액
        except ValueError:  # 입력값이 이상하면
            return  # 돌려보낸다
        else:
            if self.save_amount <= 0:  # 양수가 아니어도
                return  # 돌려보낸다
            else:  # 문제 없는 경우
                money.invest(self.save_amount)  # 저축을 하고
                self.origin.refresh()  # 원래 창을 새로고침

    # 대출받기 함수
    def get_loan(self):
        try:
            self.loan_amount = int(self.money_amount.text())
        except ValueError:
            return
        else:
            if self.loan_amount <= 0:
                return
            else:
                money.make_loan(self.loan_amount)
                self.origin.refresh()

    def pay_for_loan(self):
        try:
            self.pay_amount = int(self.money_amount.text())
        except ValueError:
            return
        else:
            if self.pay_amount <= 0:
                return
            else:
                money.payoff_loan(self.pay_amount)
                self.origin.refresh()


class List_wind(Wind):
    """
    리스트와 닫기 버튼이 있는 창입니다. Wind를 상속합니다.
    """

    def design(self):
        # 상위 클래스로부터 오버라이드합니다.
        self._vbox = QVBoxLayout()  # 수직 레이아웃
        self.List = QListWidget()  # 리스트
        self._vbox.addWidget(self.List)  # 수직 레이아웃에 리스트 추가
        self._hbox = QHBoxLayout()  # 수평 레이아웃
        place_in_layout(
            self._hbox, (Close_button("Close", "Close this window.", self),), "center")  # 수평 레이아웃에 닫기 버튼 추가
        self._vbox.addLayout(self._hbox)  # 수직 레이아웃에 수평 레이아웃 추가
        self.setLayout(self._vbox)  # 수직 레이아웃 배치

        # 창의 위치, 크기
        self.x_loc = 100
        self.y_loc = 100
        self.width = 400
        self.height = 300


class News_wind(List_wind):
    """
    뉴스를 띄우는 창입니다. List_wind를 상속합니다. 
    """

    def design(self):
        # 상위 클래스로부터 오버라이드합니다.
        super().design()
        for i in News_List:  # 뉴스 리스트(문자열 원소 iterable)에서 하나씩 꺼내어
            self.List.addItem(i)  # 뉴스를 리스트에 띄운다
        self.width = 600


class Predict_wind(Popup_wind):
    """
    정보를 예측해주는 창입니다. Popup_wind를 상속합니다.
    """

    def design(self):
        # 상위 클래스로부터 오버라이드합니다.
        self.Prediction_list = QListWidget()
        self.Prediction_list.setFixedSize(540, 270)
        self.get_info_button = Basic_button(
            "Get Info", "Purchace prediction of tomorrow", self)
        self.get_info_button.clicked.connect(self.addinfo)

        self.hbox_1 = QHBoxLayout()
        self.hbox_2 = QHBoxLayout()
        self.vbox = QVBoxLayout()

        place_in_layout(
            self.hbox_1, (self.Prediction_list,),)
        place_in_layout(self.hbox_2, (self.get_info_button, Close_button(
            "Close", "Close this window", self)))
        place_in_layout(self.vbox, (self.hbox_1, self.hbox_2))
        self.setLayout(self.vbox)

        # 창의 위치, 크기
        self.x_loc = 300
        self.y_loc = 240
        self.width = 600
        self.height = 360

    def addinfo(self):
        if money.ismoneyleft(Info_Cost):
            money.money -= Info_Cost
            self.Prediction_list.addItem(getinfo())
        self.origin.refresh()


class Storage_wind(List_wind):
    """
    창고를 띄우는 창입니다. List_wind를 상속합니다.
    """

    def design(self):
        # 상위 클래스로부터 오버라이드합니다.
        super().design()  # List_Wind의 design 호출
        self.List.addItem('이름:\t수량:\t유통기한:')
        self.List.addItem('-'*40)
        for (name, data) in list(storage.warehouse.items()):
            if not isinstance(getclass(name), ExpireProduct):
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
    (가장 무난, 후에 clicked.connect()로 기능 추가 가능)
    """

    def utility_set(self, window):
        pass


class Link_button(Push_button):
    """
    눌리면 새 창을 띄우는 버튼 클래스입니다. Push_button을 상속합니다.
    """

    def __init__(self, name, tooltip, window, link_class, link_name, link_origin=None):
        """
        상위 클래스로부터 오버라이드합니다.
        :parameter link_class: 띄울 창의 클래스입니다.
        :parameter link_name: 띄울 창의 이름입니다.
        :parameter link_origin: 어떤 창에서 띄우는지를 저장합니다.
        """
        self.linkage_info = (link_class, link_name,
                             link_origin)  # 띄울 창의 정보를 튜플로 만들기
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
        if issubclass(self.linkage_info[0], Popup_wind):  # 만약 창 클래스가 팝업이라면?
            self.link = self.linkage_info[0](
                self.linkage_info[1], self.linkage_info[2])  # 원점 정보 추가
        else:  # 아니면
            self.link = self.linkage_info[0](self.linkage_info[1])  # 그냥 호출


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
        super().open_new_window()  # 새로운 창을 열고
        self.window.strong_close(QCloseEvent)  # 지금 창을 닫는다


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
