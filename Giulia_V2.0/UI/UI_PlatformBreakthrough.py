# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_HSfund.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PlatformBreakthrough(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 1000)
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

        self.labelNMC = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.labelNMC.setObjectName("labelNMC")
        self.horizontalLayout.addWidget(self.labelNMC)
        self.minNMC = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.minNMC.setMaximumSize(QtCore.QSize(80, 50))
        self.minNMC.setObjectName("minNMC")
        self.horizontalLayout.addWidget(self.minNMC)
        self.label_NMC = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_NMC.setMaximumSize(QtCore.QSize(50, 50))
        self.label_NMC.setObjectName("label_NMC")
        self.horizontalLayout.addWidget(self.label_NMC)
        self.maxNMC = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.maxNMC.setMaximumSize(QtCore.QSize(80, 50))
        self.maxNMC.setObjectName("maxNMC")
        self.horizontalLayout.addWidget(self.maxNMC)

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
        self.sortNMC = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.sortNMC.setMaximumSize(QtCore.QSize(100, 50))
        self.sortNMC.setObjectName("sortNMC")
        self.horizontalLayout.addWidget(self.sortNMC)
        self.sortPrice = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.sortPrice.setMaximumSize(QtCore.QSize(100, 50))
        self.sortPrice.setObjectName("sortPrice")
        self.horizontalLayout.addWidget(self.sortPrice)
        self.sortChange = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.sortChange.setMaximumSize(QtCore.QSize(100, 50))
        self.sortChange.setObjectName("sortChange")
        self.horizontalLayout.addWidget(self.sortChange)
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

        self.sortChange.setChecked(True)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PlatformBreakthrough"))
        self.labelPrice.setText(_translate("MainWindow", "价格区间："))
        self.label_.setText(_translate("MainWindow", "-"))
        self.labelNMC.setText(_translate("MainWindow", "流通市值："))
        self.label_NMC.setText(_translate("MainWindow", "-"))
        self.labelChange.setText(_translate("MainWindow", "涨幅："))
        self.label_Change.setText(_translate("MainWindow", "-"))
        self.sortNMC.setText(_translate("MainWindow", "市值↓"))
        self.sortPrice.setText(_translate("MainWindow", "价格↓"))
        self.sortChange.setText(_translate("MainWindow", "涨幅↓"))
        self.DownButton.setText(_translate("MainWindow", "下载"))
        self.RefreshButton.setText(_translate("MainWindow", "刷新现价"))
        self.SearchButton.setText(_translate("MainWindow", "Search"))
