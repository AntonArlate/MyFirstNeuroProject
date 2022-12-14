from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

import sys

perem = [0]

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        
        self.setWindowTitle("тестовое окно")
        self.setGeometry(300, 250, 350, 200)

        self.perem = 0

        self.main_text = QtWidgets.QLabel(self)
        # self.main_text.setText(str(self.perem))
        self.main_text.move(100, 100)
        self.main_text.adjustSize()

        self.btn = QtWidgets.QPushButton(self)
        self.btn.move(70, 150)
        self.btn.setText("+1")
        self.btn.setFixedWidth(200)
        self.btn.clicked.connect(self.add_label)

    def add_label(self):
        self.perem += 1
        self.main_text.setText(str(self.perem))
        self.main_text.adjustSize()

    

def application():
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    application()