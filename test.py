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

if __name__ == '__main__':
    today = time.strftime('%Y-%m-%d' , time.localtime())
    client = pymongo.MongoClient(host="192.168.0.28", port=27017)
    db = client['quant']
    res = db.get_collection('stk_base').find()

    for i in res:
        if not i['code'].startswith('3'):
            time.sleep(10)
            # code = '{0:06d}'.format(int(i['code']))
            # db.get_collection('stk_base').update_many({'_id':i['_id']},{'$set':{'code':str(code)}})
            # data = ts.get_hist_data(i['code'],start='2020-12-01',end=today)
            data = ts.get_hist_data(i['code'])
            print(data)
