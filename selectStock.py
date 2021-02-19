# -*- coding: utf-8 -*-#
import json
import os
import random
import re
import requests
from datetime import datetime,date,timedelta
import time
import pymongo
import tushare as ts
import pandas as pd
import akshare as ak
pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

client = pymongo.MongoClient(host="192.168.0.28", port=27017)
db = client['quant']


class Select():

    def __init__(self,init=True):
        """
        初始化，筛除688,300，ST，退市股，新股，低价股，下跌股
        """
        if init:
            db.get_collection('today').remove()
            data = ts.get_today_all() #今日复盘
            # data = ts.get_day_all(date='2021-02-18')   #历史复盘
            filt = data['code'].str.contains('^(?!688|300)')
            data = data[filt]
            filt = data['name'].str.contains('^(?!S|退市|\*ST)')
            data = data[filt]
            data = data.to_json(orient='records')
            for i in eval(data):
                db.get_collection('today').insert(i)

            res = db.get_collection('today').find()
            for i in res:
                if i['trade'] <=10 or i['changepercent'] <0:
                    db.get_collection('today').remove({'code': i['code']})
                kk = db.get_collection('base').find_one({'code': i['code']})
                if not kk:
                    db.get_collection('today').remove({'code': i['code']})

            # 剔除新股
            newStock = ts.new_stocks()['code'].tolist()
            for i in newStock:
                db.get_collection('today').remove({'code':i},multi=True)

            # 剔除停牌
            db.get_collection('today').remove({'open': 0})


    def uniqDayK(self):
        """
        dayK数据去重
        :return:
        """
        kk = db.get_collection('dayK').aggregate([{'$group': {'_id': {'date': "$date", 'code': "$code"}}}])
        for i in kk:
            count = db.get_collection('dayK').count(i['_id'])
            if count > 1:
                print(count, i['_id'])
                db.get_collection('dayK').delete_one(i['_id'])

    def download(self):
        """
        增量获取数据
        :return:
        """
        res = db.get_collection('today').distinct('code')
        for i in res:
            print(i)
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
                    time.sleep(1)
                    data = ts.get_hist_data(i,start=nextday)
                    data['pressure'] = data.apply(lambda x: max(x['open'], x['close']), axis=1)
                    data = json.loads(data.to_json(orient='index'))
                    for k, v in data.items():
                        print(k, v)
                        v['date'] = k
                        v['code'] = i
                        db.get_collection('dayK').insert(v)

            else:
                # 无，全量获取数据
                # 次新数据少于300天，删除自选 len(index)<300
                    time.sleep(1)
                    data = ts.get_hist_data(i)
                    # 开盘价和收盘价对比取压力值pressure
                    data['pressure'] = data.apply(lambda x:max(x['open'],x['close']),axis=1)
                    data = json.loads(data.to_json(orient='index'))
                    for k,v in data.items():
                        print(k,v)
                        v['date'] = k
                        v['code'] = i
                        db.get_collection('dayK').insert(v)


    def topN(self,N):
        """
        N日内最高价
        :param N:
        :return:
        """
        today = time.strftime("%Y-%m-%d", time.localtime())
        topday = [5, 10, 30, 60, 100, 150, 200, 270]
        res = db.get_collection('today').distinct('code')
        for i in res:
            kk = db.get_collection('dayK').find({ '$and' : [{"date" : { '$ne' : today }}, {"code" : i}] })
            df = pd.DataFrame(list(kk))
            df = df.sort_values(by='date',ascending=False)
            for d in topday:

                topN = df['pressure'].max()

            print(df,topN)


            time.sleep(10)









if __name__ == '__main__':

    today = time.strftime('%Y-%m-%d' , time.localtime())

    s = Select(init=False)
    s.download()
    # s.topN(10)



