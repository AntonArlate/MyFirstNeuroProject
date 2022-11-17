# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\GBWorks\Python\MyNrutoProject\test_UI\untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.



from asyncio import sleep
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

a = 53

class call:
    def incr():
        global a
        a += 1


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 30, 701, 31))
        self.label.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(100, 100, 100);")
        self.label.setObjectName("label")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(230, 220, 391, 161))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.inc = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.inc.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(100, 100, 100);")
        self.inc.setObjectName("inc")
        self.verticalLayout.addWidget(self.inc)
        self.clear = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.clear.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(100, 100, 100);")
        self.clear.setObjectName("clear")
        self.verticalLayout.addWidget(self.clear)
        self.dec = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.dec.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(100, 100, 100);")
        self.dec.setObjectName("dec")
        self.verticalLayout.addWidget(self.dec)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        self.result = 0
        self.add_functions()




        # global a
        # for i in range(1000):
        #     a += 1
        #     print (i)
        #     self.upd(a)
    

    def upd (self):
        self.label.setText(str(a))



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Calc"))
        self.label.setText(_translate("MainWindow", "0"))
        self.inc.setText(_translate("MainWindow", "+1"))
        self.clear.setText(_translate("MainWindow", "clear"))
        self.dec.setText(_translate("MainWindow", "-1"))

    def add_functions(self):
        self.inc.clicked.connect(lambda: self.change_number(1))
        self.dec.clicked.connect(lambda: self.change_number(-1))
        self.clear.clicked.connect(lambda: self.change_number(0))

    def change_number(self, num):
        if num == 0: self.result = 0
        elif num > 0:
            self.result += 1
    


        self.label.setText(str(self.result))
        # print(self.result)





if __name__ == '__main__':


    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    print (ui)
    ui.setupUi(MainWindow)

    MainWindow.show()



    sys.exit(app.exec_())

