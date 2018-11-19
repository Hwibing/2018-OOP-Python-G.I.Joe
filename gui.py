import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

if __name__=="__main__":
    print("Hello, world!")
    print("This is GUI.")

class window(QWidget):
    def __init__(self,name):
        super().__init__()
        self.name=name
        self.init_UI(self)
    def init_UI(self,name):
        self.setwindowTitle(name)
        self.show()

app=QApplication(sys.argv)
main_window=window("Millstone")
sys.exit(app.exec_())