# -*- coding: utf-8 -*-#
import sys

import pymongo
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from CONSTANT import MONGOHOST

class StockTable(QWidget):
    def __init__(self, parent=None):
        super(StockTable, self).__init__(parent)
        # 设置标题与初始大小
        self.setWindowTitle('新高')
        self.resize(1500, 800)
        self.header = ['code', 'name', 'industry','changepercent', 'trade','top3','top5','top13','top21','top34','top55','top89','top144','top233']
        # 设置数据层次结构，4行4列
        self.model = QStandardItemModel(4, 4)
        # 设置水平方向四个头标签文本内容
        self.model.setHorizontalHeaderLabels(self.header)
        res = self.initDB()
        for idy,itemX in enumerate(res):
            _trade = itemX['trade']
            for idx,itemY in enumerate(self.header):
                item = QStandardItem(str(itemX[itemY]))
                if idx > 4 and type(itemX[itemY])==str:
                    item.setBackground(QColor(255,153,153))
                # 设置每个位置的文本值
                self.model.setItem(idy, idx, item)


        # 实例化表格视图，设置模型为自定义的模型
        self.tableView = QTableView()
        self.tableView.setModel(self.model)

        # #todo 优化1 表格填满窗口
        # #水平方向标签拓展剩下的窗口部分，填满表格
        # self.tableView.horizontalHeader().setStretchLastSection(True)
        # #水平方向，表格大小拓展到适当的尺寸
        # self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 按涨幅排序
        self.tableView.sortByColumn(3,Qt.DescendingOrder)
        # 不可编辑
        self.tableView.setItemDelegate(EmptyDelegate(self))
        # 双击取值
        self.tableView.doubleClicked.connect(self.mouseDoubleClickEvent)
        # 设置tableview所有列的默认行高为10
        self.tableView.verticalHeader().setDefaultSectionSize(10)
        # 设置tableview所有行的默认列宽为15
        self.tableView.horizontalHeader().setDefaultSectionSize(100)


        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.tableView)
        self.setLayout(layout)

    def initDB(self):
        client = pymongo.MongoClient(host=MONGOHOST, port=27017)
        db = client['quant']
        result = db.get_collection('today').find()
        return result

    def mouseDoubleClickEvent(self, event):

        return event.row(), event.column()


class EmptyDelegate(QItemDelegate):
    def __init__(self, parent):
        super(EmptyDelegate, self).__init__(parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return None


if __name__ == '__main__':

    app = QApplication(sys.argv)
    table = StockTable()
    table.show()
    sys.exit(app.exec_())