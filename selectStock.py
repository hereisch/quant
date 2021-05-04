# -*- coding: utf-8 -*-#
import json
import locale
import os
import random
import re
import requests
from datetime import datetime,date,timedelta
import time
import pymongo
import tushare as ts
import pandas as pd
from tqdm import tqdm



pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

client = pymongo.MongoClient(host="127.0.0.1", port=27017)
db = client['quant']


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
                if i['trade'] <=9 or i['changepercent'] <0:
                    db.get_collection('today').remove({'code': i['code']})
                kk = db.get_collection('base').find_one({'code': i['code']})
                if not kk:
                    db.get_collection('today').remove({'code': i['code']})

                # 行业
                industry = db.get_collection('base').find_one({'code':i['code']})
                if industry:
                    db.get_collection('today').update_many({'code':i['code']},{'$set':{'industry':industry['industry']}})


            # 剔除新股
            newStock = ts.new_stocks()
            if newStock:
                for i in newStock['code'].tolist():
                    db.get_collection('today').remove({'code':i},multi=True)

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
                    time.sleep(1)
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
                    time.sleep(1)
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
        today = time.strftime("%Y-%m-%d", time.localtime())
        topday = [3, 5, 13, 21, 34, 55, 89, 144, 233]
        res = db.get_collection('today').find()
        for i in res:
            kk = db.get_collection('dayK').find({ '$and' : [{"date" : { '$ne' : today }}, {"code" : i['code']}] })
            df = pd.DataFrame(list(kk))
            df = df.sort_values(by='date',ascending=False)
            for d in topday:
                topN = df[:d+1]['pressure'].max()
                if i['trade'] >= topN:
                    price = str(topN)
                else:
                    price = topN
                db.get_collection('today').update({'code':i['code']},{'$set':{'top'+str(d):price}})
        db.get_collection('today').remove({'top3': None})


if __name__ == '__main__':

    today = time.strftime('%Y-%m-%d' , time.localtime())

    s = Select(init=True)
    s.download()
    s.topN()
    # s.uniqDayK()
    locale.setlocale(locale.LC_CTYPE, 'chinese')
    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'))

