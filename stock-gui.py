# -*- coding: utf-8 -*-#
import sys

import pymongo
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Table(QWidget):
    def __init__(self, parent=None):
        super(Table, self).__init__(parent)
        # 设置标题与初始大小
        self.setWindowTitle('主视窗')
        self.resize(2000, 800)
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
        #水平方向标签拓展剩下的窗口部分，填满表格
        self.tableView.horizontalHeader().setStretchLastSection(True)
        #水平方向，表格大小拓展到适当的尺寸
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 按涨幅排序
        self.tableView.sortByColumn(3,Qt.DescendingOrder)

        # #TODO 优化3 删除当前选中的数据
        # indexs=self.tableView.selectionModel().selection().indexes()
        # print(indexs)
        # if len(indexs)>0:
        #   index=indexs[0]
        #   self.model.removeRows(index.row(),1)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.tableView)
        self.setLayout(layout)



    def initDB(self):
        client = pymongo.MongoClient(host="192.168.0.28", port=27017)
        db = client['quant']
        result = db.get_collection('today').find()
        return result



if __name__ == '__main__':
    app = QApplication(sys.argv)
    table = Table()
    table.show()
    sys.exit(app.exec_())