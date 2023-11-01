import os
import subprocess
import sys
import typing

from PyQt5 import QtCore, QtWidgets
import sys

from PyQt5.QtCore import Qt, QEvent, QCoreApplication
from PyQt5.QtGui import QMouseEvent

from PyQt5.QtWidgets import QApplication, QToolBar, QAction, QWidget, QLabel


from Settings import menubarsettings
from UI import mainUI
from components import titleBar, tab, webPage, bookmarksBar
from extensions import BrowserUtilities, Bypasses, EULA
from qframelesswindow import FramelessWindow


class BrowserApp(mainUI.Ui_Form, FramelessWindow):# QtWidgets.QWidget):
    bookmarkSignal = QtCore.pyqtSignal(bool)
    toggleMenuSignal = QtCore.pyqtSignal(bool)
    bookmarkupdatedSignal = QtCore.pyqtSignal(list)
    bookmarkupdateGloablSignal = QtCore.pyqtSignal(list)
    OpenNewWindowSignal = QtCore.pyqtSignal(str)
    updateMenuBarSignal = QtCore.pyqtSignal(menubarsettings.MenuBarSettings)

    BORDER_WIDTH = 8

    def __init__(self):
        super(BrowserApp, self).__init__()
        self.titleBar.raise_()
        self.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        QApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
        self.setWindowTitle("Freedom Browser")

        self.browserid = -1

        self.menuToggle = False
        self.menuToggleSettings = menubarsettings.MenuBarSettings()

        self.bookmarkBarShown = self.menuToggleSettings.bookmarkShownDefault
        self.bookmarkList = ["www.google.com", "https://brainly.com/question/18086799", "https://brainly.com/app/ask?q=test", "speedtest.net", "192.168.1.1",
                             "shuba duck", "https://bbs.archlinux.org/viewtopic.php?id=235384"]


        self.tabDict = {}
        self.tabId = 0
        self.actTab = 0
        self.tabCount = 0

        self.tBar = titleBar.TitleBar(self)
        self.verticalLayout.addWidget(self.tBar)
        self.tBar.tbPushButton_4.clicked.connect(self.addTab)
        self.tBar.onExit.connect(lambda: exitApp(form=self, browserid=self.browserid))

    def updateMenuBarSettings(self, setting):
        self.menuToggleSettings = setting
        self.updateMenuBarSignal.emit(self.menuToggleSettings)

    def newTabWindow(self, url):
        self.addTab(url)
        self.selTab(self.tabId-1)

    def toggleMenu(self, var):
        self.menuToggle = var
        self.toggleMenuSignal.emit(self.menuToggle)

    def setbookmarks(self, bookmarks):
        if bookmarks != self.bookmarkList:
            self.bookmarkList.clear()
            for item in bookmarks:
                self.bookmarkList.append(item)
            pass
            self.bookmarkupdatedSignal.emit(self.bookmarkList)

    def addbookmarks(self, bookmarktoadd):
        self.bookmarkList.append(bookmarktoadd)
        self.bookmarkupdatedSignal.emit(self.bookmarkList)
        self.bookmarkupdateGloablSignal.emit(self.bookmarkList)

    def removebookmarks(self, bookmarktoremove):
        self.bookmarkList.remove(bookmarktoremove)
        self.bookmarkupdatedSignal.emit(self.bookmarkList)
        self.bookmarkupdateGloablSignal.emit(self.bookmarkList)

    def addTab(self, url_to_open=""):
        try:
            self.tabDict[self.actTab][0].setActive(0)
            self.tabDict[self.actTab][1].hide()
        except:
            pass

        tabB = tab.Tab()
        tabB.setId(self.tabId)
        self.tBar.insertTab(tabB)
        page = webPage.WebPage(menubarsettings=self.menuToggleSettings)
        self.verticalLayout.addWidget(page)
        page.menubarSettings = self.menuToggleSettings
        page.urlChanged.connect(tabB.updateTitleBar)
        page.tabImage.connect(tabB.updateimage)
        page.openNewTab.connect(self.newTabWindow)
        page.openNewWindow.connect(self.OpenNewWindowSignal.emit)
        page.openmenu.connect(self.toggleMenu)
        page.SettingsBarUpdated.connect(self.updateMenuBarSettings)

        # bookmarks bar
        self.bookmarkSignal.connect(page.updateBookmarksBarVar)
        self.bookmarkupdatedSignal.connect(page.updateBookmarksList)
        self.toggleMenuSignal.connect(page.updateMenuVar)
        self.updateMenuBarSignal.connect(page.updateMenuBarSettings)
        page.webkeyevent.connect(self.keyPressEvent)
        page.bookmarkAdded.connect(self.addbookmarks)
        page.bookmarkDeleted.connect(self.removebookmarks)
        page.exitevent.connect(lambda: exitApp())
        page.bookmarksBarShown = self.bookmarkBarShown
        page.menu_open = self.menuToggle
        page.updateBookmarksList(self.bookmarkList)
        page.toggleMenu()
        #page.showBookMarksBar()

        page.wpLineEdit.setFocus()

        self.actTab = self.tabId
        self.tabDict[self.tabId] = [tabB, page]
        tabB.clicked.connect(self.selTab)
        tabB.tabPushButton.clicked.connect(self.delTab)

        self.tabId += 1
        self.tabCount += 1
        if url_to_open != "" and type(url_to_open) == str:
            page.loadAct(QtCore.QUrl(url_to_open))
        else:
            page.goHome()

    def selTab(self, tId):
        try:
            self.tabDict[self.actTab][0].setActive(0)
            self.tabDict[self.actTab][1].hide()
            self.tabDict[self.actTab][1].wpWidget_4.hide()
        except:
            pass
        self.tabDict[tId][0].setActive(1)
        self.tabDict[tId][1].showBookMarksBar()
        self.tabDict[tId][1].toggleMenu()
        self.tabDict[tId][1].show()
        self.actTab = tId

    def delTab(self):
        dId = int(self.sender().objectName())
        temp = list(self.tabDict)
        tempId = temp.index(dId)
        lastId = len(temp) - 1
        if self.tabCount > 1:
            if dId == self.actTab:
                if lastId > tempId:
                    sId = temp[tempId + 1]
                else:
                    sId = temp[tempId - 1]
                self.selTab(sId)
            self.tabDict[dId][0].deleteLater()
            self.tabDict[dId][1].deleteLater()
            self.tabDict.pop(dId)
            self.tabCount -= 1
        else:
            if dId == self.actTab:
                if lastId > tempId:
                    sId = temp[tempId + 1]
                else:
                    sId = temp[tempId - 1]
                self.selTab(sId)
            self.tabDict[dId][0].deleteLater()
            self.tabDict[dId][1].delete()
            self.tabDict.pop(dId)
            self.tabCount -= 1

            pass#exitApp(form=self, browserid=self.browserid)

    def delTabBinding(self, id):
        dId = id
        temp = list(self.tabDict)
        tempId = temp.index(dId)
        lastId = len(temp) - 1
        if self.tabCount > 1:
            if dId == self.actTab:
                if lastId > tempId:
                    sId = temp[tempId + 1]
                else:
                    sId = temp[tempId - 1]
                self.selTab(sId)
            self.tabDict[dId][0].deleteLater()
            self.tabDict[dId][1].deleteLater()
            self.tabDict.pop(dId)
            self.tabCount -= 1
        else:
            exitApp(form=self, browserid=self.browserid)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_T:
            if QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
                self.addTab()
        if event.key() == QtCore.Qt.Key_W:
            if QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
                self.delTabBinding(self.actTab)
        if event.key() == QtCore.Qt.Key_Tab:
            if QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
                if self.actTab < self.tabCount - 1:
                    self.selTab(self.actTab + 1)
                elif self.actTab == self.tabCount - 1:
                    self.selTab(0)
        if event.key() == QtCore.Qt.Key_B:
            if QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
                if self.bookmarkBarShown:
                    self.bookmarkSignal.emit(False)
                    self.bookmarkBarShown = False
                    self.tabDict[self.actTab][1].showBookMarksBar()
                else:
                    self.bookmarkSignal.emit(True)
                    self.bookmarkBarShown = True
                    self.tabDict[self.actTab][1].showBookMarksBar()


