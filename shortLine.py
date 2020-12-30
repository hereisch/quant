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


if __name__ == '__main__':

    print(time.strftime("%Y-%m-%d", time.localtime()))
    # df = ts.get_realtime_quotes('000876')
    # print(df.columns.values.tolist())
    df = ts.get_realtime_quotes('000876')  # Single stock symbol
    real = df[['code', 'name', 'price', 'bid', 'ask', 'volume', 'amount', 'time']]
    print(real.columns.values.tolist())
    while True:

        df = ts.get_realtime_quotes('000876')  # Single stock symbol
        real = df[['code', 'name', 'price', 'bid', 'ask', 'volume', 'amount', 'time']]
        print(list(real.iloc[0].values))
        # print(list(df.iloc[0].values))
        time.sleep(5)

