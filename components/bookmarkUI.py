# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bookmarkTestUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_tabWidget(object):
    def setupUi(self, tabWidget):
        tabWidget.setObjectName("tabWidget")
        tabWidget.resize(150, 20)
        tabWidget.setMinimumSize(QtCore.QSize(10, 20))
        tabWidget.setMaximumSize(QtCore.QSize(150, 20))
        self.horizontalLayout = QtWidgets.QHBoxLayout(tabWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget_2 = QtWidgets.QWidget(tabWidget)
        self.tabWidget_2.setMinimumSize(QtCore.QSize(10, 20))
        self.tabWidget_2.setMaximumSize(QtCore.QSize(150, 20))
        self.tabWidget_2.setStyleSheet("QWidget{\n"
"    background-color:rgb(35, 34, 39);\n"
"    color:rgb(200, 200, 200);\n"
"    padding:2px;\n"
"}")
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tabWidget_2)
        self.horizontalLayout_2.setContentsMargins(3, 0, 3, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabLabel = QtWidgets.QLabel(self.tabWidget_2)
        self.tabLabel.setMinimumSize(QtCore.QSize(10, 25))
        self.tabLabel.setMaximumSize(QtCore.QSize(150, 25))
        self.tabLabel.setObjectName("tabLabel")
        self.horizontalLayout_2.addWidget(self.tabLabel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.tabWidget_2)

        self.retranslateUi(tabWidget)
        QtCore.QMetaObject.connectSlotsByName(tabWidget)

    def retranslateUi(self, tabWidget):
        _translate = QtCore.QCoreApplication.translate
        tabWidget.setWindowTitle(_translate("tabWidget", "Form"))
        self.tabLabel.setText(_translate("tabWidget", "test"))
