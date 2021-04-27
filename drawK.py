# -*- coding: utf-8 -*-#
import os
import sys
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
                p.setBrush(pg.mkBrush('r'))
            else:
                p.setBrush(pg.mkBrush('g'))
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





## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':

    client = pymongo.MongoClient(host="192.168.0.28", port=27017)
    db = client['quant']
    res = db.get_collection('dayK').find({'code':'603990'})
    data = [(idx,i['open'],i['close'],i['low'],i['high']) for idx,i in enumerate(res)]
    df = pd.DataFrame(list(res))
    trace = go.Candlestick(x=df['date'],
                           open=df['open'],
                           high=df['high'],
                           low=df['low'],
                           close=df['close'])
    data = [trace]
    layout = {'title': '603990'}
    fig = dict(data=data, layout=layout)
    po.plot(fig,)

    item = CandlestickItem(data)
    plt = pg.plot()
    plt.addItem(item)
    plt.setWindowTitle('pyqtgraph example: customGraphicsItem')
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
