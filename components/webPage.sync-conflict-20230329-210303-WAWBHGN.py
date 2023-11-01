import os
import random

from PyQt6 import QtCore, QtGui, QtWidgets, Qt
from PyQt6.QtCore import QUrl, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWebEngineWidgets import QWebEnginePage, QWebEngineView, QWebEngineSettings
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QApplication
from components.webPageUi import Ui_wpWidget
from components import bookmark
from components.page import WebEnginePage as Page
from extensions import BrowserUtilities, Bypasses, UserAgentGenerator
from Settings import menubarsettings


class WebPage(QtWidgets.QWidget, Ui_wpWidget):
    webkeyevent = QtCore.pyqtSignal(Qt.QKeyEvent)
    urlChanged = QtCore.pyqtSignal(str)
    tabImage = QtCore.pyqtSignal(str)
    openNewTab = QtCore.pyqtSignal(str)
    openNewWindow = QtCore.pyqtSignal(str)
    bookmarkAdded = QtCore.pyqtSignal(str)
    bookmarkDeleted = QtCore.pyqtSignal(str)
    controlPressed = QtCore.pyqtSignal(bool)
    settingsPageupdated = QtCore.pyqtSignal(menubarsettings.MenuBarSettings)
    SettingsBarUpdated = QtCore.pyqtSignal(menubarsettings.MenuBarSettings)
    exitevent = QtCore.pyqtSignal()
    openmenu = QtCore.pyqtSignal(bool)

    def __init__(self, menubarsettings, parent=None):
        super(WebPage, self).__init__(parent=parent)
        fontDatabase = QFontDatabase
        fontDatabase.addApplicationFont(BrowserUtilities.resource_path("Fonts\\dripicons-v2.ttf"))

        self.setupUi(self)
        self.menuBarSettings = menubarsettings
        self.bypassActive = self.menuBarSettings.bypassActive
        self.bypassException = ["google"]
        self.activeUrl = ""
        self.searchEngineUrls = ["https://www.google.com/search?q=", "https://duckduckgo.com/?q=",
                                 "https://www.bing.com/search?q=", "https://search.yahoo.com/search?p="]

        self.bookmarkList = []
        self.bookmarksBarShown = self.menuBarSettings.bookmarkShownDefault

        self.webEngineView = QWebEngineView()
        self.webEngineView.page().setBackgroundColor(QtGui.QColor(45, 45, 45, 255))
        page = Page(settings=self.menuBarSettings)

        #TEST
        # self.webEngineView.page().profile().clearHttpCache()
        # self.webEngineView.page().profile().cookieStore().deleteAllCookies()
        # print(self.webEngineView.page().profile().isOffTheRecord())
        # self.webEngineView.page().profile().setHttpCacheType(2)
        # self.webEngineView.page().profile().setPersistentCookiesPolicy(0)
        # self.webEngineView.page().profile().setCachePath("C:\\Users\\jaxb1\\AppData\\Roaming\\freedombrowser\\cache")
        # self.webEngineView.page().profile().setPersistentStoragePath("C:\\Users\\jaxb1\\AppData\\Roaming\\freedombrowser\\storage")
        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.LocalStorageEnabled, False)
        page.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, False)

        print(self.webEngineView.page().profile().httpCacheType())
        print(self.webEngineView.page().profile().cachePath())
        print(self.webEngineView.page().profile().persistentStoragePath())
        print(self.webEngineView.page().profile().httpUserAgent())


        self.controlPressed.connect(page.updatecontrol)
        self.settingsPageupdated.connect(page.updateSettings)
        page.opennewtab.connect(self.openNewTab.emit)

        self.webEngineView.setPage(page)
        self.webEngineView.setObjectName("webEngineView")
        self.verticalLayout_3.addWidget(self.webEngineView)

        self.webEngineView.urlChanged.connect(self.urlChangedCallBack)
        self.webEngineView.iconUrlChanged.connect(self.iconurlchanged)
        self.webEngineView.loadFinished.connect(self.loadFinished)
        self.webEngineView.loadStarted.connect(self.loadStarted)

        self.webEngineView.page().fullScreenRequested.connect(self.handleFullscreenRequest)

        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)

        self.webEngineView.contextMenuEvent = self.ContextMenuReplacement

        self.wpLineEdit.returnPressed.connect(self.load)
        self.wpPushButton.clicked.connect(self.backward)
        self.wpPushButton_2.clicked.connect(self.forward)
        self.wpPushButton_3.clicked.connect(self.reload)
        self.wpPushButton_4.clicked.connect(self.goHome)

        self.pushButton_2.clicked.connect(self.activeBypass)
        self.pushButton_3.clicked.connect(lambda: self.bookmarkAdded.emit(self.webEngineView.page().url().url()))
        self.pushButton.clicked.connect(self.menuVarShit)
        # if not os.path.isfile("TEST.TEST"):
        #     self.pushButton.hide()
        # else:
        #     self.pushButton.clicked.connect(self.dumpinfo)

        if not self.bypassActive:
            self.pushButton_2.setChecked(False)
            self.activeBypass()  # lazy way of starting it toggled off

        self.testpp = bookmark.bookmark()
        self.testpp.clicked.connect(self.loadAct)
        self.bookmarkList.insert(0, self.testpp)
        self.horizontalLayout_3.addWidget(self.testpp)
        self.showBookMarksBar()
        self.updateBookmarksList(["google.com"])

        self.widget_2.setMaximumWidth(0)
        self.zoom_label.setText(f"Zoom: {int(self.webEngineView.page().zoomFactor()*100)}%")
        self.checkBox.setChecked(self.menuBarSettings.brainlyMode)
        self.checkBox_2.setChecked(self.menuBarSettings.ignoreCertificateErrors)

        self.horizontalSlider.valueChanged.connect(self.updatezoom)
        #self.checkBox.clicked.connect()
        self.checkBox_2.clicked.connect(self.ignoreErrors)
        self.pushButton_4.clicked.connect(lambda: self.exitevent.emit())
        self.pushButton_5.clicked.connect(lambda: self.openNewTab.emit(""))
        self.pushButton_7.clicked.connect(lambda: self.openNewWindow.emit(""))
        self.webEngineView.page().zoomFactor()

    def updateMenuBarSettings(self, settings):
        self.menuBarSettings = settings
        self.checkBox.setChecked(self.menuBarSettings.brainlyMode)
        self.checkBox_2.setChecked(self.menuBarSettings.ignoreCertificateErrors)
    # bookmark functions

    def updateBookmarksBarVar(self, check):
        self.bookmarksBarShown = check

    def updateBookmarksList(self, urlList):

        for bookmarktodelete in self.bookmarkList:
            bookmarktodelete.setParent(None)
        self.bookmarkList = []
        for url in urlList:
            bookmarkToAdd = bookmark.bookmark()
            bookmarkToAdd.clicked.connect(self.loadbookmark)
            bookmarkToAdd.opennewtabSignal.connect(self.openNewTab.emit)
            bookmarkToAdd.opennewwindowSignal.connect(self.openNewWindow.emit)
            bookmarkToAdd.deletebookmarkSignal.connect(self.bookmarkDeleted)
            bookmarkToAdd.tabLabel.setText(url)
            self.bookmarkList.insert(0, bookmarkToAdd)
            self.horizontalLayout_3.addWidget(bookmarkToAdd)

        self.label = QtWidgets.QLabel(self.wpWidget_4)
        self.label.setMinimumSize(QtCore.QSize(0, 25))
        self.label.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)

    def showBookMarksBar(self):
        if self.bookmarksBarShown:
            self.wpWidget_4.show()
        else:
            self.wpWidget_4.hide()

    # end bookmark functions

    # context menu
    def ContextMenuReplacement(self, event):
        contextMenu = QtWidgets.QMenu(self)
        reloadAct = contextMenu.addAction("Reload")
        reloadAct.triggered.connect(self.reload)
        backAct = contextMenu.addAction("Back")
        backAct.triggered.connect(self.backward)
        forwardAct = contextMenu.addAction("Forward")
        forwardAct.triggered.connect(self.forward)

        contextMenu.addSeparator()
        savepageAct = contextMenu.addAction("Save Page As...")
        savepageAct.triggered.connect(lambda: self.webEngineView.page().toHtml(self.saveWebPage))
        # savepageplainAct = contextMenu.addAction("Save Plain Text Page As...")
        # savepageplainAct.triggered.connect(lambda: self.webEngineView.page().toPlainText(self.saveWebPage))

        if self.webEngineView.page().contextMenuData().mediaType() == 2 or self.webEngineView.page().contextMenuData().mediaType() == 3:
            contextMenu.addSeparator()
            if self.webEngineView.page().isAudioMuted():
                unmuteAct = contextMenu.addAction("Unmute")
                unmuteAct.triggered.connect(lambda: self.webEngineView.page().setAudioMuted(False))
            else:
                muteAct = contextMenu.addAction("Mute")
                muteAct.triggered.connect(lambda: self.webEngineView.page().setAudioMuted(True))

        if self.webEngineView.page().contextMenuData().linkUrl().url() != "":
            contextMenu.addSeparator()
            openAct = contextMenu.addAction("Open")
            openAct.triggered.connect(lambda: self.loadAct(self.webEngineView.page().contextMenuData().linkUrl()))
            opennewtabAct = contextMenu.addAction("Open in New Tab")
            opennewtabAct.triggered.connect(
                lambda: self.openNewTab.emit(self.webEngineView.page().contextMenuData().linkUrl().url()))
            opennewwindowAct = contextMenu.addAction("Open in New Window")
            opennewwindowAct.triggered.connect(
                lambda: self.openNewWindow.emit(self.webEngineView.page().contextMenuData().linkUrl().url()))

            contextMenu.addSeparator()
            copylinkAct = contextMenu.addAction("Copy Link")
            copylinkAct.triggered.connect(lambda: Qt.QApplication.clipboard().setText(self.webEngineView.page().contextMenuData().linkUrl().url()))

        if self.webEngineView.selectedText() != "":
            contextMenu.addSeparator()
            copyAct = contextMenu.addAction("Copy")
            copyAct.triggered.connect(lambda: Qt.QApplication.clipboard().setText(self.webEngineView.selectedText()))

        contextMenu.addSeparator()
        viewSourceAct = contextMenu.addAction("View Page Source")
        viewSourceAct.triggered.connect(lambda: self.loadAct(f"fb:view-source:{self.webEngineView.page().url().url()}"))
        # inspectAct = contextMenu.addAction("Inspect")
        # inspectAct.triggered.connect(lambda: self.webEngineView.page().setDevToolsPage(self.webEngineView.page()))

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))

    def inspectElement(self):
        self.inspector = ()
        self.inspector.setPage(self.view.page())
        self.inspector.show()

    def saveWebPage(self, test=str):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", f"{self.webEngineView.page().title()}","Hypertext Markup Language (*.html *htm);;" "All files (*.*)")

        if filename:
            with open(filename, 'w') as f:
                f.write(test)

    # end context menu

    # side menu
    def updateMenuVar(self, check):
        self.menu_open = check

    def menuVarShit(self):
        if self.menu_open:
            self.menu_open = False
        else:
            self.menu_open = True
        self.animatedToggleMenu()

    def toggleMenu(self):
        if (self.menu_open and self.widget_2.minimumWidth() == 0) \
                or (not self.menu_open and self.widget_2.minimumWidth() == 125):
            if self.menu_open:
                self.widget_2.setMinimumWidth(125)
            else:
                self.widget_2.setMinimumWidth(0)

    def animatedToggleMenu(self):
        if self.menu_open:
            start_val = 0
            end_val = 125
        else:
            start_val = 125
            end_val = 0

        self.animation = QPropertyAnimation(self.widget_2, b"minimumWidth")
        self.animation.setDuration(100)
        self.animation.setStartValue(start_val)
        self.animation.setEndValue(end_val)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()
        self.openmenu.emit(self.menu_open)

    def updatezoom(self, zoom):
        if zoom:
            self.webEngineView.page().setZoomFactor(zoom/100)
        else:
            self.webEngineView.page().setZoomFactor(self.horizontalSlider.value()/100)
        self.zoom_label.setText(f"Zoom: {int(self.webEngineView.page().zoomFactor() * 100)}%")

    def ignoreErrors(self):
        if self.checkBox_2.isChecked():
            self.menuBarSettings.ignoreCertificateErrors = True
        else:
            self.menuBarSettings.ignoreCertificateErrors = False
        self.settingsPageupdated.emit(self.menuBarSettings)
        self.SettingsBarUpdated.emit(self.menuBarSettings)

    def dumpinfo(self):

        # test = self.webEngineView.history().items()
        # for item in self.webEngineView.history().items():
        #     print(item.url())
        #     print()
        # print(self.webEngineView.zoomFactor())
        # print(self.webEngineView.iconUrl())
        # print(self.webEngineView.settings())
        # print(self.webEngineView.page().profile().httpUserAgent())
        # self.webEngineView.page().profile().setHttpUserAgent(UserAgentGenerator.getuseragent())

        # print(self.webEngineView.page().profile().AllowPersistentCookies)
        # print(self.webEngineView.page().profile().cookieStore().deleteSessionCookies())
        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.LocalStorageEnabled, False)
        #print(self.webEngineView.page().profile().persistentStoragePath()) #C:\Users\jaxb1\AppData\Local\python\QtWebEngine\Default\Local Storage\leveldb\000003.log
        # self.webEngineView.page().triggerAction(QWebEnginePage.ReloadAndBypassCache)
        # self.webEngineView.page().profile().clearHttpCache()
        # self.webEngineView.page().profile().cookieStore().deleteAllCookies()
        # print(self.webEngineView.page().profile().isOffTheRecord())
        # self.webEngineView.page().profile().setHttpCacheType(2)
        # self.webEngineView.page().profile().setPersistentCookiesPolicy(0)
        # cahcepath = f"{random.randint(1, 100000000)} cache"
        # print(cahcepath)
        # self.webEngineView.page().profile().setCachePath(cahcepath)
        # print(self.webEngineView.page().profile().cachePath())
        # pathpath = f"{random.randint(1,100000000)} storage"
        # print(pathpath)
        # self.webEngineView.page().profile().setPersistentStoragePath(pathpath)
        # print(self.webEngineView.page().profile().persistentStoragePath())
        # # self.webEngineView.deleteLater()
        # test = input("penis")
        # with os.scandir(r"C:\Users\jaxb1\AppData\Local\python\QtWebEngine\Default\Local Storage\leveldb") as files:
        #     for file in files:
        #         print(file.name)
        #         if file.name.endswith(".log"):
        #             os.remove(file)
        #             print("removing: " + file.name)
        # self.webEngineView = QWebEngineView()
        # self.webEngineView.page().setBackgroundColor(QtGui.QColor(45, 45, 45, 255))
        # page = Page(self)
        # self.controlPressed.connect(page.updatecontrol)
        # page.opennewtab.connect(self.openNewTab.emit)
        # self.webEngineView.setPage(page)
        # self.webEngineView.setObjectName("webEngineView")
        # self.verticalLayout_3.addWidget(self.webEngineView)

    def activeBypass(self):
        if self.pushButton_2.isChecked():
            self.bypassActive = True
            self.pushButton_2.setStyleSheet("""color:rgb(255,255,255);""")
        else:
            self.bypassActive = False
            self.pushButton_2.setStyleSheet("""color:rgb(69,69,69);""")

    # download functions
    def downloadhandler(self, item):
        print(item.url().url(), item.path())
        reply = QMessageBox.question(None, 'Download',
                                     f'{item.url().url()} is trying to download:\n{item.downloadFileName()}\nWould you like to download?',
                                     buttons=QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            item.accept()

    # end download functions

    # %% browser functions

    def loadFinished(self):
        if self.bypassActive:
            try:
                QtCore.QTimer.singleShot(100, self.coverUp)
                QtCore.QTimer.singleShot(250, self.coverUp)
                QtCore.QTimer.singleShot(500, self.coverUp)
                QtCore.QTimer.singleShot(1000, self.coverUp)
            except Exception as e:
                print("exception " + e)
        self.updateforwardbackwardarrows()
        self.wpPushButton_3.setText("Z")
        self.updateAdressBar()
        self.iconurlchanged(self.webEngineView.page().iconUrl())

    def loadStarted(self):
        pass
        if "#newtab" or "''" in self.webEngineView.page().url().url():
            pass
        else:
            self.updateAdressBar()
        self.wpPushButton_3.setText("9")
        self.updateforwardbackwardarrows()
        self.iconurlchanged("")

    def coverUp(self):
        if "#newtab" not in self.activeUrl:
            if "translate.goog" in self.activeUrl:
                if self.bypassActive:
                    if (self.activeUrl.split('.')[1] not in self.bypassException) and (".exe" not in self.activeUrl):
                        self.webEngineView.page().runJavaScript(
                            """
                            function remove_by_id(_id){
                            var elem = document.getElementById(_id);
                            elem.parentNode.removeChild(elem); 
                            }
                            remove_by_id("gt-nvframe");
                        """
                        )
                        self.webEngineView.page().runJavaScript(
                            """
                            let testhidude = document.evaluate("//html/body/div[1]/div[2]/div/div/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                            testhidude.singleNodeValue.remove(); 
                            """
                        )
                        self.webEngineView.page().runJavaScript(
                            """
                            let setwhat = document.evaluate("//html/body/div[1]/div[1]/h1", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                            setwhat.singleNodeValue.remove(); 
                            """)

    def iconurlchanged(self, url):
        if type(url) == QUrl:
            self.tabImage.emit(url.url())
        elif type(url) == str:
            self.tabImage.emit(url)

    def urlChangedCallBack(self, url):
        self.activeUrl = url.url()
        if "#newtab" not in url.url():
            if "translate.goog" in url.url():
                self.urlChanged.emit(Bypasses.inverse_google_translate(url.url()))
                self.wpLineEdit.setText(Bypasses.inverse_google_translate(url.url()))
            else:
                if self.bypassActive:
                    if (url.url().split('.')[1] not in self.bypassException) and (".exe" not in url.url()):
                        self.urlChanged.emit(url.url())
                        self.wpLineEdit.setText(url.url())
                        print(Bypasses.determine_bypass_url(url.url(), 1))
                        self.webEngineView.load(QUrl(Bypasses.determine_bypass_url(url.url(), 1)))
                        QtCore.QTimer.singleShot(1000, self.coverUp)
        self.updateAdressBar()

    def handleFullscreenRequest(self, request):
        if request.toggleOn():
            request.accept()
            self.verticalLayout_3.removeWidget(self.webEngineView)
            self.webEngineView.setParent(None, QtCore.Qt.Window)
            self.webEngineView.showFullScreen()
        else:
            request.accept()
            self.verticalLayout_3.addWidget(self.webEngineView)

    def updateAdressBar(self):
        if "#newtab" in self.webEngineView.page().url().url():
            self.wpLineEdit.setText("")
            self.urlChanged.emit(str("New Tab"))
        else:
            if "translate.goog" in self.webEngineView.page().url().url():
                # self.urlChanged.emit(Bypasses.inverse_google_translate(self.webEngineView.page().url().url()))
                self.urlChanged.emit(self.webEngineView.page().title())
                self.wpLineEdit.setText(Bypasses.inverse_google_translate(self.webEngineView.page().url().url()))
            else:
                # for engine in self.searchEngineUrls:
                #     if engine in self.webEngineView.page().url().url():
                #         self.wpLineEdit.setText(self.webEngineView.page().url().url())
                #         if "&" in self.webEngineView.page().url().url().split('=')[1].replace('+', ' '):
                #             self.urlChanged.emit(str(f"{self.webEngineView.page().url().url().split('=')[1].replace('+', ' ').split('&')[0]} - {self.webEngineView.page().url().url().split('.')[1].split('.')[0]}"))
                #         else:
                #             self.urlChanged.emit(str(f"{self.webEngineView.page().url().url().split('=')[1].replace('+', ' ')} - {self.webEngineView.page().url().url().split('.')[1].split('.')[0]}"))
                #         self.wpLineEdit.setCursorPosition(0)
                #         return
                self.wpLineEdit.setText(self.webEngineView.page().url().url())
                self.urlChanged.emit(self.webEngineView.page().title())
        self.wpLineEdit.setCursorPosition(0)

    def updateforwardbackwardarrows(self):
        if self.webEngineView.history().canGoForward():
            self.wpPushButton_2.setStyleSheet("""color:rgb(255, 255, 255);""")
            self.wpPushButton_2.setEnabled(True)
        else:
            self.wpPushButton_2.setStyleSheet("""color:rgb(69,69,69);""")
            self.wpPushButton_2.setDisabled(True)
        if self.webEngineView.history().canGoBack():
            self.wpPushButton.setStyleSheet("""color:rgb(255, 255, 255);""")
            self.wpPushButton.setEnabled(True)
        else:
            self.wpPushButton.setStyleSheet("""color:rgb(69,69,69);""")
            self.wpPushButton.setDisabled(True)

    def goHome(self):
        self.webEngineView.load(QtCore.QUrl("https://www.google.com/#newtab"))
        self.urlChanged.emit("New Tab")
        self.tabImage.emit("")

    def load(self):
        url = QtCore.QUrl.fromUserInput(self.wpLineEdit.text())
        if not url.url().startswith("fb:"):
            if BrowserUtilities.url_check(self.wpLineEdit.text()):
                self.webEngineView.load(url)
            else:
                url = QtCore.QUrl(f"https://www.google.com/search?q={self.wpLineEdit.text()}")
                self.webEngineView.load(url)
        else:
            self.webEngineView.load(QUrl(url.url().strip("fb:")))
        self.urlChanged.emit(str(self.wpLineEdit.text()))

    def loadAct(self, url):
        if type(url) == QUrl:
            if not url.url().startswith("fb:"):
                if BrowserUtilities.url_check(url.url()):
                    self.webEngineView.load(url)
                else:
                    url = QtCore.QUrl(f"https://www.google.com/search?q={url.url()}")
                    self.webEngineView.load(url)
            else:
                self.webEngineView.load(QUrl(url.url().strip("fb:")))
        elif type(url) == str:
            if not url.startswith("fb:"):
                if BrowserUtilities.url_check(url.replace(" ", "-")):
                    self.webEngineView.load(QUrl(url))
                else:
                    url = QtCore.QUrl(f"https://www.google.com/search?q={url}")
                    self.webEngineView.load(url)
            else:
                self.webEngineView.load(QUrl(url.strip("fb:")))
        self.urlChanged.emit(str(self.wpLineEdit.text()))

    def loadbookmark(self, url):
        if BrowserUtilities.url_check(url):
            if not url.startswith("http"):
                loadingurl = QtCore.QUrl("https://"+url)
            else:
                loadingurl = QtCore.QUrl(url)
            self.webEngineView.load(loadingurl)
        else:
            self.webEngineView.load(QtCore.QUrl(f"https://www.google.com/search?q={url}"))
        self.urlChanged.emit(str(url))
        self.wpLineEdit.setText(Bypasses.inverse_google_translate(url))

    def backward(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Back)
        self.updateforwardbackwardarrows()
        self.updateAdressBar()

    def forward(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Forward)
        self.updateforwardbackwardarrows()
        self.updateAdressBar()

    def reload(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Reload)
        if self.wpPushButton_3.text() == "Z":
            if "#newtab" not in self.webEngineView.page().url().url():
                if "translate.goog" in self.webEngineView.page().url().url():
                    if not self.bypassActive:
                        self.urlChanged.emit(Bypasses.inverse_google_translate(self.webEngineView.page().url().url()))
                        self.wpLineEdit.setText(Bypasses.inverse_google_translate(self.webEngineView.page().url().url()))
                        self.webEngineView.load(
                            QUrl(Bypasses.inverse_google_translate(self.webEngineView.page().url().url())))
                    else:
                        self.urlChanged.emit(Bypasses.inverse_google_translate(self.webEngineView.page().url().url()))
                        self.wpLineEdit.setText(Bypasses.inverse_google_translate(self.webEngineView.page().url().url()))
                else:
                    if self.bypassActive:
                        if (self.webEngineView.page().url().url().split('.')[1] not in self.bypassException) and (
                                ".exe" not in self.webEngineView.page().url().url()):
                            self.urlChanged.emit(self.webEngineView.page().url().url())
                            self.wpLineEdit.setText(self.webEngineView.page().url().url())
                            print(Bypasses.determine_bypass_url(self.webEngineView.page().url().url(), 1))
                            self.webEngineView.load(
                                QUrl(Bypasses.determine_bypass_url(self.webEngineView.page().url().url(), 1)))
                            QtCore.QTimer.singleShot(1000, self.coverUp)
        else:
            self.webEngineView.page().triggerAction(QWebEnginePage.Stop)

    def openlinkinnewtab(self):
        self.openNewTab.emit(self.webEngineView.page().contextMenuData().linkUrl().url())

    def keyPressEvent(self, event):
        self.webkeyevent.emit(event)
        if event.key() == QtCore.Qt.Key_Control:
            self.controlPressed.emit(True)

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Control:
            self.controlPressed.emit(False)

    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        print("penis")
        if QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
          self.zoom_label.setText(f"Zoom: {int(self.webEngineView.page().zoomFactor() * 100)}%")

    # end browser functions