# -*- coding: utf-8 -*-#
import pymongo
import pandas as pd
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
import os
from UI.UI_Impact import Ui_impactWindow
import tushare as ts
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import plotly
import numpy as np
import plotly.graph_objects as go
from drawK import intervalStat
from selectStock import downStock,refresh
from CONSTANT import MONGOHOST



pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


class RiseNWindow(QMainWindow,Ui_impactWindow):

    def __init__(self,parent=None):
        super(RiseNWindow,self).__init__(parent)
        self.client = pymongo.MongoClient(host=MONGOHOST, port=27017)
        self.db = self.client['quant']
        self.setupUi(self)
        self.comboBox.addItems(['N连阳','强势股'])
        self.comboBox.currentIndexChanged[str].connect(self.showStock)
        self.stockList = None
        self.header = ['code','name','riseNum','trade','date']
        self.headerCN = ['代码', '名称','10日连阳数','现价','日期']
        self.tabK.currentChanged.connect(self.tabShow)
        self.topList = self.db.get_collection('topList').distinct('code')
        self.showStock()
        self.code = None
        self.name = None
        self.comboBox.currentIndexChanged[str].connect(self.showStock)


    def tabShow(self,x):
        indexK = ['Day','min_30','min_15','min_5','min_60','tick_time']
        typeK = ['D','30','15','5','60',]
        extent = [250,150,150,150,150]
        tabEngine = [self.webEngineView_6,self.webEngineView_5,self.webEngineView_4,self.webEngineView,self.webEngineView_3,self.webEngineView_9]
        print('当前标签是:', indexK[x])
        if x != 5:
            data = ts.get_hist_data(self.code,ktype=typeK[x])
            pageK = self.can_vol(dataframe=data,tabpage=indexK[x],name=self.code+':'+self.name,end=extent[x])
            tabEngine[x].load(QUrl.fromLocalFile(os.path.join(os.getcwd(),pageK)))
            # todo 异步存入

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


    def showStock(self,):
        impactDict = {'N连阳':'riseN','强势股':'strong'}
        # 设置数据层次结构，2行2列
        self.model = QStandardItemModel(2, 2)
        # 设置水平方向四个头标签文本内容
        self.model.setHorizontalHeaderLabels(self.headerCN)
        impactText = self.comboBox.currentText()
        res = self.initDB(coll=impactDict[impactText])
        self.stockList = pd.DataFrame(list(res))
        try:
            self.stockList = self.stockList.sort_values(by=['riseNum' ], ascending=(False))
            self.stockList = self.stockList.reset_index(drop=True)
            # self.stockList['contBoard'].fillna('',inplace=True)
            for idy, itemX in self.stockList.iterrows():
                for idx, itemY in enumerate(self.header):
                    item = QStandardItem(str(itemX[itemY]))
                    if idx == 0 and itemX[itemY] in self.topList:
                        item.setBackground(QColor(220,102,0))
                    if itemX[itemY] is True :
                        # print(itemX, '55555555555')
                        item.setBackground(QColor(204,102,255))
                    # 设置每个位置的文本值
                    self.model.setItem(idy, idx, item)

        except Exception as e:
            print(e,'清屏...')
            self.cleanScreen()
            return

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
        # x_axis = [i[2:] for i in data1.index]
        x_axis = [i[2:].replace('-','') for i in data1.date]
        # 生成新列，以便后面设置颜色
        data1['diag'] = np.empty(len(data1))
        # 设置涨/跌成交量柱状图的颜色
        data1.diag[data1.close > data1.open] = '#ff0000'
        data1.diag[data1.close <= data1.open] = '#00ff00'
        layout = go.Layout(title_text=name, title_font_size=30, autosize=True, margin=go.layout.Margin(l=10, r=1, b=10),
                           xaxis=dict( type='category'),
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
        MA5 = go.Scatter(x=x_axis,y=data1.ma5,mode='lines', line = dict(color = '#ff9900'),name='ma5')
        # 这里一定要设置yaxis=2, 确保成交量的y轴在右边，不和价格的y轴在一起
        data = [vol,candle,MA5]
        fig = go.Figure(data, layout)
        plotly.offline.plot(fig, filename=tabpage+'.html', auto_open=False)
        return tabpage+'.html'

    def initDB(self,coll='impact2to3'):

        result = self.db.get_collection(coll).find()
        return result

    def mouseDoubleClickEvent(self, event):
        # print('双击事件：',event.row(), event.column())
        # print(self.stockList.loc[event.row()]['code'],self.stockList.loc[event.row()]['name'])
        self.code,self.name = self.stockList.loc[event.row()]['code'],self.stockList.loc[event.row()]['name']
        # data = ts.get_hist_data(self.code)
        data = self.db.get_collection('dayK').find({'code':self.code}).sort('date',1)
        data = pd.DataFrame(list(data))
        kPath = self.can_vol(dataframe=data,name=self.code+':'+self.name,start=-250,end=None)
        self.webEngineView_6.load(QUrl.fromLocalFile(os.path.join(os.getcwd(),kPath)))

        # 盘口展示
        try:
            intervalStat(self.code,self.name)
            self.webEngineView_2.load(QUrl.fromLocalFile(os.path.join(os.getcwd(),'Total.html')))
            self.webEngineView_7.load(QUrl.fromLocalFile(os.path.join(os.getcwd(),'Buy.html')))
            self.webEngineView_8.load(QUrl.fromLocalFile(os.path.join(os.getcwd(),'Sale.html')))
            self.webEngineView_9.load(QUrl.fromLocalFile(os.path.join(os.getcwd(),'TickTime.html')))
        except Exception as e:
            print('区间统计错误：',self.code,e)


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
    win = RiseNWindow()
    win.show()
    # win.showMaximized()
    app.exec_()