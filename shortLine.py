# -*- coding: utf-8 -*-#
import json
import os
import re
import requests
import time
import tushare as ts
import pymongo
import pandas as pd

# pd.set_option('display.height',1000)
pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def realTime(code):
    """
    获取当日实时成交
    :param code:
    :return:
    """
    df = ts.get_realtime_quotes(code)  # Single stock symbol
    real = df[['code', 'name', 'price', 'bid', 'ask', 'volume', 'amount', 'time']]
    print(real.columns.values.tolist())
    while True:
        df = ts.get_realtime_quotes(code)  # Single stock symbol
        real = df[['code', 'name', 'price', 'bid', 'ask', 'volume', 'amount', 'time']]
        print(list(real.iloc[0].values))
        # print(list(df.iloc[0].values))
        time.sleep(5)

def todayQuotes(code):
    """
    获取当日历史分笔数据，复盘用
    :param code:
    :return:
    """
    df = ts.get_today_ticks(code)
    print(df)



if __name__ == '__main__':

    code = input('股票代码：')
    print(time.strftime("%Y-%m-%d", time.localtime()))
    # df = ts.get_realtime_quotes(code)
    # print(df.columns.values.tolist())
    realTime(code)
    # todayQuotes(code)



