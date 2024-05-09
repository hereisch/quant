# -*- coding: utf-8 -*-#
import os
import sys
import pandas as pd
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

def fund(code,_url='Eastmoney_flow',):
    """

    :param code: 代码
    :param _url: url类型,默认当日历史资金流
    :return:
    """
    win.setWindowTitle(code)
    if code.startswith('6'):
        code = '1.' + code 
    elif code == 'sh':
        code = '1.000001'
        win.setWindowTitle('SH')
    else:
         code = '0.' + code

    url = EastmoneyURL[_url].format(code)
    resp = requests.get(url,headers=headers)
    data = resp.json()['data']['klines']
    df = pd.DataFrame(data,columns=['dd'])
    if  df.empty:
        print('无数据/未开盘...')
        sys.exit(0)

    if _url == 'Eastmoney_flow':
        new = df['dd'].str.split(',', expand=True)
        new.columns = ['time','ZLJE','XDJE','ZDJE','DDJE','CDJE']
        new['time'] = new['time'].str.extract("(\d\d:\d\d)")
    elif _url == 'Eastmoney_history_flow':
        new = df['dd'].str.split(',', 15, expand=True)
        new.columns = ['time','ZLJE','XDJE','ZDJE','DDJE','CDJE','ZLJZB','XDJZB','ZDJZB','DDJZB','CDJZB','price','change','unknow1','unknow2']
        new['time'] = new['time'].str.extract("(\d\d-\d\d-\d\d)")

    new['ZLJE'] = new['ZLJE'].astype(float)/10000
    new['XDJE'] = new['XDJE'].astype(float)/10000
    new['ZDJE'] = new['ZDJE'].astype(float)/10000
    new['DDJE'] = new['DDJE'].astype(float)/10000
    new['CDJE'] = new['CDJE'].astype(float)/10000

    if _url == 'Eastmoney_history_flow':
        new['ZL_exist'] = new['ZLJE'].cumsum()
        new['XD_exist'] = new['XDJE'].cumsum()
        new['ZD_exist'] = new['ZDJE'].cumsum()
        new['DD_exist'] = new['DDJE'].cumsum()
        new['CD_exist'] = new['CDJE'].cumsum()

    os.system("cls")
    print(new.tail(10))
    print('主力:{}/{}\t大单:{}/{}\t超大:{}/{}\tcode:{}'.format(new.ZLJE.max(),new.ZLJE.min(),new.DDJE.max(),new.DDJE.min(),new.CDJE.max(),new.CDJE.min(),code))
    return new



def update():
    global code
    # now_time = datetime.now()
    data = fund(code)
    stringaxis = pg.AxisItem(orientation='bottom')
    xdict = dict(enumerate(data.index))
    axis_1 = [(i, list(data.index)[i]) for i in range(0, len(data.index), 10)]
    stringaxis.setTicks([axis_1,xdict.items()])
    curve_ZL = p1.plot(data['ZLJE'],pen=(102,255,255),name='主力')
    curve_CD = p1.plot(data['CDJE'],pen=(255,0,0),name='超大')
    curve_DD = p1.plot(data['DDJE'],pen=(255,200,0),name='大单')
    curve_ZD = p1.plot(data['ZDJE'],pen=(0,102,255),name='中单')
    curve_XD = p1.plot(data['XDJE'],pen=(0,255,0),name='小单')


    curve_ZL.setData(data['ZLJE'][:-1])
    curve_CD.setData(data['CDJE'][:-1])
    curve_DD.setData(data['DDJE'][:-1])
    curve_ZD.setData(data['ZDJE'][:-1])
    curve_XD.setData(data['XDJE'][:-1])



def update_his():
    global code
    now_time = datetime.now()
    data = fund(code=code,_url='Eastmoney_history_flow',)
    print(data)
    stringaxis = pg.AxisItem(orientation='bottom')
    xdict = dict(enumerate(data.index))
    axis_1 = [(i, list(data.index)[i]) for i in range(0, len(data.index), 10)]
    stringaxis.setTicks([axis_1,xdict.items()])
    curve_ZL = p1.plot(data['ZL_exist'],pen=(102,255,255),name='主力')
    curve_CD = p1.plot(data['CD_exist'],pen=(255,0,0),name='超大')
    curve_DD = p1.plot(data['DD_exist'],pen=(255,200,0),name='大单')
    curve_ZD = p1.plot(data['ZD_exist'],pen=(0,102,255),name='中单')
    curve_XD = p1.plot(data['XD_exist'],pen=(0,255,0),name='小单')


    curve_ZL.setData(data['ZL_exist'][:-1]) 
    curve_CD.setData(data['CD_exist'][:-1])
    curve_DD.setData(data['DD_exist'][:-1])
    curve_ZD.setData(data['ZD_exist'][:-1])
    curve_XD.setData(data['XD_exist'][:-1])



timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(5000)


# def his_flow(_code):
#     global code
#     code= _code
#     timer = pg.QtCore.QTimer()
#     timer.timeout.connect(update_his)
#     timer.start(5000)

#     QtGui.QApplication.instance().exec_()



if __name__ == '__main__':

    """个股分时资金博弈窗口"""
    # code = input('代码:')
    code = '002162'

    QtGui.QGuiApplication.instance().exec_()

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