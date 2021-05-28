# -*- coding: utf-8 -*-#
from datetime import datetime,date,timedelta
import json
import io
import re
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

pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


client = pymongo.MongoClient(host="192.168.0.28", port=27017)
db = client['quant']



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


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.client = pymongo.MongoClient(host="192.168.0.28", port=27017)
        self.setupUi(self)
        self.SearchButton.clicked.connect(self.dumiao)
        self._translate = QtCore.QCoreApplication.translate

    def dumiao(self):
        for i in range(30):
            print(i)
            QtWidgets.QApplication.processEvents()
            self.DownButton.setText(self._translate("MainWindow", str(i)))




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


@async_
def topN_child(Coll,topday,i,today):
    kk = db.get_collection('dayK').find({'$and': [{"date": {'$ne': today}}, {"code": i['code']}]}).sort('date', -1)
    df = pd.DataFrame(list(kk))
    count = 0
    topItem = {}
    for d in topday:
        topN = df[:d + 1]['pressure'].max()
        if i['trade'] >= topN:
            price = str(topN)
            count += 1
        else:
            price = topN
        topItem['top' + str(d)] = price
    topItem['count'] = count
    db.get_collection(Coll).update({'code': i['code']}, {'$set': topItem})


def topN(Coll='today'):
    """
    N日内最高价
    :param N:
    :return:
    """
    print('N日新高......')
    today = time.strftime("%Y-%m-%d", time.localtime())
    topday = [3, 5, 13, 21, 34, 55, 89, 144, 233]
    res = db.get_collection(Coll).find()
    start_time = time.clock()

    for i in tqdm(res):
        topN_child(Coll,topday,i,today)
    db.get_collection(Coll).remove({'top3': None})
    stop_time = time.clock()
    cost = stop_time - start_time
    print("cost %s second" % (cost))




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

    # start_time = time.clock()

    topN()

    # stop_time = time.clock()
    # cost = stop_time - start_time
    # print("cost %s second" % (cost))
