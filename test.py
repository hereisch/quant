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
    today = time.strftime("%Y-%m-%d", time.localtime())
    kk = db.get_collection('dayK').find({'$and': [{"date": {'$ne': today}}, {"code": '603991'}]})
    df = pd.DataFrame(list(kk))
    df = df.sort_values(by='date', ascending=False)
    topN = df[:60 + 1]['pressure'].max()
    print(df, topN)

