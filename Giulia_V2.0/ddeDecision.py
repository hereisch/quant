# -*- coding: utf-8 -*-#
import random
import json
import os
import re
from threading import Thread
import pymongo
import requests
import time
import tushare as ts
import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime, date, timedelta
from UI.UI_DDE import Ui_DDE
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
from selectStock import async_





pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


client = pymongo.MongoClient(host=MONGOHOST, port=27017)
db = client['quant']

User_Agent = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.23 Safari/537.36",
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
]


headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': '__51cke__=; Hm_lvt_34e0d77f0c897023357dcfa7daa006f3=1626846961; d_ddx=1626846965; Hm_lpvt_34e0d77f0c897023357dcfa7daa006f3=1626846985; __tins__1523105=%7B%22sid%22%3A%201626849104630%2C%20%22vd%22%3A%202%2C%20%22expires%22%3A%201626851989983%7D; __51laig__=11',
    'Host': 'ddx.gubit.cn',
    'Referer': 'http://ddx.gubit.cn/xg/ddx.html',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': random.choice(User_Agent),
}



def ddxData():
    base = db.get_collection('base').find()
    industry = {i['code']: i['name'] for i in base}

    ddx_config = ['代码', '最新价', '涨幅', '换手率', '量比', 'DDX1日', 'DDY1日', 'DDZ', 'DDX3日', 'DDX5日', 'DDX10日', 'DDX60日', 'DDX5红', 'DDX10红', 'DDX连红', 'DDX连增', '涨幅3日', '涨幅5日', '涨幅10日', 'DDY3日', 'DDY5日',
                  'DDY10日',
                  'DDY60日', '成交量(万)', 'BBD(万)', '通吃率1日', '通吃率5日', '通吃率10日', '通吃率20日', '单数比', '特大差', '大单差', '中单差', '小单差', '主动率1日', '主动率5日', '主动率10日', '流通盘(万股)', '未知']

    abcddx_config = ['code', 'spj', 'zf', 'huanshou', 'liangbi', 'ddx', 'ddy', 'ddz', 'ddx3', 'ddx5', 'ddx10', 'ddx60', '5ddx', '10ddx', 'ddxlh', 'ddxlz', 'zf3', 'zf5', 'zf10', 'ddy3', 'ddy5',
                     'ddy10',
                     'ddy60', 'cjl', 'bbd', 'tcl1', 'tcl5', 'tcl10', 'tcl20', 'dsb', 'tdc', 'ddc', 'zdc', 'xdc', 'zdl1', 'zdl5', 'zdl10', 'wtp', 'unknow']
    data = []
    for i in tqdm(range(1,26)):
        url_sz = 'http://ddx.gubit.cn/xg/ddxlist.php?orderby=8&gtype=sz0&isdesc=1&page={}&t={}'.format(i, random.random())
        url_sh = 'http://ddx.gubit.cn/xg/ddxlist.php?orderby=8&gtype=sh&isdesc=1&page={}&t={}'.format(i, random.random())
        respSZ = requests.get(url_sz, headers=headers)
        respSH = requests.get(url_sh, headers=headers)
        try:
            data += respSH.json()['data']
            data += respSZ.json()['data']
        except Exception as e:
            print(e)
            print('SH...',respSH.text)
            print('SZ...',respSZ.text)

        time.sleep(0.2)

    df = pd.DataFrame(data, columns=ddx_config)
    df['代码'] = df['代码'].apply(lambda x: str('{:0>6d}'.format(x)))
    filt = df['代码'].str.contains('^(?!688|605|300|301)')
    df = df[filt]
    df = df.drop_duplicates()
    df['名称'] = df['代码'].apply(lambda x: industry[x] if x in industry else '新股')
    df = df.sort_values(by=['DDX1日'], ascending=(False))
    print('实时刷新：',respSH.json()['updatetime'])
    return df


