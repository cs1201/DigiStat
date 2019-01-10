from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(800, 132)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.textBrowser_1 = QtWidgets.QTextBrowser(self.centralwidget)
        self.horizontalLayout.addWidget(self.textBrowser_1)
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.horizontalLayout.addWidget(self.textBrowser_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


class MyMainScreen(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()  # This is from a python export from QtDesigner
        self.ui.setupUi(self)
        # self.setMouseTracking(True)
        self.ui.textBrowser_1.installEventFilter(self)
        # self.ui.textBrowser_1.setMouseTracking(True)
        # self.ui.menubar.setMouseTracking(True)
        # self.ui.statusbar.setMouseTracking(True)

    # def setMouseTracking(self, flag):
    #     def recursive_set(parent):
    #         for child in parent.findChildren(QtCore.QObject):
    #             try:
    #                 child.setMouseTracking(flag)
    #             except:
    #                 pass
    #             recursive_set(child)
    #     QtWidgets.setMouseTracking(self, flag)
    #     recursive_set(self)

    def mouseMoveEvent(self, event):
        self.ui.textBrowser_1.setText(str(event.x()))
        self.ui.textBrowser_2.setText(str(event.y()))
        QtWidgets.QMainWindow.mouseMoveEvent(self, event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainscreen = MyMainScreen()
    mainscreen.show()
    app.exec_()