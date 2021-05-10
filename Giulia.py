# -*- coding: utf-8 -*-#
import pymongo
import pandas as pd
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
import os
from Ui_Giulia import Ui_MainWindow
import tushare as ts
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from TopStock import StockTable
import plotly
import numpy as np
import plotly.graph_objects as go

class MainWindow(QMainWindow,Ui_MainWindow):

    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.client = pymongo.MongoClient(host="192.168.0.28", port=27017)
        self.db = self.client['quant']
        self.stockList = None
        self.header = ['code', 'name', 'industry', 'nmc','changepercent', 'trade', 'top3', 'top5', 'top13', 'top21', 'top34', 'top55', 'top89', 'top144', 'top233']
        self.setupUi(self)
        self.tabK.currentChanged.connect(self.tabShow)
        self.topList = ts.top_list()['code'].tolist()
        self.showStock()
        self.code = None
        self.name = None


    def tabShow(self,x):
        indexK = ['Day','min_30','min_15','min_5','min_1']
        tabEngine = [self.webEngineView_6,]
        print('当前标签是:', indexK[x])
        # html = self.can_vol(dataframe=,tabpage=indexK[x])


    def showStock(self,sortPrice=False,pChange=True,lowPrice=4,highPrice=100):
        # 设置数据层次结构，4行4列
        self.model = QStandardItemModel(4, 4)
        # 设置水平方向四个头标签文本内容
        self.model.setHorizontalHeaderLabels(self.header)
        res = self.initDB()
        self.stockList = pd.DataFrame(list(res))
        self.stockList['nmc'] = self.stockList['nmc'] /10000
        # self.stockList['nmc'].round(2)
        if pChange:
            self.stockList = self.stockList.sort_values(by=['changepercent'],ascending=(False))
        if sortPrice:
            self.stockList.sort_values(by=['trade'], ascending=(False))

        self.stockList = self.stockList.reset_index(drop=True)

        for idy, itemX in self.stockList.iterrows():
            _trade = itemX['trade']
            for idx, itemY in enumerate(self.header):
                item = QStandardItem(str(itemX[itemY]))
                if idx ==0 and itemX[itemY] in self.topList:
                    item.setBackground(QColor(220,102,0))
                if idx > 5 and type(itemX[itemY]) == str:
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

    def can_vol(self,dataframe=None, start=0, end=250, name='Candlestick',tabpage=''):

        data1 = dataframe.iloc[start:end, :]  # 区间，这里我只是测试，并没有真正用时间来选
        data1 = data1.sort_index(axis=0, ascending=True)
        x_axis = [i[2:] for i in data1.index]
        # 生成新列，以便后面设置颜色
        data1['diag'] = np.empty(len(data1))
        # 设置涨/跌成交量柱状图的颜色
        data1.diag[data1.close > data1.open] = '#e21de2'
        data1.diag[data1.close <= data1.open] = '#1de2e2'
        layout = go.Layout(title_text=name, title_font_size=30, autosize=True, margin=go.layout.Margin(l=10, r=1, b=10),
                           xaxis=dict(title_text="Candlesticck", type='category'),
                           yaxis=dict(title_text="<b>Price</b>"),
                           yaxis2=dict(title_text="<b>Volume</b>", anchor="x", overlaying="y", side="right"))
        # layout的参数超级多，因为它用一个字典可以集成所有图的所有格式
        # 这个函数里layout值得注意的是 type='category'，设置x轴的格式不是candlestick自带的datetime形式，
        # 因为如果用自带datetime格式总会显示出周末空格，这个我找了好久才解决周末空格问题。。。
        candle = go.Candlestick(x=x_axis,
                                open=data1.open, high=data1.high,
                                low=data1.low, close=data1.close, increasing_line_color='#e21d1d',
                                decreasing_line_color='#008000', name="Price")
        vol = go.Bar(x=x_axis,
                     y=data1.volume, name="Volume", marker_color=data1.diag, opacity=0.5, yaxis='y2')
        # 这里一定要设置yaxis=2, 确保成交量的y轴在右边，不和价格的y轴在一起
        data = [vol,candle]
        fig = go.Figure(data, layout)
        plotly.offline.plot(fig, filename=tabpage+'.html', auto_open=False)
        return tabpage+'.html'

    def initDB(self):

        result = self.db.get_collection('today').find()
        return result

    def mouseDoubleClickEvent(self, event):
        # print('双击事件：',event.row(), event.column())
        # print(self.stockList.loc[event.row()]['code'],self.stockList.loc[event.row()]['name'])
        self.code,self.name = self.stockList.loc[event.row()]['code'],self.stockList.loc[event.row()]['name']
        data = ts.get_hist_data(self.code)
        kPath = self.can_vol(dataframe=data,name=self.code+':'+self.name)
        self.webEngineView_6.load(QUrl.fromLocalFile(os.path.join(os.getcwd(),kPath)))


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