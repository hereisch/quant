# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\UI_Giulia.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(2200, 1200)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 1452, 1068))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.splitter = QtWidgets.QSplitter(self.scrollAreaWidgetContents_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.groupBox = QtWidgets.QGroupBox(self.splitter)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.selectStockBtn = QtWidgets.QPushButton(self.groupBox)
        self.selectStockBtn.setObjectName("selectStockBtn")
        self.verticalLayout.addWidget(self.selectStockBtn)
        self.impactBoardBtn = QtWidgets.QPushButton(self.groupBox)
        self.impactBoardBtn.setObjectName("impactBoardBtn")
        self.verticalLayout.addWidget(self.impactBoardBtn)
        self.stockPoolBtn = QtWidgets.QPushButton(self.groupBox)
        self.stockPoolBtn.setObjectName("stockPoolBtn")
        self.verticalLayout.addWidget(self.stockPoolBtn)
        self.absorbBtn = QtWidgets.QPushButton(self.groupBox)
        self.absorbBtn.setObjectName("absorbBtn")
        self.verticalLayout.addWidget(self.absorbBtn)
        self.NRiseUpBtn = QtWidgets.QPushButton(self.groupBox)
        self.NRiseUpBtn.setObjectName("NRiseUpBtn")
        self.verticalLayout.addWidget(self.NRiseUpBtn)
        self.DDEBtn = QtWidgets.QPushButton(self.groupBox)
        self.DDEBtn.setObjectName("DDEBtn")
        self.verticalLayout.addWidget(self.DDEBtn)
        spacerItem = QtWidgets.QSpacerItem(20, 864, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.frame = QtWidgets.QFrame(self.splitter)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2.addWidget(self.splitter)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout.addWidget(self.scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1476, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.splitter.setStretchFactor(0,1)
        self.splitter.setStretchFactor(1,9)
        MainWindow.move(200, 1200)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "韭菜助手_V2.0"))
        self.groupBox.setTitle(_translate("MainWindow", "功能列表"))
        self.selectStockBtn.setText(_translate("MainWindow", "选股"))
        self.impactBoardBtn.setText(_translate("MainWindow", "打板"))
        self.stockPoolBtn.setText(_translate("MainWindow", "自选"))
        self.absorbBtn.setText(_translate("MainWindow", "阳包阴"))
        self.NRiseUpBtn.setText(_translate("MainWindow", "N连阳"))
        self.DDEBtn.setText(_translate("MainWindow", "DDE决策"))
