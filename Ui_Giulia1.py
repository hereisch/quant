# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_Giulia.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from TopStock import StockTable

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1800, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 功能列表
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(10, 10, 180, 800))
        self.listView.setObjectName("listView")

        # 新高股列表
        self.tableView = StockTable(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(200, 70, 1500, 230))
        self.tableView.setObjectName("tableView")

        # 详情标签页
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(210, 320, 1200, 480))
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.webEngineView_6 = QtWebEngineWidgets.QWebEngineView(self.tab)
        self.webEngineView_6.setGeometry(QtCore.QRect(0, 0, 930, 240))
        self.webEngineView_6.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView_6.setObjectName("webEngineView_6")

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.webEngineView_5 = QtWebEngineWidgets.QWebEngineView(self.tab_2)
        self.webEngineView_5.setGeometry(QtCore.QRect(0, 0, 930, 240))
        self.webEngineView_5.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView_5.setObjectName("webEngineView_5")

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.webEngineView_4 = QtWebEngineWidgets.QWebEngineView(self.tab_3)
        self.webEngineView_4.setGeometry(QtCore.QRect(0, 0, 930, 240))
        self.webEngineView_4.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView_4.setObjectName("webEngineView_4")

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.tab_4)
        self.webEngineView.setGeometry(QtCore.QRect(0, 0, 930, 240))
        self.webEngineView.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView.setObjectName("webEngineView")

        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.webEngineView_3 = QtWebEngineWidgets.QWebEngineView(self.tab_5)
        self.webEngineView_3.setGeometry(QtCore.QRect(0, 0, 930, 240))
        self.webEngineView_3.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView_3.setObjectName("webEngineView_3")

        # 筹码窗口
        self.tabWidget.addTab(self.tab_5, "")
        self.webEngineView_2 = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.webEngineView_2.setGeometry(QtCore.QRect(1420, 320, 300, 480))
        self.webEngineView_2.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView_2.setObjectName("webEngineView_2")

        # 搜索按钮
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1500, 30, 120, 40))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1364, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Day"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "30min"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "15min"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "5min"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "1min"))
        self.pushButton.setText(_translate("MainWindow", "Search"))
from PyQt5 import QtWebEngineWidgets