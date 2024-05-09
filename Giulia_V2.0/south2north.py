# -*- coding: utf-8 -*-#
import os,math
import sys
import pandas as pd
import numpy as np
import requests
import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from datetime import datetime
from CONSTANT import EastmoneyURL
pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


win = pg.GraphicsLayoutWidget(show=True)

win.resize(1000,400)
p1 = win.addPlot()

headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
}

def fund(_url='South2North',):
    """

    :param code: 代码
    :param _url: url类型,默认当日历史资金流
    :return:
    """
    win.setWindowTitle('北向资金')

    url = EastmoneyURL[_url]
    resp = requests.get(url,headers=headers)
    data = resp.json()['data']['s2n']
    df = pd.DataFrame(data,columns=['dd'])

    if  df.empty:
        print('无数据/未开盘...')
        sys.exit(0)


    new = df['dd'].str.split(',', expand=True)
    new.columns = ['time','HGT_nbuy','HGT_buy','SGT_nbuy','HGT_sell','BX_nbuy','SGT_buy','SGT_sell','BX_buy','BX_sell']
    # new['time'] = new['time'].str.extract("(\d\d:\d\d)")
    new = new[~new['HGT_nbuy'].str.contains('-')]
    new['HGT_buy'] = new['HGT_buy'].astype(float)/10000
    new['HGT_nbuy'] = new['HGT_nbuy'].astype(float)/10000
    new['SGT_buy'] = new['SGT_buy'].astype(float)/10000
    new['SGT_nbuy'] = new['SGT_nbuy'].astype(float)/10000
    new['HGT_sell'] = new['HGT_sell'].astype(float)/10000
    new['SGT_sell'] = new['SGT_sell'].astype(float)/10000
    new['BX_nbuy'] = new['BX_nbuy'].astype(float)/10000
    new['BX_buy'] = new['BX_buy'].astype(float)/10000
    new['BX_sell'] = new['BX_sell'].astype(float)/10000



    os.system("cls")
    print(new.tail(10))
    print('北向:{}亿,\n沪股通:{}亿,\n深股通:{}亿,'.format(
                                                        round(new.tail(1)['BX_nbuy'].values[0],2),
                                                        round(new.tail(1)['HGT_nbuy'].values[0],2),
                                                        round(new.tail(1)['SGT_nbuy'].values[0],2)))
    return new



def update():

    # now_time = datetime.now()
    data = fund()
    stringaxis = pg.AxisItem(orientation='bottom')
    xdict = dict(enumerate(data.index))
    axis_1 = [(i, list(data.index)[i]) for i in range(0, len(data.index), 10)]
    stringaxis.setTicks([axis_1,xdict.items()])
    BX_nbuy = data['BX_nbuy'].values.tolist()
    HGT_nbuy = data['HGT_nbuy'].values.tolist()
    SGT_nbuy = data['SGT_nbuy'].values.tolist()
    curve_BX  = p1.plot(BX_nbuy,pen=(102,255,255),name='北向')
    curve_HGT = p1.plot(HGT_nbuy,pen=(255,0,0),name='沪股通')
    curve_SGT = p1.plot(SGT_nbuy,pen=(255,200,0),name='深股通')


    curve_BX.setData(BX_nbuy[:-1])
    curve_HGT.setData(HGT_nbuy[:-1])
    curve_SGT.setData(SGT_nbuy[:-1])





timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(5000)


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

def data_period(data,col,k):
    """

    :param data: 原数据（df）
          time   HGT_nbuy     HGT_buy   SGT_nbuy    HGT_sell    BX_nbuy     SGT_buy    SGT_sell      BX_buy     BX_sell
    231  14:51  46.655437  329.438072  45.104432  282.782635  91.759869  338.637332  293.532900  668.075404  576.315535
    232  14:52  46.117504  330.606095  44.733136  284.488591  90.850640  339.558049  294.824913  670.164144  579.313504
    233  14:53  45.737195  331.894786  44.618519  286.157591  90.355714  340.557508  295.938989  672.452294  582.096580
    234  14:54  45.350805  333.041983  44.704565  287.691179  90.055370  341.728814  297.024249  674.770797  584.715428
    235  14:55  44.980429  334.467980  44.504763  289.487551  89.485192  342.965687  298.460923  677.433667  587.948474
    236  14:56  44.078655  335.782429  43.869791  291.703774  87.948446  344.121870  300.252080  679.904299  591.955854
    237  14:57  43.092222  337.352654  42.682837  294.260433  85.775059  345.296261  302.613424  682.648915  596.873857
    238  14:58  43.085465  337.386648  42.606654  294.301183  85.692119  345.399142  302.792488  682.785790  597.093671
    239  14:59  43.085904  337.390894  42.606654  294.304989  85.692558  345.399142  302.792488  682.790036  597.097477
    240  15:00  39.247325  342.056590  40.895077  302.809265  80.142402  351.256089  310.361012  693.312679  613.170277
    :param col: 列名
    :param k: 周期
    :return:     data = [  ## fields are (time, open, close, min, max).
                        (1., 10, 13, 5, 15),
                        (2., 13, 17, 9, 20),
                        (3., 17, 14, 11, 23),
                        (4., 14, 15, 5, 19),
                        (5., 15, 9, 8, 22),
                        (6., 9, 15, 8, 16),
    ]
    """
    lst = data[col].values.tolist()
    lst = [lst[i:i + 3] for i in range(0, len(lst), k)]
    result = []
    for idx,i in enumerate(lst):
        T = data.iloc[idx*3]['time']
        open = i[0]
        close = i[-1]
        low = min(i)
        high = max(i)
        result.append((idx,open,close,low,high))
        # print((T,open,close,low,high),i)


    return result



if __name__ == '__main__':

    """北向资金"""


    # QtGui.QGuiApplication.instance().exec_()

    # data = [  ## fields are (time, open, close, min, max).
    #     (1., 10, 13, 5, 15),
    #     (2., 13, 17, 9, 20),
    #     (3., 17, 14, 11, 23),
    #     (4., 14, 15, 5, 19),
    #     (5., 15, 9, 8, 22),
    #     (6., 9, 15, 8, 16),
    # ]
    data = fund()
    result = data_period(data,'BX_nbuy',3)

    item = CandlestickItem(result)
    plt = pg.plot()
    plt.addItem(item)
    plt.setWindowTitle('北向资金')
    pg.exec()

    # open_time = datetime.strptime(str(datetime.now().date()) + '9:30', '%Y-%m-%d%H:%M')
    # close_time = datetime.strptime(str(datetime.now().date()) + '15:00', '%Y-%m-%d%H:%M')
    # forenoon = datetime.strptime(str(datetime.now().date()) + '11:30', '%Y-%m-%d%H:%M')
    # afternoon = datetime.strptime(str(datetime.now().date()) + '13:30', '%Y-%m-%d%H:%M')
    # now_time = datetime.now()
    #
    # if open_time < now_time < forenoon or afternoon < now_time < close_time:
    #     QtGui.QApplication.instance().exec_()
    #
    # else:
    #     print('休市....') 