class DDEWindow(QMainWindow,Ui_DDE):

    def __init__(self,parent=None):
        super(DDEWindow,self).__init__(parent)
        self.client = pymongo.MongoClient(host=MONGOHOST, port=27017)
        self.db = self.client['quant']
        self.stockList = None
        self.header = ['code', 'name','spj', 'zf', 'huanshou', 'liangbi', 'ddx', 'ddy', 'ddz', 'ddx3', 'ddx5', 'ddx10', 'ddx60', '5ddx', '10ddx', 'ddxlh', 'ddxlz', 'zf3', 'zf5', 'zf10', 'ddy3', 'ddy5','ddy10','ddy60', 'cjl', 'bbd', 'tcl1', 'tcl5', 'tcl10', 'tcl20', 'dsb', 'tdc', 'ddc', 'zdc', 'xdc', 'zdl1', 'zdl5', 'zdl10', 'wtp', 'unknow']
        # self.headerCN = ['代码', '名称','最新价', '涨幅', '换手率', '量比', 'DDX1日', 'DDY1日', 'DDZ', 'DDX3日', 'DDX5日', 'DDX10日', 'DDX60日', 'DDX5红', 'DDX10红', 'DDX连红', 'DDX连增', '涨幅3日', '涨幅5日', '涨幅10日', 'DDY3日', 'DDY5日','DDY10日','DDY60日', '成交量(万)', 'BBD(万)', '通吃率1日', '通吃率5日', '通吃率10日', '通吃率20日', '单数比', '特大差', '大单差', '中单差', '小单差', '主动率1日', '主动率5日', '主动率10日', '流通盘(万股)', '未知']
        self.headerCN = ['代码', '名称','最新价', '涨幅', 'BBD(万)', 'DDX1日', 'DDY1日', 'DDZ', 'DDX3日', 'DDX5日', 'DDX10日', 'DDY3日', 'DDY5日','DDY10日', '通吃率1日', '通吃率5日', '通吃率10日','单数比', '特大差', '大单差', '中单差', '小单差', '主动率1日', '主动率5日', '主动率10日',  'DDX5红', 'DDX10红', 'DDX连红', 'DDX连增', '涨幅3日', '涨幅5日', '涨幅10日', '换手率', '量比','成交量(万)', '流通盘(万股)', '未知']
        self.setupUi(self)
        self.tabK.currentChanged.connect(self.tabShow)
        self.topList = self.db.get_collection('topList').distinct('code')
        self.showStock(autoRresh=99)
        self.code = None
        self.name = None
        self.autoRefresh = False
        self.SearchButton.clicked.connect(lambda: self.showStock(autoRresh=99,))
        self.Stop.clicked.connect(lambda: self.showStock(autoRresh=False,))
        self.RefreshButton.clicked.connect(lambda: self.showStock(autoRresh=True))
        self.minPrice.returnPressed.connect(lambda: self.showStock(autoRresh=99,))
        self.maxPrice.returnPressed.connect(lambda: self.showStock(autoRresh=99,))
        # self.maxNMC.returnPressed.connect(lambda: self.showStock(autoRresh=99,filter=True))
        # self.minNMC.returnPressed.connect(lambda: self.showStock(autoRresh=99,filter=True))
        self.minChange.returnPressed.connect(lambda: self.showStock(autoRresh=99))
        self.maxChange.returnPressed.connect(lambda: self.showStock(autoRresh=99,))


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

    @async_
    def showStock(self,autoRresh=True):
        if autoRresh is True:
            self.stockList = ddxData()
        elif autoRresh is False:
            self.cleanScreen()
            return 0
        elif autoRresh == 99:
            if self.stockList is None:
                self.stockList = ddxData()

        highPrice = self.maxPrice.text()
        lowPrice = self.minPrice.text()
        # highNMC = self.maxNMC.text()
        # lowNMC = self.minNMC.text()
        highChange = self.maxChange.text()
        lowChange = self.minChange.text()
        if highPrice.isdigit():
            self.stockList = self.stockList[self.stockList['最新价'] <= float(highPrice)]
        if lowPrice.isdigit():
            self.stockList = self.stockList[self.stockList['最新价'] >= float(lowPrice)]
        if highChange.isdigit():
            self.stockList = self.stockList[self.stockList['涨幅'] <= float(highChange)]
        if lowChange.isdigit():
            self.stockList = self.stockList[self.stockList['涨幅'] >= float(lowChange)]


        # 设置数据层次结构，2行2列
        self.model = QStandardItemModel(2, 2)
        # 设置水平方向四个头标签文本内容
        self.model.setHorizontalHeaderLabels(self.headerCN)

        if self.sortDDX1.isChecked():
            self.stockList = self.stockList.sort_values(by=['DDX1日','DDX3日','DDX5日','DDX10日'],ascending=(False,False,False,False))
        elif self.sortDDX3.isChecked():
            self.stockList = self.stockList.sort_values(by=['DDX3日','DDX1日','DDX5日','DDX10日'],ascending=(False,False,False,False))
        elif self.sortDDX5.isChecked():
            self.stockList = self.stockList.sort_values(by=['DDX5日','DDX1日','DDX3日','DDX10日'],ascending=(False,False,False,False))
        elif self.sortDDX10.isChecked():
            self.stockList = self.stockList.sort_values(by=['DDX10日','DDX1日','DDX3日','DDX5日'],ascending=(False,False,False,False))
        elif self.dsb.isChecked():
            self.stockList = self.stockList.sort_values(by=['单数比','特大差','大单差',],ascending=(False,False,False))
        elif self.BBD.isChecked():
            self.stockList = self.stockList.sort_values(by=['BBD(万)','DDX1日','DDX3日','DDX5日'],ascending=(False,False,False,False))
        elif self.sortChange.isChecked():
            self.stockList = self.stockList.sort_values(by=['涨幅','DDX1日','DDX3日','DDX5日'],ascending=(False,False,False,False))
        elif self.sortCapitcal.isChecked():
            self.stockList = self.stockList.sort_values(by=['特大差','大单差','通吃率1日','主动率1日'],ascending=(False,False,False,False))

        self.stockList = self.stockList.reset_index(drop=True)

        try:
            for idy, itemX in self.stockList.iterrows():
                for idx, itemY in enumerate(self.headerCN):
                    item = QStandardItem(str(itemX[itemY]))
                    if idx ==0 and itemX[itemY] in self.topList:
                        item.setBackground(QColor(220,102,0))
                    # 'trade' index in self.header
                    if self.headerCN.index('BBD(万)') <= idx <= self.headerCN.index('主动率10日') :
                        if itemX[itemY] > 0:
                            item.setForeground(QColor(255,0,0))
                        else:
                            item.setForeground(QColor(0, 150, 0))

                    if self.headerCN.index('涨幅3日') <= idx <= self.headerCN.index('涨幅10日') :
                        if itemX[itemY] > 0:
                            item.setForeground(QColor(255,0,0))
                        else:
                            item.setForeground(QColor(0, 150, 0))
                    #
                    # if self.headerCN.index('BBD(万)') <= idx <= self.headerCN.index('通吃率20日') :
                    #     if itemX[itemY] > 0:
                    #         item.setForeground(QColor(255,0,0))
                    #     else:
                    #         item.setForeground(QColor(0, 150, 0))


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
    win = DDEWindow()
    win.show()
    # win.showMaximized()
    app.exec_()