class Browser(QtCore.QThread):
    bookmarkSignal = QtCore.pyqtSignal(bool)
    bookmarkupdatedSignal = QtCore.pyqtSignal(list)
    exitSignal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.windowDict = {}
        self.windowCount = -1
        self.bookmarkBarShown = False
        self.globalBookmarks = []

    def setupalone(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.opennewwindow()
        self.app.exec()

    def opennewwindow(self, url=""):
        form = BrowserApp()
        form.OpenNewWindowSignal.connect(self.opennewwindow)

        form.browserid = self.windowCount
        if url != "":
            form.newTabWindow(url)
        else:
            form.addTab()
        form.bookmarkupdateGloablSignal.connect(self.updatebookmarksGlobal)
        self.bookmarkupdatedSignal.connect(form.setbookmarks)
        form.show()

        self.windowDict[self.windowCount] = form
        self.windowCount += 1

    def updatebookmarksGlobal(self, bookmarklist):
        self.globalBookmarks = bookmarklist
        self.bookmarkupdatedSignal.emit(bookmarklist)

    def exitSignalSender(self):
        self.exitSignal.emit()


browser = Browser()


def exitApp(exitCode=1337, form=None, browserid=-1):

    if browser.windowCount == 0:
        if __name__ == '__main__':
            sys.exit(exitCode)
        else:
            browser.exitSignalSender()
            subprocess.call(f'taskkill /f /IM "{os.path.basename(__file__).replace(".py", ".exe")}"',
                            creationflags=0x08000000)
            sys.exit(exitCode)
    else:
        form.hide()
        browser.windowDict.pop(browserid)
        browser.windowCount -= 1


def start():
    # create the instance of our Window
    browser.opennewwindow()


if __name__ == '__main__':
    browser.setupalone()

