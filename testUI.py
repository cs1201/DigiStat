# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './DigiStat.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(320, 240)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        MainWindow.setFont(font)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Btn_Up = QtWidgets.QPushButton(self.centralwidget)
        self.Btn_Up.setGeometry(QtCore.QRect(240, 40, 51, 51))
        self.Btn_Up.setObjectName("Btn_Up")
        self.Btn_Down = QtWidgets.QPushButton(self.centralwidget)
        self.Btn_Down.setGeometry(QtCore.QRect(240, 130, 51, 51))
        self.Btn_Down.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.Btn_Down.setObjectName("Btn_Down")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 320, 240))
        self.graphicsView.setObjectName("graphicsView")
        self.Label_Temp = QtWidgets.QLabel(self.centralwidget)
        self.Label_Temp.setGeometry(QtCore.QRect(100, 70, 61, 71))
        font = QtGui.QFont()
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.Label_Temp.setFont(font)
        self.Label_Temp.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Label_Temp.setObjectName("Label_Temp")
        self.Label_Unit = QtWidgets.QLabel(self.centralwidget)
        self.Label_Unit.setGeometry(QtCore.QRect(160, 70, 31, 41))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.Label_Unit.setFont(font)
        self.Label_Unit.setAlignment(QtCore.Qt.AlignCenter)
        self.Label_Unit.setObjectName("Label_Unit")
        self.graphicsView.raise_()
        self.Btn_Up.raise_()
        self.Btn_Down.raise_()
        self.Label_Temp.raise_()
        self.Label_Unit.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Btn_Up.setText(_translate("MainWindow", "+"))
        self.Btn_Down.setText(_translate("MainWindow", "-"))
        self.Label_Temp.setText(_translate("MainWindow", "23"))
        self.Label_Unit.setText(_translate("MainWindow", "°C"))

