import sys
from PyQt5.QtWidgets import QWidget, QMainWindow, QAction, QApplication, QMessageBox, QPushButton
from PyQt5.QtCore import QCoreApplication
from abc import abstractmethod

if __name__=="__main__":
    print("Hello, world!")
    print("This is GUI.")

class Wind(QWidget):
    """
    창 클래스입니다. QWidget을 상속합니다.
    Wind 클래스를 만들면 창이 띄워집니다.
    """
    def __init__(self, name):
        """
        생성자입니다. 
        띄울 창의 이름을 결정하며, 끝날 때 initUI를 호출합니다.
        :parameter name: 창의 이름입니다.   
        """
        super().__init__() # 상위 클래스의 생성자 호출
        self.name=name # 창의 이름 정하기
        self.strong=False # 되묻지 않고 닫을지에 대한 여부
        self.setup() # setup 메소드 호출

    def setup(self):
        """
        창을 세팅하고 띄웁니다.
        """
        self.setWindowTitle(self.name) # 창의 제목(위쪽 바에 표시되는...)
        self.show() # 보이기

    def closeEvent(self, QCloseEvent): # 창 닫기 이벤트(X자 누르거나 .close() 호출 시)
        if self.strong: # 만약 되묻지 않기로 했다면? 
            QCloseEvent.accept() # 그냥 CloseEvent 수용
        else: # 되묻기
            # 메시지박스로 물어보기(Y/N), 그 결과를 ans에 저장
            ans=QMessageBox.question(self, "Confirm", "Do you want to quit?", 
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if ans==QMessageBox.Yes: # ~.Yes, ~.No는 상수여서 비교 가능
                QCloseEvent.accept() # CloseEvent 수용
            else:
                QCloseEvent.ignore() # CloseEvent 거절

    def strong_close(self, QCloseEvent): # 강하게 닫기 함수
        self.strong=True # 안 되묻기로 한 뒤
        self.close() # 닫는다(그냥 종료)

class Main_wind(QMainWindow):
    """
    메인 윈도우입니다. QMainWindow를 상속합니다. (혼동을 막기 위해 Wind와의 다중 상속을 피했습니다.)
    Wind와 상당히 유사합니다. 게임 플레이의 중추입니다.
    Main window에서 모든 부가 창으로 이동할 수 있습니다.
    """
    def __init__(self, name):
        """
        생성자입니다.
        끝날 때 initUI를 호출합니다.
        :parameter name: 창의 이름입니다. 
        """
        super().__init__() # 상위 클래스의 생성자 호출
        self.name=name # 창의 이름 정하기
        self.strong=False # 일단 약하게 닫기
        self.setup() # setup 메소드 호출

    def setup(self):
        """
        창을 세팅하고 띄웁니다. 
        """
        self.setWindowTitle(self.name) # 창의 제목
        self.setGeometry(100,100,1300,800) # 위치, 크기
        self.statusBar().showMessage("Main") # 상태 표시줄
        
        main_menu=self.menuBar() # 메뉴 바 만들기
        main_menu_file=main_menu.addMenu("File") # 메뉴 항목 추가
        self.show() # 창 보이기

    def closeEvent(self, QCloseEvent):
        if self.strong: # 만약 되묻지 않기로 했다면? 
            QCloseEvent.accept() # 그냥 CloseEvent 수용
        else: # 되묻기
            # 메시지박스로 물어보기(Y/N), 그 결과를 ans에 저장
            ans=QMessageBox.question(self, "Confirm", "Do you want to quit? Changes will not be saved.", 
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if ans==QMessageBox.Yes: # 결과를 보고 결정
                QCloseEvent.accept() # 이벤트 수용
            else:
                QCloseEvent.ignore() # 이벤트 거절

    def strong_close(self, QCloseEvent): # 강하게 닫기
        self.strong=True
        self.close()

class Intro_wind(Wind):
    """
    프로그램을 작동하자마자 뜨는 창입니다. Wind를 상속합니다.
    게임 시작/종료 버튼만 존재합니다. 게임 시작을 누르면 게임이 열리고, 게임 종료를 누르면 끝납니다.
    """
    def setup(self):
        # 상위 클래스로부터 오버라이드합니다.
        """
        띄울 창의 이름 결정, 시작/종료 버튼 생성, 위치/크기 조정을 담당합니다. 
        :parameter name: 창의 이름입니다.
        """
        self.setWindowTitle(self.name) # 창의 이름 지정
        start_btn=Push_button("Start", "Start game.", self) # 게임 시작 버튼
        quit_btn=Close_button("Quit", "Quit game.", self) # 종료 버튼

        self.setGeometry(300,300,200,150) # 창 위치와 창 크기
        start_btn.move(45,35) # 버튼 위치 조정
        quit_btn.move(45,85) # 버튼 위치 조정   
        self.show() # 창 보이기

class Push_button(QPushButton):
    """
    버튼 클래스입니다. QPushButton을 상속합니다.
    __init__의 매개변수로 이름과 툴팁, 띄울 Wind 클래스(혹은 그 상속)을 받습니다.
    """
    def __init__(self, name, tooltip, window):
        """
        생성자입니다. __init__이 끝날 때 utility_set을 호출합니다.
        :parameter name: 버튼의 이름(내용)입니다.
        :parameter tooltip: 버튼의 툴팁입니다. (마우스 올리면 나오는 내용)
        :parameter window: 버튼이 위치하는 Wind 객체입니다.
        """
        super().__init__(name,window) # 상위 클래스의 생성자 호출
        self.resize(self.sizeHint()) # 글씨에 따라 버튼 크기 결정
        self.setToolTip(tooltip) # 툴팁 설정
        self.utility_set(window)

    @abstractmethod
    def utility_set(self, window):
        """
        기능 설정입니다. 기능을 부여하려면 Override해야 합니다.
        """
        pass

class Link_button(Push_button):
    """
    눌리면 새 창을 띄우는 버튼 클래스입니다. Push_button을 상속합니다.
    """
    def __init__(self, name, tooltip, window, link_class, link_name):
        # 상위 클래스로부터 오버라이드합니다.
        """
        :parameter link_class: 띄울 창의 클래스입니다.
        :parameter link_name: 띄울 창의 이름입니다.
        """
        super().__init__(name, tooltip, window) # 상위 클래스의 생성자 호출
        self.resize(self.sizeHint()) # 글씨에 따라 버튼 크기 결정
        self.setToolTip(tooltip) # 툴팁 설정
        self.window_info=(link_class, link_name) # 창의 정보를 튜플로 만들기
        self.utility_set(window)

    def utility_set(self, window):
        # 상위 클래스로부터 오버라이드합니다. 
        self.clicked.connect(self.open_new_window)
    
    def open_new_window(self):
        """
        새 창을 여는 메소드입니다.
        """
        new_window=self.window_info[0](self.window_info[1])
        new_window.show()
        raise NotImplementedError

class Moveto_button(Link_button):
    """
    눌리면 다른 창으로 이동하는 버튼 클래스입니다. Link_button을 상속합니다.
    """
    pass # Link_Button 구현하고 하자

class Close_button(Push_button):
    """
    창을 닫을 때 쓰는 버튼 클래스입니다. Push_button을 상속합니다. 
    """
    def utility_set(self, window):
        # 상위 클래스로부터 오버라이드합니다. 
        self.clicked.connect(window.strong_close) # 호출하는 window를 닫습니다. (강하게)

class Quit_button(Close_button):
    """
    프로그램을 종료할 때 버튼 클래스입니다. Close_button을 상속합니다. 
    """
    def utility_set(self, window):
        # 상위 클래스로부터 오버라이드합니다. 
        self.clicked.connect(QCoreApplication.instance().quit) # 버튼을 누르면 다 종료되도록

if __name__=="__main__":
    app=QApplication(sys.argv) # application 객체 생성하기 위해 시스템 인수 넘김
    intro=Intro_wind("Intro")
    sys.exit(app.exec_()) # 이벤트 처리를 위한 루프 실행(메인 루프), 루프가 끝나면 프로그램도 종료
