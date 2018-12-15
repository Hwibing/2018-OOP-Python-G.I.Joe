# -*- coding:utf-8 -*-
# 사용 폰트: 제주고딕
import sys

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QCloseEvent, QIcon, QPixmap, QFont, QColor
from PyQt5.QtWidgets import (QAction, QApplication, QHBoxLayout, QLabel,
                             QLineEdit, QListWidget, QMainWindow, QMessageBox,
                             QPushButton, QVBoxLayout, QWidget, QCheckBox)

from MainStream import *

opened_window_list = dict()  # 열려 있는 창들을 모아 놓은 딕셔너리(이름이 key, 객체가 value)


def place_in_layout(layout: (QHBoxLayout, QVBoxLayout), details: tuple, arrange="spread"):
    """
    레이아웃과 담을 것들을 받아 배치합니다. (Stretch 이용)
    :parameter layout: 레이아웃입니다. (QHBoxLayout 또는 QVBoxLayout)
    :parameter details: 레이아웃에 담을 것들의 튜플 객체입니다.
    :parameter arrange: 배치 방식입니다. 
    :Exception: 담을 내용 오류/유효하지 않은 배치 방식
    """
    arrange = arrange.lower()  # 소문자화(비교를 위해)
    if arrange not in ("spread", "center", "front", "back", "wing_f", "wing_b", "dispersion", "normal"):  # 배치 방식이 다음 중 없으면?
        raise Exception("Invalid arrangement.")  # 예외 발생

    """
    spread: 고르게 분산
    center: 중심으로 쏠림
    front: 앞으로 쏠림 / back: 뒤로 쏠림
    wing_f, wing_b: 양쪽으로 갈라짐, 홀수 개 위젯일 때 가운데 것을 f는 앞에, b는 뒤에 붙임
    """
    # 이하는 크게 신경쓰지 않아도 됨(배치 방법에 따라 위젯 적절히 나열하기
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
                layout.addLayout(details[l])
            finally:
                layout.addStretch(1)
        elif is_odd and "b" in arrange:
            layout.addStretch(1)
            try:
                layout.addWidget(details[l])
            except Exception:
                layout.addLayout(details[l])
        else:
            layout.addStretch(1)
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


def YN_question(window, question_name: str, question_str: str):
    """
    QMessagebox로 예/아니오를 물어봅니다.
    :parameter window: 어디 창에서 질문을 띄울 건지
    :parameter question_name: 질문 창 이름(문자열)
    :parameter question_str: 질문 내용(문자열)
    :return: bool타입의 대답(True: Yes, False: No)
    """
    ans = QMessageBox.question(window, question_name, question_str,
                               QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)  # 메시지박스로 대답 얻고
    return (ans == QMessageBox.Yes)  # 대답이 Yes인지를 비교하여 리턴


def set_background_color(changing_object, color):
    """
    changing_object의 배경색을 바꾸어줍니다!
    :parameter changing_object: 배경색이 존재하는 pyqt 객체
    :parameter color: 배경색을 어떤 색으로 바꿀지
    :return: 제대로 되면 True, 아니면 False
    아래 코드는 신경쓰지 않는걸로! (dict 쓰려니 메모리가...눈물...)
    """
    p = changing_object.palette()
    if color == "red":
        p.setColor(changing_object.backgroundRole(), Qt.red)
    elif color == "blue":
        p.setColor(changing_object.backgroundRole(), Qt.blue)
    elif color == "green":
        p.setColor(changing_object.backgroundRole(), Qt.green)
    elif color == "black":
        p.setColor(changing_object.backgroundRole(), Qt.black)
    elif color == "white":
        p.setColor(changing_object.backgroundRole(), Qt.white)
    elif color == "gray":
        p.setColor(changing_object.backgroundRole(), Qt.gray)
    else:
        return False
    changing_object.setPalette(p)
    return True


def gen_items_in_list(list_widget: QListWidget):
    """
    list_widget 안의 모든 원소를 순서대로 반환하는 제너레이터입니다.
    :parameter list_widget: 아이템을 순서대로 보고 싶은 QListWidget 객체입니다. 
    """
    for i in range(list_widget.count()):
        yield list_widget.item(i)


