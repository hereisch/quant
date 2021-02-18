# -*- coding: utf-8 -*-#
import json
import os
import re
import requests
import time
import pymongo
import tushare as ts
import pandas as pd
import akshare as ak
pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

client = pymongo.MongoClient(host="127.0.0.1", port=27017)
db = client['stock']


class Select():

    def __init__(self):
        res = db.get_collection('today').find()
        for i in res:
            if i['trade'] <=10 or i['changepercent'] <0:
                db.get_collection('today').remove({'code': i['code']})
            kk = db.get_collection('base').find_one({'code': i['code']})
            if not kk:
                db.get_collection('today').remove({'code': i['code']})

    def download(self):
        res = db.get_collection('today').distinct('code')
        for i in res:
            time.sleep(5)
            data = ts.get_hist_data(i)
            # todo
            # 开盘价和收盘价对比取压力值pressure
            data = json.loads(data.to_json(orient='index'))
            for k,v in data.items():
                print(k,v)
                v['date'] = k
                v['code'] = i
                db.get_collection('dayK').insert(v)


    def topN(self,day):
        pass







if __name__ == '__main__':

    today = time.strftime('%Y-%m-%d' , time.localtime())

    s = Select()
    s.download()



