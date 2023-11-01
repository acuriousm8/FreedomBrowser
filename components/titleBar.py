
from PyQt5 import QtCore, QtGui, QtWidgets
from components.titleBarUi import Ui_tbWidget
from components.movableLabel import MovableLabel
import sys


class TitleBar(QtWidgets.QWidget, Ui_tbWidget):
    onExit = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(TitleBar, self).__init__(parent=parent)
        self.setupUi(self)
        self.parent = parent
        self.tbLabel_2.mainWindow = self.parent
        self.tbLabel_3.mainWindow = self.parent
        self.tbLabel_4.mainWindow = self.parent
        self.tbLabel_5.mainWindow = self.parent
        self.tbLabel_6.mainWindow = self.parent
        self.tbLabel_7.mainWindow = self.parent

        self.tbPushButton.clicked.connect(self.parent.showMinimized)
        self.tbPushButton_2.clicked.connect(self.winShowMaximized)
        self.tbPushButton_3.clicked.connect(lambda: self.onExit.emit())

        self.tbLabel_7.movingWindow.connect(self.windowMovedEvent)
        self.tbLabel_6.movingWindow.connect(self.windowMovedEvent)
        self.tbLabel_5.movingWindow.connect(self.windowMovedEvent)
        self.tbLabel_4.movingWindow.connect(self.windowMovedEvent)
        self.tbLabel_3.movingWindow.connect(self.windowMovedEvent)
        self.tbLabel_2.movingWindow.connect(self.windowMovedEvent)

        self.tbLabel_2.doubleClickedSignal.connect(self.winShowMaximized)
        self.tbLabel_5.doubleClickedSignal.connect(self.winShowMaximized)
        self.tbLabel_7.doubleClickedSignal.connect(self.winShowMaximized)

    def winShowMaximized(self):
        if self.window().isMaximized():
            self.window().showNormal()
            self.tbPushButton_2.setText("")
        else:
            self.tbPushButton_2.setText(";")
            self.window().showMaximized()
        # if not self.parent.isMaximized():
        #     self.parent.showMaximized()
        #     self.parent.showNormal()
        #     self.parent.showMaximized()
        #     self.tbPushButton_2.setText(";")
        # else:
        #     self.parent.showNormal()
        #     self.tbPushButton_2.setText("")

    def windowMovedEvent(self):
        # self.parent.showNormal()
        # self.tbPushButton_2.setText("")
        # if self.parent.isMaximized():
        #     self.parent.showMaximized()
        #     self.parent.showNormal()
        if self.window().isMaximized():
            self.tbPushButton_2.setText(";")
        else:
            self.tbPushButton_2.setText("")

    def insertTab(self, widget):
        self.horizontalLayout.addWidget(widget)
