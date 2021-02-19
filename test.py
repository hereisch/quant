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

    res = db.get_collection('today').distinct('code')
    for i in res[2:]:
        print(i)
        kk = db.get_collection('dayK').find({'code': i})
        df = pd.DataFrame(list(kk))
        # df = 除今日外切片-today
        topN = df['pressure'].max()
        print(topN)
        print(df)

        time.sleep(10)

