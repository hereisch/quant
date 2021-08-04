# -*- coding: utf-8 -*-#
import json
import os
import re
from threading import Thread
from datetime import datetime, date, timedelta
import pymongo
import requests
import time
import tushare as ts
from CONSTANT import MONGOHOST


def async_(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper



def sendMSG(msg='test'):
    KEY = '580f5ca93c8f068fb01ed010d4815f5f'
    data = {
        "msg": msg,  # 需要发送的消息
        "qq": "694749274"  # 需要接收消息的QQ号码
    }

    url = 'https://qmsg.zendee.cn/send/' + KEY
    resp = requests.post(url, data=data)
    print(msg)


@async_
def supervisory(label=0):
    """
    打板监控
    :param label: 12：一进二  23：二进三  99：厂字板
    :return:
    """
    if label == 0:
        return 0
    global impact23
    global impact12
    global impact99
    if label == 12:
        for code in impact12:
            time.sleep(0.5)
            df = ts.get_realtime_quotes(code)
            # print('get_realtime_quotes12',code)
            if eval(df['price'][0]) < eval(df['open'][0]):
                scope = round((eval(df['price'][0])/eval(df['open'][0])-1)*100,2)
                # 开板幅度大于-2%
                if scope > -3:
                    msg = '一进二：\n代码：{}\n名称：{}\n现价：{}\n涨幅：{}\n{}'.format(code, name[code],df['price'][0], scope, time.strftime('%m-%d  %H:%M:%S'))
                    sendMSG(msg=msg)
                time.sleep(200)
    elif label == 23:
        for code in impact23:
            time.sleep(0.5)
            df = ts.get_realtime_quotes(code)
            # print('get_realtime_quotes23', code)

            if eval(df['price'][0]) < eval(df['open'][0]):
                scope = round((eval(df['price'][0]) / eval(df['open'][0]) - 1) * 100, 2)
                if scope >-3:
                    msg = '二进三：\n代码：{}\n名称：{}\n现价：{}\n涨幅：{}\n{}'.format(code, name[code],df['price'][0], scope, time.strftime('%m-%d  %H:%M:%S'))
                    sendMSG(msg=msg)
                time.sleep(200)

    elif label == 99:
        for code in impact99:
            df = ts.get_realtime_quotes(code)
            scope = round((eval(df.open[0]) / eval(df.pre_close[0])-1)*100,2)
            if 9.5 > scope > 6:
                msg = '厂字开板：\n代码：{}\n名称：{}\n现价：{}\n涨幅：{}\n{}'.format(code, name[code], df['price'][0], scope, time.strftime('%m-%d  %H:%M:%S'))
                sendMSG(msg=msg)
            time.sleep(1)


def initBoard(board='',label=0):

    """
        开板初始化，9:30后执行
        删除非涨停股
    :param board:
    :param label:
    :return:
    """
    global impact12
    global impact23
    global impact99

    if label == 12:
        for code in board:
            stock = ts.get_realtime_quotes(code)
            if eval(stock.open[0]) / eval(stock.pre_close[0]) > 1.09:
                impact12.append(stock.code[0])
                db.get_collection('impact1to2').update({'code':stock.code[0]},{'$set':{'contBoard':True}})
        print('一进二：', impact12)

    elif label ==23:
        for code in board:
            stock = ts.get_realtime_quotes(code)
            if eval(stock.open[0]) / eval(stock.pre_close[0]) > 1.09:
                impact23.append(stock.code[0])
                db.get_collection('impact2to3').update({'code':stock.code[0]},{'$set':{'contBoard':True}})
        print('二进三：', impact23)

    elif label == 99:
        board1 = db.get_collection('impact1to2').distinct('code',{'contBoard':{'$ne':True}})
        for i in board1:
            stock = ts.get_realtime_quotes(i)
            if eval(stock.open[0]) / eval(stock.pre_close[0]) > 1.04:
                    impact99.append(i)
            time.sleep(1)
        board2 = db.get_collection('impact2to3').distinct('code',{'contBoard':{'$ne':True}})
        for i in board2:
            stock = ts.get_realtime_quotes(i)
            if eval(stock.open[0]) / eval(stock.pre_close[0]) > 1.04:
                    impact99.append(i)
            time.sleep(1)

        print('厂字板：',impact99)


def stockPool():
    """
    自选监控
    30min、15min、5min极值支撑位
    """
    # 获取30min
    df = ts
    # 筛选压力、支撑



if __name__ == '__main__':

    client = pymongo.MongoClient(host= MONGOHOST , port=27017)
    db = client['quant']
    print('开板预警....')
    open_time = datetime.strptime(str(datetime.now().date()) + '9:30', '%Y-%m-%d%H:%M')
    close_time = datetime.strptime(str(datetime.now().date()) + '15:00', '%Y-%m-%d%H:%M')
    forenoon = datetime.strptime(str(datetime.now().date()) + '11:30', '%Y-%m-%d%H:%M')
    afternoon = datetime.strptime(str(datetime.now().date()) + '13:30', '%Y-%m-%d%H:%M')

    #开板初始化，开板保持涨停
    impact23 = []
    impact12 = []
    impact99 = []
    board2to3 = db.get_collection('impact2to3').distinct('code')
    board1to2 = db.get_collection('impact1to2').distinct('code')
    initBoard(board=board2to3, label=23)
    initBoard(board=board1to2, label=12)
    initBoard(label=99)
    res = db.get_collection('base').find()
    name = {i['code']:i['name'] for i in res}

    while True:
        now_time = datetime.now()
        if open_time < now_time <forenoon or afternoon < now_time < close_time:
            supervisory(label=23)
            supervisory(label=12)
            # supervisory(label=99)
            time.sleep(120)
        elif open_time > now_time:
            print('未开盘，等待...')
            time.sleep(120)
        elif now_time > close_time:
            print('非交易时间...')
            break

        else:
            print('午间休盘....',now_time)
            time.sleep(600)



