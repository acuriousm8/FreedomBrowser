import sys

from PyQt5 import QtWidgets, QtCore
if sys.platform == "win32":
    import win32con
    from win32api import SendMessage
    from win32gui import ReleaseCapture


class MovableLabel(QtWidgets.QLabel):
    mainWindow = None
    movingWindow = QtCore.pyqtSignal()
    doubleClickedSignal = QtCore.pyqtSignal()

    def __init__(self, parent = None):
        super(MovableLabel, self).__init__(parent = parent)
        self.parent = parent

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.mainWindow.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            ReleaseCapture()
            SendMessage(self.window().winId(), win32con.WM_SYSCOMMAND,
                        win32con.SC_MOVE | win32con.HTCAPTION, 0)
            self.movingWindow.emit()
            event.ignore()
            # self.mainWindow.move(event.globalPos() - self.dragPosition)
            # event.accept()


    def mouseDoubleClickEvent(self, QMouseEvent):
        self.doubleClickedSignal.emit()
