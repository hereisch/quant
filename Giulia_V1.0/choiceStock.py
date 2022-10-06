# -*- coding: utf-8 -*-#
import json
import os
import re
import json
import pymongo
import requests
import time
import tushare as ts
import pandas as pd

# pd.set_option('display.height',1000)
pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


client = pymongo.MongoClient(host='127.0.0.1',port=27017)
db = client['stock']

def capTops():
    """
       获取近5、10、30、60日个股上榜统计数据,包括上榜次数、累积购买额、累积卖出额、净额、买入席位数和卖出席位数
       """
    try:
        day = int(input('近天数(5、10、30、60)：'))
    except:
        day = 10
        print('默认10天')
    cap = ts.cap_tops(days=day)
    print('\n')
    print(cap.sort_values(by=['bamount', 'count'], ascending=(False, False)))


def topList():
    """今日上榜"""
    top = ts.top_list()
    print(top.sort_values(by=['pchange'], ascending=(False)))


def choice():

    data = ts.get_today_all()
    filt = data['code'].str.contains('^(?!688|300)')
    data = data[filt]
    filt = data['name'].str.contains('^(?!ST|退市|\*ST)')
    data = data[filt]
    # 筛选出涨幅>0,80>收盘价>10
    result = data[(data['changepercent'] > 2) & (data['trade'] > 10) & (data['trade'] < 100)].sort_values(by=['changepercent'],ascending=(False))
    print('\n', result)



if __name__ == '__main__':

    # capTops()
    # topList()
    # choice()
    ts.new_stocks()