# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\UI_Selector.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DDE(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(2000, 1200)
        # MainWindow.setWindowOpacity(0.5)
        # MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
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
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
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
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.sortDDX1 = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.sortDDX1.setMaximumSize(QtCore.QSize(100, 50))
        self.sortDDX1.setObjectName("sortDDX1")
        self.horizontalLayout.addWidget(self.sortDDX1)
        self.sortDDX3 = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.sortDDX3.setMaximumSize(QtCore.QSize(100, 50))
        self.sortDDX3.setObjectName("sortDDX3")
        self.horizontalLayout.addWidget(self.sortDDX3)
        self.sortDDX5 = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.sortDDX5.setMaximumSize(QtCore.QSize(100, 50))
        self.sortDDX5.setObjectName("sortDDX5")
        self.horizontalLayout.addWidget(self.sortDDX5)
        self.sortDDX10 = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.sortDDX10.setMaximumSize(QtCore.QSize(100, 50))
        self.sortDDX10.setObjectName("sortDDX10")
        self.horizontalLayout.addWidget(self.sortDDX10)
        self.dsb = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.dsb.setMaximumSize(QtCore.QSize(100, 50))
        self.dsb.setObjectName("dsb")
        self.horizontalLayout.addWidget(self.dsb)
        self.BBD = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.BBD.setMaximumSize(QtCore.QSize(100, 50))
        self.BBD.setObjectName("BBD")
        self.horizontalLayout.addWidget(self.BBD)
        self.sortChange = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.sortChange.setMaximumSize(QtCore.QSize(100, 50))
        self.sortChange.setObjectName("sortChange")
        self.horizontalLayout.addWidget(self.sortChange)
        self.sortCapitcal = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.sortCapitcal.setMaximumSize(QtCore.QSize(100, 50))
        self.sortCapitcal.setObjectName("sortCapitcal")
        self.horizontalLayout.addWidget(self.sortCapitcal)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.Stop = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.Stop.setMaximumSize(QtCore.QSize(200, 100))
        self.Stop.setObjectName("Stop")
        self.horizontalLayout.addWidget(self.Stop)
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
        self.stockTable.setMinimumSize(QtCore.QSize(0, 100))
        self.stockTable.setObjectName("stockTable")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.tabK = QtWidgets.QTabWidget(self.splitter)
        self.tabK.setObjectName("tabK")
        self.Day = QtWidgets.QWidget()
        self.Day.setObjectName("Day")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.Day)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.webEngineView_6 = QtWebEngineWidgets.QWebEngineView(self.Day)
        self.webEngineView_6.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView_6.setObjectName("webEngineView_6")
        self.horizontalLayout_3.addWidget(self.webEngineView_6)
        self.tabK.addTab(self.Day, "")
        self.min_30 = QtWidgets.QWidget()
        self.min_30.setObjectName("min_30")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.min_30)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.webEngineView_5 = QtWebEngineWidgets.QWebEngineView(self.min_30)
        self.webEngineView_5.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView_5.setObjectName("webEngineView_5")
        self.horizontalLayout_4.addWidget(self.webEngineView_5)
        self.tabK.addTab(self.min_30, "")
        self.min_15 = QtWidgets.QWidget()
        self.min_15.setObjectName("min_15")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.min_15)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.webEngineView_4 = QtWebEngineWidgets.QWebEngineView(self.min_15)
        self.webEngineView_4.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView_4.setObjectName("webEngineView_4")
        self.horizontalLayout_5.addWidget(self.webEngineView_4)
        self.tabK.addTab(self.min_15, "")
        self.min_5 = QtWidgets.QWidget()
        self.min_5.setObjectName("min_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.min_5)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.min_5)
        self.webEngineView.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView.setObjectName("webEngineView")
        self.horizontalLayout_6.addWidget(self.webEngineView)
        self.tabK.addTab(self.min_5, "")
        self.min_1 = QtWidgets.QWidget()
        self.min_1.setObjectName("min_1")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.min_1)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.webEngineView_3 = QtWebEngineWidgets.QWebEngineView(self.min_1)
        self.webEngineView_3.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView_3.setObjectName("webEngineView_3")
        self.horizontalLayout_7.addWidget(self.webEngineView_3)
        self.tabK.addTab(self.min_1, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.webEngineView_9 = QtWebEngineWidgets.QWebEngineView(self.tab)
        self.webEngineView_9.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView_9.setObjectName("webEngineView_9")
        self.horizontalLayout_11.addWidget(self.webEngineView_9)
        self.tabK.addTab(self.tab, "")
        self.tabStatic = QtWidgets.QTabWidget(self.splitter)
        self.tabStatic.setObjectName("tabStatic")
        self.Total = QtWidgets.QWidget()
        self.Total.setObjectName("Total")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.Total)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.webEngineView_2 = QtWebEngineWidgets.QWebEngineView(self.Total)
        self.webEngineView_2.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView_2.setObjectName("webEngineView_2")
        self.horizontalLayout_8.addWidget(self.webEngineView_2)
        self.tabStatic.addTab(self.Total, "")
        self.Buy = QtWidgets.QWidget()
        self.Buy.setObjectName("Buy")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.Buy)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.webEngineView_7 = QtWebEngineWidgets.QWebEngineView(self.Buy)
        self.webEngineView_7.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView_7.setObjectName("webEngineView_7")
        self.horizontalLayout_9.addWidget(self.webEngineView_7)
        self.tabStatic.addTab(self.Buy, "")
        self.Sale = QtWidgets.QWidget()
        self.Sale.setObjectName("Sale")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.Sale)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.webEngineView_8 = QtWebEngineWidgets.QWebEngineView(self.Sale)
        self.webEngineView_8.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView_8.setObjectName("webEngineView_8")
        self.horizontalLayout_10.addWidget(self.webEngineView_8)
        self.tabStatic.addTab(self.Sale, "")
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
        self.tabK.setCurrentIndex(0)
        self.tabStatic.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        self.sortDDX1.setChecked(True)
        self.splitter_2.setStretchFactor(0, 7)
        self.splitter_2.setStretchFactor(1, 2)
        self.splitter.setStretchFactor(0, 7)
        self.splitter.setStretchFactor(1, 2)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.labelPrice.setText(_translate("MainWindow", "价格区间："))
        self.label_.setText(_translate("MainWindow", "-"))
        self.labelNMC.setText(_translate("MainWindow", "待定："))
        self.label_NMC.setText(_translate("MainWindow", "-"))
        self.labelChange.setText(_translate("MainWindow", "涨幅："))
        self.label_Change.setText(_translate("MainWindow", "-"))
        self.sortDDX1.setText(_translate("MainWindow", "DDX1↓"))
        self.sortDDX3.setText(_translate("MainWindow", "DDX3↓"))
        self.sortDDX5.setText(_translate("MainWindow", "DDX5↓"))
        self.sortDDX10.setText(_translate("MainWindow", "DDX10↓"))
        self.dsb.setText(_translate("MainWindow", "单数比↓"))
        self.BBD.setText(_translate("MainWindow", "资金流↓"))
        self.sortChange.setText(_translate("MainWindow", "涨幅↓"))
        self.sortCapitcal.setText(_translate("MainWindow", "游资↓"))
        self.Stop.setText(_translate("MainWindow", "停止刷新"))
        self.RefreshButton.setText(_translate("MainWindow", "刷新"))
        self.SearchButton.setText(_translate("MainWindow", "Search"))
        self.tabK.setTabText(self.tabK.indexOf(self.Day), _translate("MainWindow", "Day"))
        self.tabK.setTabText(self.tabK.indexOf(self.min_30), _translate("MainWindow", "30min"))
        self.tabK.setTabText(self.tabK.indexOf(self.min_15), _translate("MainWindow", "15min"))
        self.tabK.setTabText(self.tabK.indexOf(self.min_5), _translate("MainWindow", "5min"))
        self.tabK.setTabText(self.tabK.indexOf(self.min_1), _translate("MainWindow", "1min"))
        self.tabK.setTabText(self.tabK.indexOf(self.tab), _translate("MainWindow", "分时"))
        self.tabStatic.setTabText(self.tabStatic.indexOf(self.Total), _translate("MainWindow", "Total"))
        self.tabStatic.setTabText(self.tabStatic.indexOf(self.Buy), _translate("MainWindow", "Buy"))
        self.tabStatic.setTabText(self.tabStatic.indexOf(self.Sale), _translate("MainWindow", "Sale"))
from PyQt5 import QtWebEngineWidgets