def only_positive_int(parameter):
    """
    parameter를 양의 정수로 바꿀 수 있다면 바꿔서 반환합니다.
    그럴 수 없다면 값을 반환하지 않습니다. 
    :parameter parameter: int화시킬 객체입니다.
    :return 1: 양의 정수를 반환합니다.
    :return 2: None
    """
    try:
        parameter = int(parameter)
    except ValueError:
        return
    else:
        if parameter > 0:
            return parameter


def alert_message(origin, alert_name, alert_detail):
    """
    경고 창을 띄웁니다. 닫기 전엔 다른 걸 할 수 없습니다.
    :parameter origin: 이 경고창이 어디서 띄워지는지
    :parameter alert_name: 경고 창의 제목
    :parameter alert_detail: 경고 창 내용
    """
    msg = QMessageBox()  # 메시지 객체 생성
    msg.setIcon(QMessageBox.Critical)  # 아이콘: 빨간 X자
    msg.setWindowTitle(alert_name)  # 창 이름
    msg.setText(alert_detail)  # 창 내용
    msg.setStandardButtons(QMessageBox.Ok)  # 버튼 1개 추가: ok 버튼
    msg.exec_()  # 실행하기(이거 끄기 전에 못 끔)

# 누가 클래스 상속구조 이따구로 짰냐 아 나구나


