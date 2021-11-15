# -*- coding: utf-8 -*-#
import random
from datetime import datetime,date,timedelta
import json
import io
import re
from threading import Thread
import matplotlib.pyplot as plt
import pandas as pd
import pymongo
import requests
import time
import tushare as ts
import pandas as pd
from plotly.subplots import make_subplots
import plotly.offline as po
import plotly
import numpy as np
import plotly.graph_objects as go
from plotly import subplots
from tqdm import tqdm
from datetime import datetime, date, timedelta
import scipy.signal as signal




pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


client = pymongo.MongoClient(host="192.168.0.28", port=27017)
db = client['quant']


headers = {
    # 'Accept': '*/*',
    # 'Accept-Encoding': 'gzip, deflate',
    # 'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Cookie': '__51cke__=; Hm_lvt_34e0d77f0c897023357dcfa7daa006f3=1626846961; d_ddx=1626846965; Hm_lpvt_34e0d77f0c897023357dcfa7daa006f3=1626846985; __tins__1523105=%7B%22sid%22%3A%201626849104630%2C%20%22vd%22%3A%202%2C%20%22expires%22%3A%201626851989983%7D; __51laig__=11',
    # 'Host': 'ddx.gubit.cn',
    # 'Referer': 'http://ddx.gubit.cn/xg/xuangu2.html',
    # 'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
}


def async_(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

import sys
from Ui_Giulia import Ui_MainWindow
import tushare as ts
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import plotly.graph_objects as go
from PyQt5 import QtCore, QtGui, QtWidgets
from selectStock import async_

pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)







def voice():
    # 语音播报模块
    import pyttsx3

    msg = ''' here you are ,are you ok
        '''
    # 模块初始化
    engine = pyttsx3.init()
    volume = engine.getProperty('volume')

    # 标准的粤语发音
    voices = engine.setProperty('voice', "com.apple.speech.synthesis.voice.sin-ji")

    # 普通话发音
    # voices = engine.setProperty(
    #     'voice', "com.apple.speech.synthesis.voice.ting-ting.premium")

    # 台湾甜美女生普通话发音
    # voices = engine.setProperty(
    #     'voice', "com.apple.speech.synthesis.voice.mei-jia")
    print('准备开始语音播报...')
    # 输入语音播报词语
    engine.setProperty('volume', 0.7)
    engine.say(msg)

    engine.runAndWait()



def sendMSG(msg='test'):
    KEY = '580f5ca93c8f068fb01ed010d4815f5f'
    data = {
        "msg": msg,  # 需要发送的消息
        "qq": "694749274"  # 需要接收消息的QQ号码
    }

    url = 'https://qmsg.zendee.cn/send/' + KEY
    resp = requests.post(url, data=data)
    print(resp.json())




def support(code='',ktype='30'):
    # day = 1440 min
    df = ts.get_k_data('600639', ktype='30')
    df['support'] = df.apply(lambda x: min(x['open'], x['close']), axis=1)
    df['pressure'] = df.apply(lambda x: max(x['open'], x['close']), axis=1)
    sup = df['support'][0:48].values
    pre = df['pressure'][0:48].values
    print(sup)
    print(pre)
    # x=np.array([
    #     0, 6, 25, 20, 15, 8, 15, 6, 0, 6, 0, -5, -15, -3, 4, 10, 8, 13, 8, 10, 3,1, 20, 7, 3, 0 ])
    plt.figure(figsize=(16, 4))
    plt.plot(np.arange(len(sup)), sup)
    plt.plot(np.arange(len(pre)), pre)
    # print(x[signal.argrelextrema(x, np.greater)])
    # print(signal.argrelextrema(x, np.greater))
    print('极大值坐标', signal.argrelextrema(pre, np.greater)[0])
    print('极大值', pre[signal.argrelextrema(pre, np.greater)])
    print('极小值', sup[signal.argrelextrema(-sup, np.greater)])
    print('坐标', signal.argrelextrema(-sup, np.greater)[0])
    plt.plot(signal.argrelextrema(sup, np.greater)[0], sup[signal.argrelextrema(sup, np.greater)], 'o')  # 极大值
    plt.plot(signal.argrelextrema(-sup, np.greater)[0], sup[signal.argrelextrema(-sup, np.greater)], '+')  # 极小值

    plt.plot(signal.argrelextrema(pre, np.greater)[0], pre[signal.argrelextrema(pre, np.greater)], 'o')  # 极大值
    plt.plot(signal.argrelextrema(-pre, np.greater)[0], pre[signal.argrelextrema(-pre, np.greater)], '+')  # 极小值
    # plt.plot(peakutils.index(-x),x[peakutils.index(-x)],'*')
    plt.show()



