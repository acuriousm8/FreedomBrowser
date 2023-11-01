
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QInputDialog
from components.bookmarkUI import Ui_tabWidget


class bookmark(QtWidgets.QWidget, Ui_tabWidget):
    clicked = QtCore.pyqtSignal(str)
    opennewtabSignal = QtCore.pyqtSignal(str)
    opennewwindowSignal = QtCore.pyqtSignal(str)
    deletebookmarkSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(bookmark, self).__init__(parent=parent)
        self.setupUi(self)
        self.contextMenuEvent = self.ContextMenu

    def ContextMenu(self, event):
        contextMenu = QtWidgets.QMenu(self)
        openAct = contextMenu.addAction("Open")
        openAct.triggered.connect(lambda: self.clicked.emit(str(self.tabLabel.text())))
        opennewtabAct = contextMenu.addAction("Open in New Tab")
        opennewtabAct.triggered.connect(lambda: self.opennewtabSignal.emit(str(self.tabLabel.text())))
        opennewwindowAct = contextMenu.addAction("Open in New Window")
        opennewwindowAct.triggered.connect(lambda: self.opennewwindowSignal.emit(str(self.tabLabel.text())))

        contextMenu.addSeparator()

        editAct = contextMenu.addAction("Edit Bookmark")
        editAct.triggered.connect(self.modifybookmark)
        deleteAct = contextMenu.addAction("Delete Bookmark")
        deleteAct.triggered.connect(lambda: self.deletebookmarkSignal.emit(str(self.tabLabel.text())))
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))

    def modifybookmark(self):
        text, ok = QInputDialog.getText(self, 'Edit Bookmark', 'URL:')
        if ok:
            self.tabLabel.setText(text)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit(str(self.tabLabel.text()))
