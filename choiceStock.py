# -*- coding: utf-8 -*-#
import json
import os
import re
import requests
import time
import tushare as ts
import pandas as pd

# pd.set_option('display.height',1000)
pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


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


if __name__ == '__main__':

   capTops()
   #  topList()