def MA(df, n,ksgn='close'):
    '''
    def MA(df, n,ksgn='close'):
    #Moving Average
    MA是简单平均线，也就是平常说的均线
    【输入】
        df, pd.dataframe格式数据源
        n，时间长度
        ksgn，列名，一般是：close收盘价
    【输出】
        df, pd.dataframe格式数据源,
        增加了一栏：ma_{n}，均线数据
    '''
    xnam='ma{n}'.format(n=n)
    #ds5 = pd.Series(pd.rolling_mean(df[ksgn], n), name =xnam)
    ds2=pd.Series(df[ksgn], name =xnam,index=df.index);
    ds5 = ds2.rolling(center=False,window=n).mean()
    #print(ds5.head()); print(df.head())
    #
    df = df.join(ds5)
    #
    return df

def stat():
    df = ts.get_tick_data('002547', date='2021-06-10', src='tt')
    print(df)
    buy = df[df['type'] == '买盘']
    sale = df[df['type'] == '卖盘']
    s = sale.groupby(['price'])['volume'].sum()
    b = buy.groupby(['price'])['volume'].sum()
    t = df.groupby(['price'])['volume'].sum()
    print('买入总成交：', buy['volume'].sum(), '手')
    print('卖出总成交：', sale['volume'].sum(), '手')
    print('总买入：', buy['amount'].sum())
    print('总卖出：', sale['amount'].sum())
    print('净买入额：', (buy['amount'].sum() - sale['amount'].sum()) / 10000, '万')



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
    # print(new)
    return new





if __name__ == '__main__':


    client = pymongo.MongoClient(host="192.168.0.28", port=27017)
    db = client['quant']
    now = time.strftime('%m-%d  %H:%M:%S')
    today = time.strftime("%Y-%m-%d", time.localtime())
    yesterday = (date.today() + timedelta(-1)).strftime('%Y-%m-%d')
    day2ago = (date.today() + timedelta(-2)).strftime('%Y-%m-%d')
    # app = QApplication(sys.argv)
    # win = MainWindow()
    # win.show()
    # # win.showMaximized(ter
    # app.exec_()

    # 二进三 复盘查找两连板 昨天，前天 涨幅>9.8 ,进入打板池
    #  T字板 ：open == high == close >9.8  >low
    # 打板池轮询开板，通知
    # 参考   岳阳林纸， 山东墨龙 三星医疗，汇洁股份，圣济堂，锦鸿集团，小康股份，宜宾纸业




    # 补0占位
    # print('{:0>2d}'.format(3))

    # base = db.get_collection('base').find()
    # industry = {i['code']: i['name'] for i in base}




    # df = ts.get_sina_dd('600023',date='2021-10-28')
    # print(df)
    # a = 'http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill_all.php?num=100&page=1&sort=ticktime&asc=0&volume=40000&type=0&symbol=sh600023'

    # db.get_collection('NMC').remove()
    # data = ts.get_today_all()
    # filt = data['code'].str.contains('^(?!8|688)')
    # data = ts.get_today_all()
    # filt = data['name'].str.contains('^(?!S|退市|\*ST)')
    # data = data[filt]
    # data = data.to_json(orient='records')
    # for i in eval(data):
    #     db.get_collection('NMC').insert(i)
    res = db.get_collection('NMC').find()
    nmc = {i['code']:i['nmc']/100000000 for i in res}
    print(nmc)



