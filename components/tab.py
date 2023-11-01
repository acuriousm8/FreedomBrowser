from urllib.request import urlopen, Request
from urllib.error import URLError
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from components.tabUi import Ui_tabWidget


class Tab(QtWidgets.QWidget, Ui_tabWidget):
    clicked = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(Tab, self).__init__(parent=parent)
        self.setupUi(self)

    def setActive(self, act):
        if act == 0:
            self.tabWidget_2.setStyleSheet("QWidget{\n"
"    background-color:rgba(0, 0, 0, 0);\n"
"    color:rgb(144, 144, 144);\n"
"    padding:2px;\n"
"}QWidget:hover{\n"
"    background-color:rgb(25, 25, 25);\n"
"    border-top-left-radius:5px;\n"
"    border-top-right-radius:5px;\n"
"}")
        else:
            self.tabWidget_2.setStyleSheet("QWidget{\n"
"    background-color:rgb(35, 34, 39);\n"
"    color:rgb(170, 170, 170);\n"
"    border-top-left-radius:5px;\n"
"    border-top-right-radius:5px;\n"
"    padding:2px;\n"
"}")

    def updateTitleBar(self, title):
        self.tabLabel.setText(title)

    def updateimage(self, url):
        if url != "" and self.tabLabel.text() != "New Tab":
            try:
                r = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/5.15.2 Chrome/83.0.4103.122 Safari/537.36'})
                data = urlopen(r).read()
                pixmap = QPixmap()
                pixmap.loadFromData(data)
                self.label.setScaledContents(True)
                self.label.setPixmap(pixmap)
            except URLError as test:
                print("favicon error: " + str(test))
                self.label.setText("")
        else:
            self.label.setText("")

    def setId(self, bId):
        self.tabPushButton.setObjectName(str(bId))

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit(int(self.tabPushButton.objectName()))
