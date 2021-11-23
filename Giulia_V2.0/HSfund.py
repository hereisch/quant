# -*- coding: utf-8 -*-#
# -*- coding: utf-8 -*-#
import time
from datetime import datetime, date, timedelta
import pymongo
import pandas as pd
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
import os
from UI.UI_HSfund import Ui_HSfund
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from CONSTANT import MONGOHOST
from BK_fund import fundHS
from selectStock import async_

pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


client = pymongo.MongoClient(host="192.168.0.28", port=27017)
db = client['quant']


class HSfundWindow(QMainWindow,Ui_HSfund):

    def __init__(self,parent=None):
        super(HSfundWindow,self).__init__(parent)
        self.setupUi(self)
        self.data = fundHS()
        self.res = db.get_collection('NMC').find()
        self.nmc = {i['code']: round(i['nmc']/10000,2) for i in self.res} 
        self.data['nmc'] = self.data['f12'].apply(lambda x:self.nmc[x])
        self.header = ['f12','f14','f3','f2','nmc','f62','f184','f66','f69','f72','f75','f78','f81','f84','f87','date',]
        self.headerCN = ["code","name","涨跌幅","最新价","市值","主力净额（万）","主力净占比","超大单净额（万）","超大单净占比","大单净额（万）","大单净占比","中单净额（万）","中单净占比","小单净额（万）","小单净占比","时间"]
        self.data = self.data[self.header]
        self.SearchButton.clicked.connect(lambda: self.showStock(autoRresh=99,))
        self.maxPrice.returnPressed.connect(lambda: self.showStock(autoRresh=99,))
        self.minPrice.returnPressed.connect(lambda: self.showStock(autoRresh=99,))
        self.maxNMC.returnPressed.connect(lambda: self.showStock(autoRresh=99, ))
        self.minNMC.returnPressed.connect(lambda: self.showStock(autoRresh=99, ))
        self.maxChange.returnPressed.connect(lambda: self.showStock(autoRresh=99,))
        self.minChange.returnPressed.connect(lambda: self.showStock(autoRresh=99,))
        self.RefreshButton.clicked.connect(lambda: self.showStock(autoRresh=True))

        self.showStock()



    def cleanScreen(self):
        self.model = QStandardItemModel(2, 2)
        self.model.setHorizontalHeaderLabels(self.headerCN)
        self.stockTable.setModel(self.model)
        for idx, itemY in enumerate(self.header):
            item = QStandardItem()
            self.model.setItem(0, idx, item)
        layout = QVBoxLayout()
        layout.addWidget(self.stockTable)
        self.setLayout(layout)

    @async_
    def showStock(self,autoRresh=False):
        if autoRresh is True:
            self.data = fundHS()
            self.data['nmc'] = self.data['f12'].apply(lambda x: self.nmc[x])
        elif autoRresh == 99:
            if self.data is None:
                self.data = fundHS()
                self.data['nmc'] = self.data['f12'].apply(lambda x: self.nmc[x])

        # 设置数据层次结构，2行2列
        self.model = QStandardItemModel(2, 2)
        # 设置水平方向四个头标签文本内容
        self.model.setHorizontalHeaderLabels(self.headerCN)

        highPrice = self.maxPrice.text()
        lowPrice = self.minPrice.text()
        highNMC = self.maxNMC.text()
        lowNMC = self.minNMC.text()
        highChange = self.maxChange.text()
        lowChange = self.minChange.text()
        if highPrice.isdigit():
            self.data = self.data[self.data['f2'] <= float(highPrice)]
        if lowPrice.isdigit():
            self.data = self.data[self.data['f2'] >= float(lowPrice)]
        if highNMC.isdigit():
            self.data = self.data[self.data['nmc'] <= float(highNMC)]
        if lowNMC.isdigit():
            self.data = self.data[self.data['nmc'] >= float(lowNMC)]
        try:
            highChange = eval(highChange)
            self.data = self.data[self.data['f3'] <= float(highChange)]
        except:
            pass
        try:
            lowChange = eval(lowChange)
            self.data = self.data[self.data['f3'] >= float(lowChange)]
        except:
            pass
        
        
        if self.sortZLJE.isChecked():
            self.data = self.data.sort_values(by=['f62',],ascending=(False))
        if self.sortZLJZB.isChecked():
            self.data = self.data.sort_values(by=['f184',],ascending=(False))
        if self.sortCDJE.isChecked():
            self.data = self.data.sort_values(by=['f66',],ascending=(False))
        if self.sortCDJZB.isChecked():
            self.data = self.data.sort_values(by=['f69',],ascending=(False))
            
        self.data = self.data.reset_index(drop=True)


        try:
            for idy, itemX in self.data.iterrows():
                for idx, itemY in enumerate(self.header):
                    item = QStandardItem(str(itemX[itemY]))
                    if self.headerCN.index('主力净额（万）') <= idx < self.headerCN.index('时间'):
                        if itemX[itemY] > 0:
                            item.setForeground(QColor(255,0,0))
                        else:
                            item.setForeground(QColor(0, 150, 0))
                    self.model.setItem(idy, idx, item)



        except Exception as e:
            print(e)

        self.stockTable.setModel(self.model)
        # 不可编辑
        self.stockTable.setItemDelegate(EmptyDelegate(self))

        # 设置tableview所有列的默认行高为10
        # self.stockTable.verticalHeader().setDefaultSectionSize(20)
        # 设置tableview所有行的默认列宽为15
        # self.stockTable.horizontalHeader().setDefaultSectionSize(80)
        self.stockTable.resizeRowsToContents()
        self.stockTable.resizeColumnsToContents()

        layout = QVBoxLayout()
        layout.addWidget(self.stockTable)
        self.setLayout(layout)


class EmptyDelegate(QItemDelegate):
    def __init__(self, parent):
        super(EmptyDelegate, self).__init__(parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return None


if __name__ == '__main__':
    """
        For My Dream Car  -----  Alfa Romeo Giulia
        """
    app = QApplication(sys.argv)
    win = HSfundWindow()
    win.show()
    # win.showMaximized()
    app.exec_()