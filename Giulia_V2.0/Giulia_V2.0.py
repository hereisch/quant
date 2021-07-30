# -*- coding: utf-8 -*-#
import pymongo
import pandas as pd
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
import os
from UI.UI_Giulia import Ui_MainWindow
from UI.UI_Selector import Ui_Selector
import tushare as ts
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import plotly
import numpy as np
import plotly.graph_objects as go
from selectStock import downStock,refresh
from Selector import SelectorWindow
from Impact import ImpactWindow
from RiseN import RiseNWindow
from ddeDecision import DDEWindow


pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)





class MainWindow(QMainWindow,Ui_MainWindow):

    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.setupUi(self)
        self.qsl = QStackedLayout(self.frame)
        self.selectorWindow = SelectorWindow()
        self.qsl.addWidget(self.selectorWindow)
        self.impact = ImpactWindow()
        self.qsl.addWidget(self.impact)
        self.pool = QMainWindow()
        self.qsl.addWidget(self.pool)
        self.notification = QMainWindow()
        self.qsl.addWidget(self.notification)
        self.riseN = RiseNWindow()
        self.qsl.addWidget(self.riseN)
        self.dde = DDEWindow()
        self.qsl.addWidget(self.dde)


        self.selectStockBtn.clicked.connect(self.switch)
        self.impactBoardBtn.clicked.connect(self.switch)
        self.stockPoolBtn.clicked.connect(self.switch)
        self.supervisorBtn.clicked.connect(self.switch)
        self.NRiseUpBtn.clicked.connect(self.switch)
        self.DDEBtn.clicked.connect(self.switch)


    def switch(self):
        sender = self.sender().objectName()
        index = {
            "selectStockBtn":0,
            "impactBoardBtn":1,
            "stockPoolBtn":2,
            "supervisorBtn":3,
            "NRiseUpBtn":4,
            "DDEBtn":5,
        }
        self.qsl.setCurrentIndex(index[sender])





if __name__ == '__main__':
    """
    For My Dream Car  -----  Alfa Romeo Giulia
    """
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    # win.showMaximized()
    app.exec_()