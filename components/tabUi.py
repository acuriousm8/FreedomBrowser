


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_tabWidget(object):

    def setupUi(self, tabWidget):
        tabWidget.setObjectName("tabWidget")
        tabWidget.resize(180, 35)
        tabWidget.setMinimumSize(QtCore.QSize(40, 35))
        tabWidget.setMaximumSize(QtCore.QSize(180, 35))
        self.horizontalLayout = QtWidgets.QHBoxLayout(tabWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget_2 = QtWidgets.QWidget(tabWidget)
        self.tabWidget_2.setMinimumSize(QtCore.QSize(40, 35))
        self.tabWidget_2.setMaximumSize(QtCore.QSize(180, 35))
        self.tabWidget_2.setStyleSheet("QWidget{\n"
"    background-color:rgb(35, 34, 39);\n"
"    color:rgb(170, 170, 170);\n"
"    border-top-left-radius:5px;\n"
"    border-top-right-radius:5px;\n"
"    padding:2px;\n"
"}")
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tabWidget_2)
        self.horizontalLayout_2.setContentsMargins(3, 0, 3, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.label = QtWidgets.QLabel(self.tabWidget_2)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QtCore.QSize(0,0))
        self.label.setMaximumSize(QtCore.QSize(15,15))
        self.horizontalLayout_2.addWidget(self.label)

        self.tabLabel = QtWidgets.QLabel(self.tabWidget_2)
        self.tabLabel.setMinimumSize(QtCore.QSize(10, 25))
        self.tabLabel.setMaximumSize(QtCore.QSize(150, 25))
        self.tabLabel.setObjectName("tabLabel")
        self.horizontalLayout_2.addWidget(self.tabLabel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.tabPushButton = QtWidgets.QPushButton(self.tabWidget_2)
        self.tabPushButton.setMinimumSize(QtCore.QSize(25, 25))
        self.tabPushButton.setMaximumSize(QtCore.QSize(25, 25))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.tabPushButton.setFont(font)
        self.tabPushButton.setStyleSheet("QPushButton{\n"
"    background-color:rgba(0, 0, 0, 0);\n"
"    color:rgb(144, 144, 144);\n"
"}\n"
"QPushButton:hover{\n"
"    color:rgb(255, 255, 255);\n"
"}\n"
"QPushButton:pressed{\n"
"    padding-top:5px;\n"
"    padding-left:5px;\n"
"}")
        self.tabPushButton.setObjectName("-1")
        self.horizontalLayout_2.addWidget(self.tabPushButton)
        self.horizontalLayout.addWidget(self.tabWidget_2)

        self.retranslateUi(tabWidget)
        QtCore.QMetaObject.connectSlotsByName(tabWidget)

    def retranslateUi(self, tabWidget):
        _translate = QtCore.QCoreApplication.translate
        tabWidget.setWindowTitle(_translate("tabWidget", "Form"))
        self.tabLabel.setText(_translate("tabWidget", "New Tab"))
        self.tabPushButton.setText(_translate("tabWidget", "x"))
