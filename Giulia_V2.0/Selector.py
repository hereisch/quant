# -*- coding: utf-8 -*-#
import time
from datetime import datetime, date, timedelta
import pymongo
import pandas as pd
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
import os
from UI.UI_Selector import Ui_Selector
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



class SelectorWindow(QMainWindow,Ui_Selector):

    def __init__(self,parent=None):
        super(SelectorWindow,self).__init__(parent)
        self.client = pymongo.MongoClient(host=MONGOHOST, port=27017)
        self.db = self.client['quant']
        self.stockList = None
        self.header = ['code', 'name', 'industry', 'nmc','turnoverratio','volRatio','changepercent', 'trade','coverage', 'top3', 'top5', 'top13', 'top21', 'top34', 'top55', 'top89', 'top144', 'top233','ma5','ma10','ma20']
        self.headerCN = ['代码', '名称', '行业', '流通市值','换手率','成交量比','涨幅', '现价','阳包阴', '3日', '5日', '13日', '21日', '34日', '55日', '89日', '144日', '233日','5日线','10日线','20日线']
        self.setupUi(self)
        self.tabK.currentChanged.connect(self.tabShow)
        self.topList = self.db.get_collection('topList').distinct('code')
        self.showStock()
        self.code = None
        self.name = None
        self.comboBox.addItems(['所有行业'] + self.db.get_collection('today').distinct('industry'))
        self.SearchButton.clicked.connect(self.showStock)
        self.AddStockButton.clicked.connect(self.AddStockPool)
        self.DownButton.clicked.connect(lambda: self.showStock(download=True))
        self.RefreshButton.clicked.connect(lambda: self.showStock(fresh=True))
        self.minPrice.returnPressed.connect(self.showStock)
        self.maxPrice.returnPressed.connect(self.showStock)
        self.maxNMC.returnPressed.connect(self.showStock)
        self.minNMC.returnPressed.connect(self.showStock)
        self.minChange.returnPressed.connect(self.showStock)
        self.maxChange.returnPressed.connect(self.showStock)
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


    def showStock(self,fresh=False,download=False):
        if fresh is True:
            refresh()
        if download is True:
            downStock()
        self.topList = self.db.get_collection('topList').distinct('code')
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
        industryText = self.comboBox.currentText()
        res = self.initDB(lowPrice=lowPrice,highPrice=highPrice,highNMC=highNMC,lowNMC=lowNMC,highChange=highChange,lowChange=lowChange)
        self.stockList = pd.DataFrame(list(res))
        if industryText != '' and industryText != '所有行业':
            self.stockList = self.stockList[self.stockList['industry']==industryText]

        self.stockList['nmc'] = self.stockList['nmc'] / 10000
        self.stockList['nmc'] = self.stockList['nmc'].round(2)
        self.stockList['turnoverratio'] = self.stockList['turnoverratio'].round(3)

        if self.changePercent.isChecked():
            self.stockList = self.stockList.sort_values(by=['changepercent',],ascending=(False,))
        elif self.sortPrice.isChecked():
            self.stockList = self.stockList.sort_values(by=['trade'], ascending=(True))
        elif self.sortVol.isChecked():
            self.stockList = self.stockList.sort_values(by=['volRatio','count','changepercent'],ascending=(False,False,False))
        elif self.sortCount.isChecked():
            self.stockList = self.stockList.sort_values(by=['count','changepercent','volRatio'],ascending=(False,False,False))
        elif self.profit.isChecked():
            self.stockList = self.stockList.sort_values(by=['profit', 'count', 'changepercent'], ascending=(False, False, False))
        elif self.coverage.isChecked():
            self.stockList = self.stockList.sort_values(by=['coverage','changepercent'], ascending=(False, False))



        self.stockList = self.stockList.reset_index(drop=True)

        try:
            for idy, itemX in self.stockList.iterrows():
                _trade = itemX['trade']
                for idx, itemY in enumerate(self.header):
                    item = QStandardItem(str(itemX[itemY]))
                    if idx ==0 and itemX[itemY] in self.topList:
                        item.setBackground(QColor(220,102,0))
                    # 'trade' index in self.header
                    if idx == self.header.index('trade') and itemX['open'] <= itemX['ma5'] <= _trade and itemX['open'] <= itemX['ma10'] <= _trade and itemX['open'] <= itemX['ma20'] <= _trade:
                        # item.setForeground(QColor(255,0,0))
                        item.setBackground(QColor(204, 102, 255))
                    if self.header.index('ma5') > idx > self.header.index('trade') and type(itemX[itemY]) == str:
                        item.setBackground(QColor(255, 153, 153))
                    if idx == self.header.index('ma5') and _trade <= itemX['ma5']:
                        # 跌破5日线
                        item.setBackground(QColor(0, 255, 0))
                    if idx == self.header.index('changepercent') and itemX['open'] == itemX['high'] and itemX['changepercent'] > 9:
                        # 涨停高开一字板
                        item.setBackground(QColor(255, 10, 10))

                    # if idx >= self.header.index('ma5') and type(itemX[itemY]) == str:
                    #     item.setBackground(QColor(204,102,255))
                    # 设置每个位置的文本值
                    self.model.setItem(idy, idx, item)

        except Exception as e:
            self.cleanScreen()
            print(e)

        self.stockTable.setModel(self.model)
        # 不可编辑
        self.stockTable.setItemDelegate(EmptyDelegate(self))
        # 双击取值
        self.stockTable.doubleClicked.connect(self.mouseDoubleClickEvent)
        # 设置tableview所有列的默认行高为10
        self.stockTable.verticalHeader().setDefaultSectionSize(20)
        # 设置tableview所有行的默认列宽为15
        self.stockTable.horizontalHeader().setDefaultSectionSize(80)

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
        MA10 = go.Scatter(x=x_axis,y=data1.ma10,mode='lines', line = dict(color = '#0066ff'),name='ma10')
        MA20 = go.Scatter(x=x_axis,y=data1.ma20,mode='lines', line = dict(color = '#ff00ff'),name='ma20')
        # 这里一定要设置yaxis=2, 确保成交量的y轴在右边，不和价格的y轴在一起
        data = [vol,candle,MA5,MA10,MA20]
        fig = go.Figure(data, layout)
        plotly.offline.plot(fig, filename=tabpage+'.html', auto_open=False)
        return tabpage+'.html'

    def initDB(self,lowPrice='',highPrice='',highNMC='',lowNMC='',highChange='',lowChange=''):

        query = []

        if lowPrice.isdigit():
            query.append({"trade" : { "$gte" : int(lowPrice) }})
        if highPrice.isdigit():
            query.append({"trade": {"$lte": int(highPrice)}})
        if highNMC.isdigit():
            query.append({"nmc": {"$lte": int(highNMC)*10000}})
        if lowNMC.isdigit():
            query.append({"nmc": {"$gte": int(lowNMC)*10000}})
        if lowChange.isdigit():
            query.append({"changepercent" : { "$gte" : int(lowChange) }})
        if highChange.isdigit():
            query.append({"changepercent" : { "$lte" : int(highChange) }})

        if query:
            result = self.db.get_collection('today').find({ "$and" : query})
        else:
            result = self.db.get_collection('today').find()
        return result


    def AddStockPool(self):
        """
        添加自选，保存10日自选
        :return:
        """
        today = time.strftime("%Y-%m-%d", time.localtime())
        day10 = (date.today() + timedelta(-10)).strftime('%Y%m%d')
        self.db.get_collection('newTop').remove({'date':{'$lte':day10}})
        res = self.db.get_collection('today').find({"$or": [{"changepercent": {"$gte": 8}}, {"count": {"$gte": 7}}]})
        r = self.db.get_collection('newTop').find_one({'date':today})
        if not r:
            for i in res:
                i.pop('_id')
                i['date'] = today
                self.db.get_collection('newTop').insert(i)


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
    win = SelectorWindow()
    win.show()
    # win.showMaximized()
    app.exec_()