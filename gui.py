import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

if __name__=="__main__":
    # 디버깅용...
    print("Hello, world!")
    print("This is GUI.")

# 창 클래스
class Wind(QWidget):
    """
    창 클래스입니다. QWidget을 상속합니다.
    __init__ 메소드의 매개변수로 name 문자열을 넘겨주어야 합니다.
    Wind 클래스를 만들면 창이 띄워집니다.
    """
    def __init__(self,name):
        """
        생성자입니다. __init__이 끝날 때 initUI를 호출합니다.
        :parameter name: 창의 이름입니다.   
        """
        super().__init__() # 상위 클래스의 생성자 호출
        self.name=name # 창의 이름 정하기
        self.init_UI() # init_UI 메소드 호출

    def init_UI(self):
        """
        창의 UI를 수정하고, 창을 실질적으로 띄웁니다.
        """
        self.setWindowTitle(self.name) # 창의 제목(위쪽 바에 표시되는...)
        self.show() # 보이기

class Intro_wind(Wind):
    """
    프로그램을 작동하자마자 뜨는 창입니다. Wind를 상속합니다.
    게임 시작/종료 버튼만 존재합니다. 게임 시작을 누르면 게임이 열리고, 게임 종료를 누르면 끝납니다.
    :parameter name: 띄울 창의 이름입니다.
    """
    def init_UI(self):
        self.setWindowTitle(self.name) # 창이 이름 지정
        start_btn=Push_button("Start","Start game.",self) # 게임 시작 버튼
        quit_btn=Push_button("Quit","Quit game.",self) # 종료 버튼
        self.setGeometry(300,300,200,150) # 창 위치와 창 크기
        start_btn.move(45,35) # 버튼 위치 조정
        quit_btn.move(45,85) # 버튼 위치 조정
        self.show() # 창 보이기

class Push_button(QPushButton):
    """
    버튼 클래스입니다. QPushButton을 상속합니다.
    __init__의 매개변수로 이름과 툴팁, 띄울 Wind 클래스(혹은 그 상속)을 받습니다.
    """
    def __init__(self,name,tooltip,window):
        """
        생성자입니다. __init__이 끝날 때 initUI를 호출합니다.
        :parameter name: 창의 이름입니다.
        """
        super().__init__(name,window) # 상위 클래스의 생성자 호출
        self.resize(self.sizeHint()) # 글씨에 따라 버튼 크기 결정
        self.setToolTip(tooltip) # 툴팁 설정

app=QApplication(sys.argv) # application 객체 생성하기 위해 시스템 인수 넘김
intro=Intro_wind("Intro")
sys.exit(app.exec_()) # 이벤트 처리를 위한 루프 실행(메인 루프), 루프가 끝나면 프로그램도 종료