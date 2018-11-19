import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

if __name__=="__main__":
    print("Hello, world!")
    print("This is GUI.")

class window(QWidget): # QWidget 클래스를 상속함(창)
    def __init__(self,name): # 생성자
        super().__init__()
        self.name=name # 창의 이름
        self.init_UI(self)
    def init_UI(self,name): # UI 초기화
        self.setWindowTitle(name) # 창의 이름(init의 name)
        self.show() # 보이기

app=QApplication(sys.argv)
main_window=window("Millstone")
sys.exit(app.exec_())