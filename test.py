# -*- coding: utf-8 -*-#
from datetime import datetime,date,timedelta
import json
import os
import re
import pandas as pd
import pymongo
import requests
import time
import tushare as ts

pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


client = pymongo.MongoClient(host="192.168.0.28", port=27017)
db = client['quant']


if __name__ == '__main__':
    # today = time.strftime("%Y-%m-%d", time.localtime())
    # kk = db.get_collection('dayK').find({'$and': [{"date": {'$ne': today}}, {"code": '603991'}]})
    # df = pd.DataFrame(list(kk))
    # df = df.sort_values(by='date', ascending=False)
    # topN = df[:60 + 1]['pressure'].max()
    # print(df, topN)

    import mongoengine
    mongoengine.connect('quant',host='192.168.0.28',port=27017)


    class Users(mongoengine.Document):
        meta = {'collection':'today'}
        name = mongoengine.StringField(required=True, max_length=200)
        age = mongoengine.IntField(required=True)


    users = Users.objects.all()  # 返回所有的文档对象列表

    for u in users:
        print("name:", u.name, ",age:", u.age)
