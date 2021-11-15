# -*- coding: utf-8 -*-#
import os
import sys
import pandas as pd
import requests
import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from datetime import datetime

pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('Fund')
win.resize(1200,300)
p1 = win.addPlot()

headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
}

def fund(code):

    code = '1.' + code if code.startswith('6') else '0.' + code
    url = 'http://push2.eastmoney.com/api/qt/stock/fflow/kline/get?lmt=0&klt=1&fields1=f1%2Cf2%2Cf3%2Cf7&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61%2Cf62%2Cf63%2Cf64%2Cf65&ut=b2884a393a59ad64002292a3e90d46a5&secid={}'.format(code)
    resp = requests.get(url,headers=headers)
    data = resp.json()['data']['klines']
    df = pd.DataFrame(data,columns=['dd'])
    new = df['dd'].str.split(',',6,expand=True)
    new.columns = ['time','ZLJE','XDJE','ZDJE','DDJE','CDJE']
    new['time'] = new['time'].str.extract("(\d\d:\d\d)")
    new['ZLJE'] = new['ZLJE'].astype(float)/10000
    new['XDJE'] = new['XDJE'].astype(float)/10000
    new['ZDJE'] = new['ZDJE'].astype(float)/10000
    new['DDJE'] = new['DDJE'].astype(float)/10000
    new['CDJE'] = new['CDJE'].astype(float)/10000
    os.system("cls")
    print(new.tail(10))
    return new



def update():
    global code
    now_time = datetime.now()
    data = fund(code)
    stringaxis = pg.AxisItem(orientation='bottom')
    xdict = dict(enumerate(data.index))
    axis_1 = [(i, list(data.index)[i]) for i in range(0, len(data.index), 10)]
    stringaxis.setTicks([axis_1,xdict.items()])
    curve_ZL = p1.plot(data['ZLJE'],pen=(102,255,255),name='主力')
    curve_CD = p1.plot(data['CDJE'],pen=(255,0,0),name='超大')
    curve_DD = p1.plot(data['DDJE'],pen=(255,200,0),name='大单')
    curve_ZD = p1.plot(data['ZDJE'],pen=(0,0,255),name='中单')
    curve_XD = p1.plot(data['XDJE'],pen=(0,255,0),name='小单')


    curve_ZL.setData(data['ZLJE'][:-1])
    curve_CD.setData(data['CDJE'][:-1])
    curve_DD.setData(data['DDJE'][:-1])
    curve_ZD.setData(data['ZDJE'][:-1])
    curve_XD.setData(data['XDJE'][:-1])




timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10000)

if __name__ == '__main__':

    """个股分时资金博弈窗口"""
    code = input('代码:')

    QtGui.QApplication.instance().exec_()

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