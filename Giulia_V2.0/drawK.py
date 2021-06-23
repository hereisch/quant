# -*- coding: utf-8 -*-#
import os
import sys
import time

import pandas as pd
import pymongo
import pyqtgraph as pg
from PyQt5.QtCore import QRect, QUrl
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pyqtgraph import QtCore, QtGui
import plotly.offline as po
import plotly.graph_objs as go
import plotly.offline as pyof
import numpy as np
import matplotlib.pyplot as plt
from plotly import subplots
import tushare as ts
import plotly
from datetime import datetime, date, timedelta
from CONSTANT import MONGOHOST



class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data  ## data must have fields: time, open, close, min, max
        self.generatePicture()

    def generatePicture(self):
        ## pre-computing a QPicture object allows paint() to run much more quickly,
        ## rather than re-drawing the shapes every time.
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        w = (self.data[1][0] - self.data[0][0]) / 3.
        for (t, open, close, min, max) in self.data:
            p.drawLine(QtCore.QPointF(t, min), QtCore.QPointF(t, max))
            if open > close:
                # 开盘价高于收盘价，绿
                p.setBrush(pg.mkBrush('g'))
            else:
                p.setBrush(pg.mkBrush('r'))
            p.drawRect(QtCore.QRectF(t - w, open, w * 2, close - open))
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        ## boundingRect _must_ indicate the entire area that will be drawn on
        ## or else we will get artifacts and possibly crashing.
        ## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QtCore.QRectF(self.picture.boundingRect())

    """
    data = [  ## fields are (time, open, close, min, max).
        (1., 10, 13, 5, 15),
        (2., 13, 17, 9, 20),
        (3., 17, 14, 11, 23),
        (4., 14, 15, 5, 19),
        (5., 15, 9, 8, 22),
        (6., 9, 15, 8, 16),
    ]
    """


def intervalStat(code,name):

    """区间成交量统计,18:00以后、开盘前调get_tick_data 接口"""

    now_time = datetime.now()
    open_time =datetime.strptime(str(datetime.now().date())+'9:30', '%Y-%m-%d%H:%M')
    # close_time = datetime.strptime(str(datetime.now().date()) + '15:00', '%Y-%m-%d%H:%M')
    if time.localtime().tm_hour >=18 :
        # 当日数据复盘
        today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        df = ts.get_tick_data(code, date=today, src='tt')
        df.rename(columns={'volume': 'vol'}, inplace=True)
        df.replace('买盘','买入',inplace=True)
        df.replace('卖盘','卖出',inplace=True)
        df.replace('中性盘','-',inplace=True)
    elif now_time <= open_time:
        # 上一个交易日数据
        pro = ts.pro_api()
        yesterday = (date.today() + timedelta(-1)).strftime('%Y%m%d')
        lastTrade = pro.trade_cal(end_date=yesterday)
        lastTrade = lastTrade[lastTrade['is_open']==1]
        lastTrade = lastTrade.iloc[-1]['cal_date']
        print(lastTrade,'上一交易日',code)
        df = ts.get_tick_data(code, date=lastTrade, src='tt')
        df.rename(columns={'volume': 'vol'}, inplace=True)
        df.replace('买盘', '买入', inplace=True)
        df.replace('卖盘', '卖出', inplace=True)
        df.replace('中性盘', '-', inplace=True)
    else:
        # 开盘
        df = ts.get_today_ticks(code)
        df['amount'] = df['price']* df['vol']*100

    buy = df[df['type'] == '买入']
    sale = df[df['type'] == '卖出']
    mid = df[df['type'] == '-']

    s = sale.groupby(['price'])['vol'].sum()
    b = buy.groupby(['price'])['vol'].sum()
    # t = df.groupby(['price'])['vol'].sum()

    print('买入总成交：',buy['vol'].sum(),'手')
    print('卖出总成交：',sale['vol'].sum(),'手')
    print('总买入：',buy['amount'].sum())
    print('总卖出：',sale['amount'].sum())
    print('净买入额：',(buy['amount'].sum()-sale['amount'].sum())/10000,'万')

    # fig = subplots.make_subplots(rows=3, cols=1)
    traceS = go.Bar(x = list(s.to_dict().values()),y = list(s.to_dict().keys()),name='卖出',marker=dict(color='green'),orientation = 'h')
    traceB = go.Bar(x = list(b.to_dict().values()),y = list(b.to_dict().keys()),name='买入',marker=dict(color='red'),orientation = 'h')
    # traceT
    # = go.Bar(x = list(t.to_dict().keys()),y = list(t.to_dict().values()),name='总数',marker=dict(color='blue'))
    layout = go.Layout(barmode='stack')
    figT = go.Figure(data=[traceB,traceS],layout=layout)
    plotly.offline.plot(figT, filename= 'Total.html', auto_open=False)
    figB = go.Figure(data=traceB)
    plotly.offline.plot(figB, filename='Buy.html', auto_open=False)
    figS = go.Figure(data=traceS)
    plotly.offline.plot(figS, filename= 'Sale.html', auto_open=False)


    traceTick = go.Scatter(x=df.index, y=df['price'], marker=dict(color='gray'))
    layout = go.Layout(title_text=code+':'+name,margin=go.layout.Margin(l=1, r=1, b=10),
                       yaxis=dict(title_text="<b>Price</b>"),
                       yaxis2=dict(title_text="<b>Volume</b>", anchor="x", overlaying="y", side="right"))
    df['color'] = ''

    df.color[df.type == '买入'] = 'red'
    df.color[df.type == '卖出'] = 'green'
    df.color[df.type == '-'] = 'gray'
    vol = go.Bar(x=df.index, y=df['vol'], marker_color=df['color'], yaxis='y2')
    data = [traceTick, vol]
    figTick = go.Figure(data, layout)
    plotly.offline.plot(figTick, filename= 'TickTime.html', auto_open=False)







## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':

    client = pymongo.MongoClient(host=MONGOHOST, port=27017)
    db = client['quant']
    res = db.get_collection('dayK').find({'code':'603990'})

    df = pd.DataFrame(list(res))
    dayK = go.Candlestick(x=df['date'],
                           open=df['open'],
                           high=df['high'],
                           low=df['low'],
                           close=df['close'],
                           increasing_line_color='red',
                           decreasing_line_color='green')
    volume = go.Bar(x=df['date'],y=df['volume']/10000)
    _data = [dayK,volume]
    layout = {'title': '603990'}
    fig = subplots.make_subplots(rows=1, cols=1,subplot_titles='draw')
    fig.append_trace(dayK,1,1)
    fig.append_trace(volume,1,1)
    fig.update_layout(xaxis={'tickmode':'auto', 'nticks':10,'tickformat':'%Y-%m-%d'})
    fig.show()
    # fig = dict(data=_data, layout=layout)
    # po.plot(fig,)

    # data = [(idx,i['open'],i['close'],i['low'],i['high']) for idx,i in enumerate(res)]
    # print(data,res)
    # item = CandlestickItem(data)
    # plt = pg.plot()
    # plt.addItem(item)
    # plt.setWindowTitle('pyqtgraph example: customGraphicsItem')
    # if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    #     QtGui.QApplication.instance().exec_()
