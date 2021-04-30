# -*- coding: utf-8 -*-#
import pymongo
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
        self.setupUi(self)
        self.showStock()

    def showStock(self,sortPricd=False,pChange=True):
        self.header = ['code', 'name', 'industry', 'changepercent', 'trade', 'top3', 'top5', 'top13', 'top21', 'top34', 'top55', 'top89', 'top144', 'top233']
        # 设置数据层次结构，4行4列
        self.model = QStandardItemModel(4, 4)
        # 设置水平方向四个头标签文本内容
        self.model.setHorizontalHeaderLabels(self.header)
        res = self.initDB()
        for idy, itemX in enumerate(res):
            _trade = itemX['trade']
            for idx, itemY in enumerate(self.header):
                item = QStandardItem(str(itemX[itemY]))
                if idx > 4 and type(itemX[itemY]) == str:
                    item.setBackground(QColor(255, 153, 153))
                # 设置每个位置的文本值
                self.model.setItem(idy, idx, item)

        self.stockTable.setModel(self.model)
        self.stockTable.sortByColumn(3, Qt.DescendingOrder)
        # 不可编辑
        self.stockTable.setItemDelegate(EmptyDelegate(self))
        # 双击取值
        self.stockTable.doubleClicked.connect(self.mouseDoubleClickEvent)
        # 设置tableview所有列的默认行高为10
        self.stockTable.verticalHeader().setDefaultSectionSize(10)
        # 设置tableview所有行的默认列宽为15
        self.stockTable.horizontalHeader().setDefaultSectionSize(100)

        layout = QVBoxLayout()
        layout.addWidget(self.stockTable)
        self.setLayout(layout)



    def initDB(self):
        client = pymongo.MongoClient(host="192.168.0.28", port=27017)
        db = client['quant']
        result = db.get_collection('today').find()
        return result

    def mouseDoubleClickEvent(self, event):
        print('双击事件：',event.row(), event.column())
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