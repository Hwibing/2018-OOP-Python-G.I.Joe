import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

if __name__=="__main__":
    print("Hello, world!")
    print("This is GUI.")

class Wind(QWidget):
    def __init__(self,name): # 생성자
        super().__init__() # 상위 클래스의 생성자 호출
        self.name=name
        self.initUI() # initUI 메소드 호출
    def initUI(self):
        self.setWindowTitle(self.name) # 창의 제목(위쪽 바에 표시되는...)
        self.show() # 보이기

app=QApplication(sys.argv) # application 객체 생성하기 위해 시스템 인수 넘김
k=Wind("Main Window")
sys.exit(app.exec_()) # 이벤트 처리를 위한 루프 실행(메인 루프), 루프가 끝나면 프로그램도 종료