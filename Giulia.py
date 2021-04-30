# -*- coding: utf-8 -*-#
import pymongo
import pandas as pd
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from Ui_Giulia import Ui_MainWindow

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


    def showStock(self,sortPricd=False,pChange=True,lowPrice=5,highPrice=100):
        # 设置数据层次结构，4行4列
        self.model = QStandardItemModel(4, 4)
        # 设置水平方向四个头标签文本内容
        self.model.setHorizontalHeaderLabels(self.header)
        res = self.initDB()
        self.stockList = pd.DataFrame(list(res))
        if pChange:
            self.stockList = self.stockList.sort_values(by=['changepercent'],ascending=(False))
        if sortPricd:
            self.stockList.sort_values(by=['trade'], ascending=(False))
        self.stockList = self.stockList.reset_index(drop=True)
        # print('kkkkkkk',self.stockList)
        for idy, itemX in self.stockList.iterrows():
            _trade = itemX['trade']
            # print('33333333333',idy,itemX)
            # kk = {}
            for idx, itemY in enumerate(self.header):

                item = QStandardItem(str(itemX[itemY]))
                if idx > 4 and type(itemX[itemY]) == str:
                    item.setBackground(QColor(255, 153, 153))
                # 设置每个位置的文本值
                self.model.setItem(idy, idx, item)
                print(idy,idx,itemX[itemY])
                # kk[itemY] = itemX[itemY]
            # print(idy, kk)

        self.stockTable.setModel(self.model)
        self.stockTable.sortByColumn(3, Qt.DescendingOrder)
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
        # print(self.stockList)
        print(self.stockList.loc[event.row()])
        return event.row(), event.column()


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