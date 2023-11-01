
from PyQt5 import QtCore, QtGui, QtWidgets
from components.bookmarksBarUi import Ui_Form


class bookmarkBar(QtWidgets.QWidget, Ui_Form):
    clicked = QtCore.pyqtSignal(int)

    def __init__(self, parent = None):
        super(bookmarkBar, self).__init__(parent = parent)
        self.setupUi(self)

