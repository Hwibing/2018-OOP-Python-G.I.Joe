import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

if __name__=="__main__":
    print("Hello, world!")
    print("This is GUI.")

# 창 클래스
class Wind(QWidget):
    """
    창 클래스입니다. QWidget을 상속합니다.
    시작하자마자 __init__이 호출되며, __init__은 창의 이름을 매개변수로 받습니다.
    :parameter name: 띄울 창의 이름입니다.
    """
    def __init__(self,name): # 생성자
        super().__init__() # 상위 클래스의 생성자 호출
        self.name=name # 창의 이름 정하기
        self.initUI() # initUI 메소드 호출
    def initUI(self):
        self.setWindowTitle(self.name) # 창의 제목(위쪽 바에 표시되는...)
        self.show() # 보이기

class button(QPushButton):
    """
    버튼 클래스입니다. QPushButton을 상속합니다.
    """
    raise NotImplementedError

class intro_wind(Wind):
    """
    프로그램을 작동하자마자 뜨는 창입니다. Wind를 상속합니다.
    게임 시작/종료 버튼만 존재합니다. 게임 시작을 누르면 게임이 열리고, 게임 종료를 누르면 끝납니다.
    :parameter name: 띄울 창의 이름입니다.
    """
    def initUI(self):
        self.setWindowTitle(self.name) # 창이 이름 지정
        start_btn=QPushButton("Start",self) # 시작 버튼
        start_btn.resize(start_btn.sizeHint()) # 크기 조정
        start_btn.setToolTip("Start game.") # 툴팁 설정
        quit_btn=QPushButton("Quit",self) # 종료 버튼
        quit_btn.resize(quit_btn.sizeHint()) # 크기 조정
        start_btn.setToolTip("Quit game.") # 툴팁 설정

        self.setGeometry(300,300,200,150) # 창 위치와 창 크기
        start_btn.move(45,30) # 버튼 위치 조정
        quit_btn.move(45,90) # 버튼 위치 조정
        self.show() # 창 보이기

app=QApplication(sys.argv) # application 객체 생성하기 위해 시스템 인수 넘김
intro=intro_wind("Intro")
sys.exit(app.exec_()) # 이벤트 처리를 위한 루프 실행(메인 루프), 루프가 끝나면 프로그램도 종료