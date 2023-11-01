from PyQt5 import QtCore, QtWebEngineWidgets, QtGui, Qt
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtWidgets import QMessageBox
from Settings import menubarsettings


class WebEnginePage(QWebEnginePage):
    opennewtab = QtCore.pyqtSignal(str)
    control_pressed = False
    test = []

    def __init__(self, settings, *args, **kwargs):
        QWebEnginePage.__init__(self, *args, **kwargs)
        self.geometryChangeRequested.connect(self.handleGeometryChange)
        self.menuBarSettings = settings

    def updatecontrol(self, pressed):
        self.control_pressed = pressed

    def updateSettings(self, settings):
        self.menuBarSettings = settings

    def certificateError(self, error):
        if self.menuBarSettings.ignoreCertificateErrors:
            return True
        reply = QMessageBox.question(None, 'Error',
                                     f'An error has occurred: Certificate Error\nWould you like to ignore it?',
                                     buttons=QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            error.ignoreCertificateError()
            return True
        else:
            return False

    _windows = {}

    # @classmethod
    # def newWindow(cls):
    #     pP = QtCore.pyqtSignal(str)
    #     window = QWebEngineView()
    #     window.setObjectName(f'window-{id(window)}')
    #     window.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
    #     window.destroyed.connect(
    #         lambda window: cls._windows.pop(window.objectName(), None))
    #     window.setPage(cls(window))
    #     window.loadStarted.connect(lambda x: cls.pp.emit(window.page().url().url()))
    #     cls._windows[window.objectName()] = window
    #     return window


    def handleGeometryChange(self, rect):
        view = self.view()
        window = QtGui.QWindow.fromWinId(view.winId())
        if window is not None:
            rect = rect.marginsRemoved(window.frameMargins())
        view.resize(rect.size())
        view.show()

    def createWindow(self, mode):
        print("Test")
        window = self.newWindow()
        window.pP.connect("")
        if mode != QtWebEngineWidgets.QWebEnginePage.WebDialog:
            pass
        return window.page()

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if _type == QWebEnginePage.NavigationTypeLinkClicked:
            if self.control_pressed:
                self.opennewtab.emit(url.url())
                return False
        #print(url.url())
       #print(self.test)
        if url.url() in self.test:
            return False
        return super().acceptNavigationRequest(url, _type, isMainFrame)
