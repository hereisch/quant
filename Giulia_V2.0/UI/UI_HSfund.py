# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_HSfund.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HSfund(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1800, 1000)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1586, 976))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelPrice = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.labelPrice.setMaximumSize(QtCore.QSize(80, 50))
        self.labelPrice.setObjectName("labelPrice")
        self.horizontalLayout.addWidget(self.labelPrice)
        self.minPrice = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.minPrice.setMaximumSize(QtCore.QSize(80, 50))
        self.minPrice.setObjectName("minPrice")
        self.horizontalLayout.addWidget(self.minPrice)
        self.label_ = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_.setMaximumSize(QtCore.QSize(50, 50))
        self.label_.setObjectName("label_")
        self.horizontalLayout.addWidget(self.label_)
        self.maxPrice = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.maxPrice.setMaximumSize(QtCore.QSize(80, 50))
        self.maxPrice.setObjectName("maxPrice")
        self.horizontalLayout.addWidget(self.maxPrice)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.labelChange = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.labelChange.setObjectName("labelChange")
        self.horizontalLayout.addWidget(self.labelChange)
        self.minChange = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.minChange.setMaximumSize(QtCore.QSize(80, 50))
        self.minChange.setObjectName("minChange")
        self.horizontalLayout.addWidget(self.minChange)
        self.label_Change = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_Change.setMaximumSize(QtCore.QSize(50, 50))
        self.label_Change.setObjectName("label_Change")
        self.horizontalLayout.addWidget(self.label_Change)
        self.maxChange = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.maxChange.setMaximumSize(QtCore.QSize(80, 50))
        self.maxChange.setObjectName("maxChange")
        self.horizontalLayout.addWidget(self.maxChange)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.sortZLJE = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.sortZLJE.setMaximumSize(QtCore.QSize(100, 50))
        self.sortZLJE.setObjectName("sortZLJE")
        self.horizontalLayout.addWidget(self.sortZLJE)
        self.sortZLJZB = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.sortZLJZB.setMaximumSize(QtCore.QSize(100, 50))
        self.sortZLJZB.setObjectName("sortZLJZB")
        self.horizontalLayout.addWidget(self.sortZLJZB)
        self.sortCDJE = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.sortCDJE.setMaximumSize(QtCore.QSize(100, 50))
        self.sortCDJE.setObjectName("sortCDJE")
        self.horizontalLayout.addWidget(self.sortCDJE)
        self.sortCDJZB = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.sortCDJZB.setMaximumSize(QtCore.QSize(100, 50))
        self.sortCDJZB.setObjectName("sortCDJZB")
        self.horizontalLayout.addWidget(self.sortCDJZB)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.comboBox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.comboBox.setMaximumSize(QtCore.QSize(150, 100))
        self.comboBox.setCurrentText("")
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.DownButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.DownButton.setMaximumSize(QtCore.QSize(200, 100))
        self.DownButton.setObjectName("DownButton")
        self.horizontalLayout.addWidget(self.DownButton)
        self.RefreshButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.RefreshButton.setMaximumSize(QtCore.QSize(200, 100))
        self.RefreshButton.setObjectName("RefreshButton")
        self.horizontalLayout.addWidget(self.RefreshButton)
        self.SearchButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.SearchButton.setMaximumSize(QtCore.QSize(200, 100))
        self.SearchButton.setIconSize(QtCore.QSize(10, 20))
        self.SearchButton.setObjectName("SearchButton")
        self.horizontalLayout.addWidget(self.SearchButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.splitter_2 = QtWidgets.QSplitter(self.scrollAreaWidgetContents)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setOpaqueResize(True)
        self.splitter_2.setObjectName("splitter_2")
        self.stockTable = QtWidgets.QTableView(self.splitter_2)
        self.stockTable.setMinimumSize(QtCore.QSize(0, 250))
        self.stockTable.setObjectName("stockTable")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.verticalLayout.addWidget(self.splitter_2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.addWidget(self.scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1610, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.sortZLJE.setChecked(True)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HSfund"))
        self.labelPrice.setText(_translate("MainWindow", "价格区间："))
        self.label_.setText(_translate("MainWindow", "-"))
        self.labelChange.setText(_translate("MainWindow", "涨幅："))
        self.label_Change.setText(_translate("MainWindow", "-"))
        self.sortZLJE.setText(_translate("MainWindow", "主力净额↓"))
        self.sortZLJZB.setText(_translate("MainWindow", "主力净占比↓"))
        self.sortCDJE.setText(_translate("MainWindow", "超大净额↓"))
        self.sortCDJZB.setText(_translate("MainWindow", "超大净占比↓"))
        self.DownButton.setText(_translate("MainWindow", "下载"))
        self.RefreshButton.setText(_translate("MainWindow", "刷新现价"))
        self.SearchButton.setText(_translate("MainWindow", "Search"))