class Wind(QWidget):
    """
    창 클래스입니다. QWidget을 상속합니다.
    Wind 클래스를 만들면 창이 띄워집니다.
    """

    def __init__(self, name, origin=None):
        """
        생성자입니다. 
        띄울 창의 이름을 결정하며, 끝날 때 setup을 호출합니다.
        :parameter name: 창의 이름입니다.
        :parameter origin: 본 창을 띄운 창입니다. 
        """
        opened_window_list[name] = self
        super().__init__()  # 상위 클래스의 생성자 호출
        self.name = name  # 창의 이름 정하기
        self.origin = origin  # 원점 확인
        self.strong = False  # 되묻지 않고 닫을지에 대한 여부
        self.design()  # 디자인
        self.btnClickConnect()  # 버튼 기능 연결
        self.setup()  # 셋업

    def design(self):
        """
        창을 디자인합니다. 반드시 오버라이드해야 합니다.
        하는 일: 레이아웃, 버튼/텍스트 띄우기, 크기 결정
        """
        raise Exception("Abstract Method")

    def btnClickConnect(self):
        """
        버튼 클릭과 함수를 연결해줍니다. 반드시 오버라이드해야 합니다.
        하는 일: 버튼과 함수를 연결짓기
        """
        raise Exception("Abstract Method")

    def setup(self):
        """
        창을 세팅하고 띄웁니다.
        하는 일: 창의 제목 설정, 창 보이기, 창 위치/크기 설정
        """
        self.setWindowTitle(self.name)  # 창의 제목 설정
        self.move(self.x_loc, self.y_loc)  # 창의 위치 설정
        self.setFixedSize(self.width, self.height)  # 창의 크기 설정
        self.show()  # 창 보이기

    def closeEvent(self, QCloseEvent):
        """
        창 닫기 이벤트입니다. X 버튼을 누르거나 .close()를 호출할 때 발생합니다.
        사용자에게 정말 닫을 거냐고 되묻습니다.
        강하게 닫을 경우 (strong=true) 되묻지 않고 바로 꺼집니다.
        """
        if self.strong:  # 만약 되묻지 않기로 했다면?
            QCloseEvent.accept()  # 그냥 CloseEvent 수용
        else:  # 되묻기
            # 물어보기(Y/N), 그 결과를 ans에 저장
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
        기본적으로 .update지만, 오버라이드 시 앞에 무언가를 넣을 수도 있습니다.
        """
        self.update()  # 업데이트


class Main_wind(Wind):
    """
    메인 윈도우입니다. Wind를 상속합니다.
    게임 플레이의 중추입니다.
    Main window에서 모든 부가 창으로 이동할 수 있습니다.
    """

    def __init__(self, name, origin=None):
        self.opened = {"agr": True, "liv": True, "man": True, "lux": True}
        super().__init__(name, origin)

    def design(self):
        # 상위 클래스로부터 오버라이드합니다.
        self.Products = QListWidget()  # 물품 목록
        self.showProducts()  # 물품 리스트 출력

        self.Products.setFixedSize(600, 450)  # 크기 고정
        # self.Products.setFont(QFont("ㅁㄴㅇㄹ")) # 폰트 설정
        self.Products.itemSelectionChanged.connect(
            self.selectionChanged_event)  # 선택 아이템이 바뀌었을 때

        self.Info_text = Text("{}번째 주\n남은 돈: {}\n창고 용량: {}/{}".format(
            Day, money.money, storage.quantity, storage.maxsize), self)  # 정보 텍스트
        self.Info_text.setFont(QFont("제주고딕", 10))
        self.Bank_button = Link_button(
            "은행", "은행 창을 엽니다.", self, Bank_Wind, "Bank", self)  # 은행
        self.Storage_button = Link_button(
            "창고", "창고 목록을 봅니다", self, Storage_wind, "Storage", self)  # 창고용량

        self.item_deal = QVBoxLayout()  # 물품 정보 및 매매
        self.item_name = Text("왼쪽의 물건 목록에서", self)  # 초기 텍스트1
        self.item_price = Text("거래하려는 것을 선택하세요.", self)  # 초기 텍스트2
        self.ProductImageLabel = QLabel(self)

        self.Buy_button = Basic_button(
            "구매", "선택한 물건을 수량만큼 구입합니다.", self)  # 구입 버튼
        self.Sell_button = Basic_button(
            "판매", "선택한 물건을 수량만큼 판매합니다.", self)  # 판매 버튼
        self.Buy_max = Basic_button(
            "최댓값", "현재 돈으로 살 수 있는 만큼 수량을 지정합니다.", self)  # 최댓값
        self.Sell_all = Basic_button(
            "보유량", "선택한 물건이 창고에 있는 개수 만큼 수량을 지정합니다..", self)  # 전부 팔기

        self.Buy_layer = QHBoxLayout()  # 구매, 최대 버튼
        self.Sell_layer = QHBoxLayout()  # 판매, 전체 버튼
        place_in_layout(
            self.Buy_layer, (self.Buy_max, self.Buy_button), "normal")
        place_in_layout(self.Sell_layer,
                        (self.Sell_all, self.Sell_button), "normal")

        self.numCount = QLineEdit(self)  # 개수 입력하는 부분
        self.numCount.setPlaceholderText("개수를 입력하세요...")  # 힌트 메시지
        place_in_layout(self.item_deal, (self.item_name,
                                         self.item_price, self.ProductImageLabel,
                                         self.Buy_layer, self.numCount, self.Sell_layer))  # 물품 처리 영역

        self.News_button = Link_button(
            "뉴스", "오늘의 뉴스 목록입니다.", self, News_wind, "News")  # 뉴스 버튼
        self.Predict_button = Link_button(
            "예측", "내일의 예측을 보러 갑니다.", self, Predict_wind, "Predict", self)  # 예측 버튼

        self.Next_day_button = Basic_button(
            "잠자기", "다음 날로 넘어갑니다", self)  # '다음 날' 버튼
        self.Next_day_button.setShortcut("Ctrl+S")
        self.End_button = Quit_button(
            "종료", "저장되지 않습니다.", self)  # '끝내기' 버튼

        top_box = QHBoxLayout()  # 상부
        place_in_layout(
            top_box, (self.Info_text, self.Bank_button, self.Storage_button))

        mid_box = QHBoxLayout()  # 중간
        place_in_layout(mid_box, (self.Products, self.item_deal))

        low_box = QHBoxLayout()  # 중하부, 각 품목을 클릭하면 줄어들도록
        # 4개의 체크박스(보기/접기 용도)
        self.agr_chkbox = QCheckBox("agriculture", self)
        self.liv_chkbox = QCheckBox("livestock", self)
        self.man_chkbox = QCheckBox("manufactured", self)
        self.lux_chkbox = QCheckBox("luxury", self)
        self.checkboxes = (self.agr_chkbox, self.liv_chkbox,
                           self.man_chkbox, self.lux_chkbox)
        for i in self.checkboxes:
            i.toggle()  # 시작은 켜져 있는 상태로
        place_in_layout(low_box, (self.agr_chkbox, self.liv_chkbox,
                                  self.man_chkbox, self.lux_chkbox), "center")

        bottom_box = QHBoxLayout()  # 하부
        place_in_layout(
            bottom_box, (self.News_button, self.Predict_button, self.Next_day_button, self.End_button), "wing_b")

        vbox = QVBoxLayout()  # 전체 레이아웃
        vbox.addStretch(1)
        place_in_layout(vbox, (top_box, mid_box, low_box,
                               bottom_box), arrange="dispersion")

        # 창의 위치, 크기
        self.x_loc = 60
        self.y_loc = 45
        self.width = 1280
        self.height = 720
        self.setLayout(vbox)

    def btnClickConnect(self):
        # 상위 클래스로부터 오버라이드합니다.
        self.Buy_button.clicked.connect(self.buy_item)
        self.Sell_button.clicked.connect(self.sell_item)
        self.Buy_max.clicked.connect(self.max_buy)
        self.Sell_all.clicked.connect(self.all_sell)
        self.Next_day_button.clicked.connect(self.next_day)
        for i in self.checkboxes:
            i.stateChanged.connect(self.hide_n_show(i))

    def showProducts(self):
        """
        Products - QListWidget에 물건들을 넣습니다.
        처음에 비운 뒤, 아이템을 순서대로 박아줍니다.
        구분선이 존재합니다.
        """
        self.Products.clear()
        self.Products.addItem("물품\t요금(τ)\t유통기한(일)")
        if self.opened["agr"]:
            self.Products.addItem("----------[농산물]-----------")
            for (name, [price, date]) in list(agriculture.productList.items()):
                self.Products.addItem(name+"\t"+str(price)+"\t"+str(date))
        if self.opened["liv"]:
            self.Products.addItem("----------[축/수산물]-----------")
            for (name, [price, date]) in list(livestock.productList.items()):
                self.Products.addItem(name+"\t"+str(price)+"\t"+str(date))
        if self.opened["man"]:
            self.Products.addItem("----------[공산품]-----------")
            for (name, price) in list(manufactured.productList.items()):
                self.Products.addItem(name+"\t"+str(price))
        if self.opened["lux"]:
            self.Products.addItem("----------[사치품]-----------")
            for (name, price) in list(luxury.productList.items()):
                self.Products.addItem(name+"\t"+str(price))

    def selectionChanged_event(self):
        """
        리스트(물건 목록)에서 선택한 아이템이 바뀌었을 때 호출됩니다.
        하는 일: 텍스트 바꾸기, 이미지 바꾸기, 현 아이템 바꾸기
        """
        try:
            k = str(self.Products.currentItem().text())
        except AttributeError:
            return
        else:
            if "-" in k or "τ" in k:
                return
            k = k.split("\t")

        self.current_item_name = str(k[0].strip("\t"))  # 아이템 이름
        self.current_item_price = int(
            k[1].strip("\t").replace("\t", ""))  # 아이템 가격
        self.item_name.setText(self.current_item_name)  # 이름을 띄우고
        self.item_price.setText(str(self.current_item_price)+" Tau")  # 가격도 띄우고

        # 물건의 클래스 이름을 받아 적절한 이미지 배치
        self.item_class = getclass(self.current_item_name).type
        print("images/Raw File/{}/{}.png".format(self.item_class, self.current_item_name))
        self.item_pixmap = QPixmap(
            "images/Raw File/{}/{}.png".format(self.item_class, self.current_item_name))  # 픽스맵 불러오기
        self.ProductImageLabel.setPixmap(self.item_pixmap)  # 픽스맵 띄우기
        self.update()  # 새로고침

    def hide_n_show(self, changedCheck):  # Closure를 이용한 clicked.connect(매개변수 함수)
        def folder():  # inner function
            k = changedCheck.text()[:3].lower()  # 첫 3글자 소문자
            self.opened[k] = not self.opened[k]  # 상태 반전
            self.refresh()  # 새로고침
        return folder

    def buy_item(self):
        """
        아이템을 구매할 때 호출되는 메소드입니다. (buy button 클릭됨)
        self.num이 유효한 값인지 확인하고, 선택한 아이템이 있는지도 확인합니다.
        결정 직전에 되묻습니다. 취소할 수 있습니다.
        """
        self.num = self.numCount.text()
        self.num = only_positive_int(self.num)
        if self.num:  # 유효한 값일 경우
            try:
                ans = YN_question(self, "Confirm", "정말 사시겠어요?\n총 가격: %d Tau" % (
                    self.num*int(self.current_item_price)))  # ㄹㅇ 살거임?
            except AttributeError:  # 선택을 안했다면(current 생성 X)
                alert_message(self, "Error", "품목을 선택해주세요.")
                return  # 리턴
            if ans:  # 넹
                self.result = buy(self.current_item_name, getclass(
                    self.current_item_name), self.num)  # 그럼 사세요
                self.refresh()
                if not self.result:  # 만약 구매에 실패하면?
                    QMessageBox().about(self, "Error", "그럴 수 없습니다.\n돈 혹은 창고를 확인해주세요.")
            else:  # 아녀
                pass  # 지나가세요
        else:
            alert_message(self, "Error", "유효하지 않은 값입니다.")

    def sell_item(self):
        """
        아이템을 판매할 때 호출되는 메소드입니다. (sell button 클릭됨)
        self.num이 유효한 값인지 확인하고, 선택한 아이템이 있는지도 확인합니다.
        결정 직전에 되묻습니다. 취소할 수 있습니다.
        """
        self.num = self.numCount.text()
        self.num = only_positive_int(self.num)
        if self.num:
            try:
                ans = YN_question(self, "Confirm", "정말 파시겠어요?\n총 가격: %d Tau" % (
                    self.num*int(self.current_item_price)))  # ㄹㅇ 팔거임?
            except AttributeError:  # 선택을 안했다면(current 생성 X)
                QMessageBox.about(
                    self, "Alert", "품목을 선택해주세요.")  # 알림
                return  # 리턴
            if ans:
                self.result = sell(self.current_item_name, getclass(
                    self.current_item_name), self.num)
                self.refresh()
                if not self.result:  # 만약 판매에 실패하면?
                    QMessageBox().about(self, "Error", "그럴 수 없습니다.\n창고를 확인해주세요.")
            else:
                pass
        else:
            alert_message(self, "Error", "유효하지 않은 값입니다.")

    def max_buy(self):
        # 금액 내에서 최대로 구입 가능한 수량을 입력해줍니다.
        try:
            self.numCount.setText(
                str(money.money//self.current_item_price))  # 정수 나눗셈
        except AttributeError:
            alert_message(self, "Error", "아이템을 선택해주세요.")

    def all_sell(self):
        # 창고에 있는 물건의 개수를 입력해줍니다.
        try:
            pass
        except AttributeError:
            alert_message(self, "Error", "아이템을 선택해주세요.")

    def next_day(self):
        """
        다음 날로 넘어갑니다. Day를 증가시키고, storage의 유통기한을 1씩 없앱니다.
        파산을 감지합니다. (돈<0)
        Main Window를 제외한 모든 창을 닫고, 새로 뉴스를 띄웁니다.
        """
        global Day
        Day += 1  # 하루 더하기
        bad_event_result = sleep()  # 잠자기

        self.window_will_be_closed = opened_window_list.items()
        for (window_name, window_object) in self.window_will_be_closed:  # 지금까지 열려 있는 창 닫기(main 제외)
            if not isinstance(window_object, Main_wind):
                window_object.strong_close()  # 닫는당
        opened_window_list.clear()  # 딕셔너리를 비우고
        opened_window_list[self.name] = self  # 자신을 넣는다

        self.refresh()  # 다시 창 띄우기
        if money.money < 0:  # 돈이 0보다 적으면
            QMessageBox().about(self, "Bankrupt", "You are bankrupt!")  # 파산 알림
            self.restart_button = Moveto_button(
                "Restart", "Restart game.", self, Intro_wind, "Restart")  # 보이지 않는 버튼
            self.restart_button.click()  # 게임 재시작
            raise NotImplementedError  # 변수 초기화
        self.News_button.click()  # 뉴스 띄우기

        if bad_event_result == (True,):
            alert_message(self, "Thief", "도둑이 당신의 금고를 털었습니다!\n보유 재산이 0원이 됩니다.")

    def refresh(self):
        # 상위 클래스로부터 오버라이드합니다.
        self.Info_text.setText("{}번째 주\n남은 돈: {}\n창고 용량: {}/{}".format(
            Day, money.money, storage.quantity, storage.maxsize))  # 텍스트 재설정
        self.showProducts()  # 사진 다시 띄우기, 리스트 다시 출력.
        super().refresh()  # 상위 클래스의 refresh 불러옴


class Intro_wind(Wind):
    """
    프로그램을 작동하자마자 뜨는 창입니다. Wind를 상속합니다.
    게임 시작/종료 버튼만 존재합니다. 게임 시작을 누르면 게임이 열리고, 게임 종료를 누르면 끝납니다.
    """

    def design(self):
        # 상위 클래스로부터 오버라이드합니다.
        self._start_btn = Moveto_button(
            "시작하기", "게임을 시작합니다", self, Main_wind, "Main")  # 게임 시작 버튼
        self._start_hbox = QHBoxLayout()  # 게임 시작 버튼 배치 레이아웃(수평)
        place_in_layout(self._start_hbox, (self._start_btn,),
                        "center")  # 배치(함수 이용)

        self._quit_btn = Quit_button("종료하기", "게임을 종료합니다.", self)  # 게임 종료 버튼
        self._quit_hbox = QHBoxLayout()  # 게임 종료 버튼 배치 레이아웃(수평)
        place_in_layout(self._quit_hbox, (self._quit_btn,),
                        "center")  # 배치(함수 이용)

        self._vmid_box = QVBoxLayout()  # 두 레이아웃을 수직으로 놓는 레이아웃
        place_in_layout(self._vmid_box, (self._start_hbox,
                                         self._quit_hbox))  # 두 버튼의 레이아웃을 레이아웃에 담음

        self.setLayout(self._vmid_box)  # 창의 레이아웃을 이걸로 설정

        self.x_loc = 300
        self.y_loc = 300
        self.width = 200
        self.height = 150

    def btnClickConnect(self):
        # 상위 클래스로부터 오버라이드합니다.
        pass


class Bank_Wind(Wind):
    """
    은행 업무를 맡는 창입니다. List_wind를 상속합니다.
    """

    def design(self):
        # 상위 클래스로부터 오버라이드합니다.
        self.vbox = QVBoxLayout()  # 수직 레이아웃(hbox들 담을 예정)
        self.hbox_1 = QHBoxLayout()  # 위에서 1번째: 적금액, 대출액
        self.hbox_2 = QHBoxLayout()  # 위에서 2번째: 숫자 입력하기
        self.hbox_3 = QHBoxLayout()  # 위에서 3번째: 버튼 모음
        self.hbox_4 = QHBoxLayout()  # 위에서 4번째: 닫기

        self.save_button = Basic_button(
            "적금", "적금 계좌에 입금합니다. 다시 꺼낼 수 없습니다.", self)  # 저축 버튼
        self.loan_button = Basic_button(
            "대출", "대출을 받습니다. 이자에 조심하세요!", self)  # 대출 버튼
        self.pay_button = Basic_button(
            "상환", "대출금을 갚습니다.", self)  # 대출 갚기 버튼
        place_in_layout(self.hbox_3, (self.save_button,
                                      self.loan_button, self.pay_button))

        self.now_invest = Text("적금액: "+str(money.bank), self)  # 현재 적금액
        self.now_loan = Text("대출금: "+str(money.debt), self)  # 현재 대출액
        place_in_layout(self.hbox_1, (self.now_invest, self.now_loan))

        self.money_count = QLineEdit()  # 돈 입력하는 곳
        self.money_count.setPlaceholderText("돈을 입력하세요...")  # 텍스트 힌트
        place_in_layout(self.hbox_2, (self.money_count,), "center")
        place_in_layout(self.hbox_4, (Close_button(
            "닫기", "은행에서 나갑니다.", self),), "center")

        place_in_layout(self.vbox, (self.hbox_1, self.hbox_2, self.hbox_3,
                                    self.hbox_4), "dispersion")
        self.setLayout(self.vbox)

        self.x_loc = 225
        self.y_loc = 250
        self.width = 500
        self.height = 200

    def btnClickConnect(self):
        # 상위 클래스로부터 오버라이드합니다.
        self.save_button.clicked.connect(self.save_money)
        self.loan_button.clicked.connect(self.get_loan)
        self.pay_button.clicked.connect(self.pay_for_loan)

    # 저축하기 함수
    def save_money(self):
        """
        돈을 저축하는 함수입니다. (save button 클릭 시 호출)
        money_count의 값을 읽어 돈을 넣습니다.
        저축을 하고 창을 새로고침하여 텍스트를 업데이트합니다.
        """
        self.save_amount = only_positive_int(self.money_count.text())  # 저축 금액
        if self.save_amount:
            self.result = money.invest(self.save_amount)  # 저축을 하고
            self.origin.refresh()  # 원래 창을 새로고침
            if not self.result:  # 저축이 안되면
                alert_message(self, "Error", "그럴 수 없습니다.\n돈을 확인해주세요.")
        else:
            alert_message(self, "Error", "유효하지 않은 값입니다.")
        self.refresh()  # 창 새로고침

    # 대출 받기 함수, 저축과 크게 안 다름
    def get_loan(self):
        self.loan_amount = only_positive_int(self.money_count.text())
        if self.loan_amount:
            money.make_loan(self.loan_amount)
            self.origin.refresh()
        else:
            alert_message(self, "Error", "유효하지 않은 값입니다.")
        self.refresh()

    # 대출 갚기 함수, 역시 크게 안 다름
    def pay_for_loan(self):
        self.pay_amount = only_positive_int(self.money_count.text())
        if self.pay_amount:
            self.result = money.payoff_loan(self.pay_amount)
            self.origin.refresh()
            if not self.result:
                alert_message(self, "Error", "그럴 수 없습니다.\n돈을 확인해주세요.")
        else:
            alert_message(self, "Error", "유효하지 않은 값입니다.")
        self.refresh()

    def refresh(self):
        # 상위 클래스로부터 오버라이드합니다.
        self.now_invest.setText("적금액: "+str(money.bank))  # 현재 적금액 텍스트 업데이트
        self.now_loan.setText("대출금: "+str(money.debt))  # 현재 대출액 텍스트 업데이트
        super().refresh()


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
            self._hbox, (Close_button("닫기", "이 창을 닫습니다.", self),), "center")  # 수평 레이아웃에 닫기 버튼 추가
        self._vbox.addLayout(self._hbox)  # 수직 레이아웃에 수평 레이아웃 추가
        self.setLayout(self._vbox)  # 수직 레이아웃 배치

        self.x_loc = 100
        self.y_loc = 100
        self.width = 400
        self.height = 300

    def btnClickConnect(self):
        # 상위 클래스로부터 오버라이드합니다.
        pass


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


class Predict_wind(Wind):
    """
    정보를 예측해주는 창입니다. Wind를 상속합니다.
    아니 이거 뭔가 List_wind 상속하면 되는데 ㅠㅠ
    """

    def design(self):
        # 상위 클래스로부터 오버라이드합니다.
        self.Prediction_list = QListWidget()
        self.Prediction_list.setFixedSize(540, 270)
        self.get_info_button = Basic_button(
            "정보 얻기", "돈을 지불하고 내일 무슨 일이 일어날지 알아봅니다", self)

        self.hbox_1 = QHBoxLayout()
        self.hbox_2 = QHBoxLayout()
        self.vbox = QVBoxLayout()

        place_in_layout(
            self.hbox_1, (self.Prediction_list,),)
        place_in_layout(self.hbox_2, (self.get_info_button, Close_button(
            "닫기", "이 창을 닫습니다.", self)))
        place_in_layout(self.vbox, (self.hbox_1, self.hbox_2))
        self.setLayout(self.vbox)

        self.x_loc = 300
        self.y_loc = 240
        self.width = 600
        self.height = 360

    def btnClickConnect(self):
        # 상위 클래스로부터 오버라이드합니다.
        self.get_info_button.clicked.connect(self.addinfo)

    def addinfo(self):
        if money.ismoneyleft(Info_Cost):
            money.money -= Info_Cost
            self.Prediction_list.addItem(getinfo())
        self.origin.refresh()


class Storage_wind(Wind):
    """
    창고를 띄우는 창입니다. Wind를 상속합니다.
    """

    def design(self):
        # 상위 클래스로부터 오버라이드합니다.
        self.List = QListWidget()  # 창고 품목 리스트
        self.List.addItem('이름:\t수량:\t유통기한:')
        self.List.addItem('-'*40)
        # 아래는 창고에 무엇이 들어있는지를 보여주는 부분
        for (name, data) in list(storage.warehouse.items()):
            if not isinstance(getclass(name), ExpireProduct):
                self.List.addItem(name + '\t' + str(data))
        for (name, datelist) in list(storage.warehouse_expire.items()):
            for [number, date] in datelist:
                self.List.addItem(name + '\t' + str(number) + '\t' + str(date))

        # 수직 레이아웃, 수평 레이아웃
        self._hbox = QHBoxLayout()
        self._vbox = QVBoxLayout()
        self.up_button = Basic_button(
            "창고 구매" if money.rent else "업그레이드",
            "더 좋은 창고로 이전합니다. 용량이 늘어나고, 보관 기간이 길어집니다.", self)

        place_in_layout(self._hbox, (self.up_button, Close_button(
            "닫기", "창고에서 나갑니다.", self)), "center")
        place_in_layout(self._vbox, (self.List, self._hbox), "normal")
        self.setLayout(self._vbox)

        self.x_loc = 100
        self.y_loc = 100
        self.width = 400
        self.height = 400

    def btnClickConnect(self):
        # 상위 클래스로부터 오버라이드합니다.
        self.up_button.clicked.connect(self.storage_upgrade)  # 창고 업그레이드 버튼

    def storage_upgrade(self):
        """
        창고를 업그레이드해주는 함수입니다.
        이 함수가 한 번이라도 호출되었다면 버튼이 '업그레이드'라, 아니면 '창고 구매'라고 뜹니다.
        """
        money.buy_warehouse(0)  # 창고 구매
        self.refresh()  # 새로고침

    def refresh(self):
        # 상위 클래스로부터 오버라이드합니다.
        self.up_button.setText("업그레이드")  # 버튼 텍스트 바꿔주기
        self.origin.refresh()
        super().refresh()


class Push_button(QPushButton):
    """
    버튼 클래스입니다. QPushButton을 상속합니다.
    """

    def __init__(self, name, tooltip, window):
        """
        생성자입니다. __init__이 끝날 때 utility_set을 호출합니다.
        :parameter name: 버튼의 이름(내용)입니다.
        :parameter tooltip: 버튼의 툴팁입니다. (마우스 올리면 나오는 내용)
        :parameter window: 이 버튼이 포함된 창입니다.
        """
        super().__init__(name, window)  # 상위 클래스의 생성자 호출
        self.setFont(QFont("제주고딕"))  # 폰트 설정
        self.design(tooltip)  # 디자인하기
        self.utility_set(window)  # 기능 설정

    def design(self, tooltip):
        """
        버튼을 디자인합니다.
        하는 일: 버튼 툴팁 설정, 위치 조정
        :parameter tooltip: 버튼 툴팁(마우스 올리면 나타나는 거)입니다.
        """
        self.setToolTip(tooltip)  # 툴팁 설정
        self.setFixedSize(self.sizeHint())  # 글씨에 따라 버튼 크기 조정

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
        self.link = self.linkage_info[0](
            self.linkage_info[1], self.linkage_info[2])  # 원점 정보 추가


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
        self.setShortcut("Esc")  # 단축키 설정: Esc


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
        self.setFont(QFont("제주고딕"))  # 폰트 설정

    def setup(self):
        # 텍스트를 세팅하고 띄웁니다. 크기는 글자에 맞추어 고정됩니다.
        self.setFixedSize(self.sizeHint())  # 크기 설정
        self.show()


app = QApplication(sys.argv)  # application 객체 생성하기 위해 시스템 인수 넘김
intro = Intro_wind("Intro")
sys.exit(app.exec_())  # 이벤트 처리를 위한 루프 실행(메인 루프), 루프가 끝나면 프로그램도 종료
