# -*- coding: utf-8 -*-#
import pymongo
import pandas as pd
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from Ui_Giulia import Ui_MainWindow
from test import can_vol
import tushare as ts
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from TopStock import StockTable



class MainWindow(QMainWindow,Ui_MainWindow):

    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.client = pymongo.MongoClient(host="192.168.0.28", port=27017)
        self.db = self.client['quant']
        self.stockList = None
        self.header = ['code', 'name', 'industry', 'changepercent', 'trade', 'top3', 'top5', 'top13', 'top21', 'top34', 'top55', 'top89', 'top144', 'top233']
        self.setupUi(self)
        self.showStock()


    def showStock(self,sortPrice=False,pChange=True,lowPrice=5,highPrice=100):
        # 设置数据层次结构，4行4列
        self.model = QStandardItemModel(4, 4)
        # 设置水平方向四个头标签文本内容
        self.model.setHorizontalHeaderLabels(self.header)
        res = self.initDB()
        self.stockList = pd.DataFrame(list(res))
        if pChange:
            self.stockList = self.stockList.sort_values(by=['changepercent'],ascending=(False))
        if sortPrice:
            self.stockList.sort_values(by=['trade'], ascending=(False))

        self.stockList = self.stockList.reset_index(drop=True)

        for idy, itemX in self.stockList.iterrows():
            _trade = itemX['trade']
            for idx, itemY in enumerate(self.header):
                item = QStandardItem(str(itemX[itemY]))
                if idx > 4 and type(itemX[itemY]) == str:
                    item.setBackground(QColor(255, 153, 153))
                # 设置每个位置的文本值
                self.model.setItem(idy, idx, item)


        self.stockTable.setModel(self.model)
        # 不可编辑
        self.stockTable.setItemDelegate(EmptyDelegate(self))
        # 双击取值
        self.stockTable.doubleClicked.connect(self.mouseDoubleClickEvent)
        # 设置tableview所有列的默认行高为10
        self.stockTable.verticalHeader().setDefaultSectionSize(20)
        # 设置tableview所有行的默认列宽为15
        self.stockTable.horizontalHeader().setDefaultSectionSize(100)

        layout = QVBoxLayout()
        layout.addWidget(self.stockTable)
        self.setLayout(layout)



    def initDB(self):

        result = self.db.get_collection('today').find()
        return result

    def mouseDoubleClickEvent(self, event):
        print('双击事件：',event.row(), event.column())
        print(self.stockList.loc[event.row()]['code'],self.stockList.loc[event.row()]['name'])

        data = ts.get_hist_data(self.stockList.loc[event.row()]['code'])
        kPath = can_vol(dataframe=data)
        self.webEngineView_6.load(QUrl.fromLocalFile('/Users/hereisch/Desktop/GitHub/quant/'+kPath))


class EmptyDelegate(QItemDelegate):
    def __init__(self, parent):
        super(EmptyDelegate, self).__init__(parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return None




if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    # win.showMaximized()
    app.exec_()