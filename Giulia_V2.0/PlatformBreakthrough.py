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
from UI.UI_PlatformBreakthrough import Ui_PlatformBreakthrough
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from CONSTANT import MONGOHOST
from BK_fund import breakThrough
from selectStock import async_

pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


client = pymongo.MongoClient(host=MONGOHOST, port=27017)
db = client['quant']


class PlatformBreakthroughWindow(QMainWindow,Ui_PlatformBreakthrough):
    """共用HSfund UI"""
    def __init__(self,parent=None):
        super(PlatformBreakthroughWindow,self).__init__(parent)
        self.setupUi(self)
        self.data = breakThrough()
        self.res = db.get_collection('NMC').find()
        self.nmc = {i['code']: round(i['nmc']/10000,2) for i in self.res} 
        self.data['nmc'] = self.data['code'].apply(lambda x:self.nmc[x])
        self.header = ['code', 'name', 'nmc', 'new', 'zdf']
        self.headerCN = ["code","name","市值","最新价","涨跌幅"]
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
            self.data = breakThrough()
            self.data['nmc'] = self.data['code'].apply(lambda x: self.nmc[x])
        elif autoRresh == 99:
            if self.data is None:
                self.data = breakThrough()
                self.data['nmc'] = self.data['code'].apply(lambda x: self.nmc[x])

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
            self.data = self.data[self.data['new'] <= float(highPrice)]
        if lowPrice.isdigit():
            self.data = self.data[self.data['new'] >= float(lowPrice)]
        if highNMC.isdigit():
            self.data = self.data[self.data['nmc'] <= float(highNMC)]
        if lowNMC.isdigit():
            self.data = self.data[self.data['nmc'] >= float(lowNMC)]
        try:
            highChange = eval(highChange)
            self.data = self.data[self.data['zdf'] <= float(highChange)]
        except:
            pass
        try:
            lowChange = eval(lowChange)
            self.data = self.data[self.data['zdf'] >= float(lowChange)]
        except:
            pass
        
        
        if self.sortNMC.isChecked():
            self.data = self.data.sort_values(by=['nmc',],ascending=(False))
        if self.sortChange.isChecked():
            self.data = self.data.sort_values(by=['zdf',],ascending=(False))
        if self.sortPrice.isChecked():
            self.data = self.data.sort_values(by=['new',],ascending=(False))

            
        self.data = self.data.reset_index(drop=True)


        try:
            for idy, itemX in self.data.iterrows():
                for idx, itemY in enumerate(self.header):
                    item = QStandardItem(str(itemX[itemY]))
                    if self.headerCN.index('涨跌幅') == idx:
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
    win = PlatformBreakthroughWindow()
    win.show()
    # win.showMaximized()
    app.exec_()