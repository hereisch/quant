# -*- coding: utf-8 -*-#
import json
import locale
import os
import random
from threading import Thread
from datetime import datetime,date,timedelta
import time
import pymongo
import tushare as ts
import pandas as pd
from tqdm import tqdm
from PyQt5.QtWidgets import QMainWindow
import os
from Ui_Giulia import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

client = pymongo.MongoClient(host="192.168.0.28", port=27017)
db = client['quant']

locale.setlocale(locale.LC_CTYPE, 'chinese')



def async_(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper


class Select():

    def __init__(self,init=True):
        """
        初始化，筛除688,300，ST，退市股，新股，低价股，下跌股
        """
        if init:

            data = ts.get_today_all() #今日复盘
            # data = ts.get_day_all(date='2021-02-18')   #历史复盘
            filt = data['code'].str.contains('^(?!688|300)')
            data = data[filt]
            filt = data['name'].str.contains('^(?!S|退市|\*ST)')
            data = data[filt]
            data = data.to_json(orient='records')
            db.get_collection('today').remove()
            for i in eval(data):
                db.get_collection('today').insert(i)

            res = db.get_collection('today').find()
            for i in res:
                if i['trade'] <=3 or i['changepercent'] <0:
                    db.get_collection('today').remove({'code': i['code']})
                kk = db.get_collection('base').find_one({'code': i['code']})
                if not kk:
                    db.get_collection('today').remove({'code': i['code']})

                # 行业
                industry = db.get_collection('base').find_one({'code':i['code']})
                if industry:
                    db.get_collection('today').update_many({'code':i['code']},{'$set':{'industry':industry['industry']}})


            # 剔除新股
            try:
                newStock = ts.new_stocks()
                if newStock:
                    for i in newStock['code'].tolist():
                        db.get_collection('today').remove({'code':i},multi=True)
            except:
                pass

            # 剔除停牌
            db.get_collection('today').remove({'open': 0})


    def uniqDayK(self):
        """
        dayK数据去重
        :return:
        """
        kk = db.get_collection('dayK').aggregate([{'$group': {'_id': {'date': "$date", 'code': "$code"}}}])
        for i in tqdm(kk):
            count = db.get_collection('dayK').count(i['_id'])
            if count > 1:
                print(count, i['_id'])
                db.get_collection('dayK').delete_one(i['_id'])

    #todo 获取30min，15min，5min，1min数据

    def download(self,):
        """
        增量获取数据
        :return:
        """
        res = db.get_collection('today').distinct('code')
        for i in tqdm(res):
            # print(i)
            # 查询库中是否有历史数据
            kk = db.get_collection('dayK').find({'code':i})
            kk = list(kk)
            if kk:
                # 有，获取最大日期+1，获取数据
                df = pd.DataFrame(kk)
                lastday = df['date'].max()
                nextday = (datetime.strptime(lastday, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
                today = time.strftime("%Y-%m-%d", time.localtime())
                if nextday < today:
                    time.sleep(0.5)
                    data = ts.get_hist_data(i,start=nextday)
                    if not data.empty:
                        data['pressure'] = data.apply(lambda x: max(x['open'], x['close']), axis=1)
                        data = json.loads(data.to_json(orient='index'))
                        for k, v in data.items():
                            # print(k, v)
                            v['date'] = k
                            v['code'] = i
                            db.get_collection('dayK').insert(v)

            else:
                # 无，全量获取数据
                # 次新数据少于300天，删除自选 len(index)<300
                    time.sleep(0.5)
                    data = ts.get_hist_data(i)
                    # 开盘价和收盘价对比取压力值pressure
                    data['pressure'] = data.apply(lambda x:max(x['open'],x['close']),axis=1)
                    data = json.loads(data.to_json(orient='index'))
                    for k,v in data.items():
                        # print(k,v)
                        v['date'] = k
                        v['code'] = i
                        db.get_collection('dayK').insert(v)


    def topN(self):
        """
        N日内最高价
        :param N:
        :return:
        """
        print('N日新高......')
        today = time.strftime("%Y-%m-%d", time.localtime())
        topday = [3, 5, 13, 21, 34, 55, 89, 144, 233]
        res = db.get_collection('today').find()
        for i in tqdm(res):
            kk = db.get_collection('dayK').find({ '$and' : [{"date" : { '$ne' : today }}, {"code" : i['code']}] })
            df = pd.DataFrame(list(kk))
            try:
                df = df.sort_values(by='date',ascending=False)
            except:
                continue
            for d in topday:
                topN = df[:d+1]['pressure'].max()
                if i['trade'] >= topN:
                    price = str(topN)
                else:
                    price = topN
                db.get_collection('today').update({'code':i['code']},{'$set':{'top'+str(d):price}})
        db.get_collection('today').remove({'top3': None})


# @async_
def downStock():

    print('开始下载数据....', time.strftime('%Y年%m月%d日%H时%M分%S秒'))
    s = Select(init=True)
    s.download()
    s.topN()
    # s.uniqDayK()
    print('数据下载完毕....', time.strftime('%Y年%m月%d日%H时%M分%S秒'))

@async_
def refresh():

    print('开始刷新....', time.strftime('%Y年%m月%d日%H时%M分%S秒'))
    s = Select(init=True)
    s.topN()
    print('刷新完毕....',time.strftime('%Y年%m月%d日%H时%M分%S秒'))



if __name__ == '__main__':

    downStock()
