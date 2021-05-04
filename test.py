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
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as po


pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


client = pymongo.MongoClient(host="127.0.0.1", port=27017)
db = client['quant']


def can_vol(dataframe=None, start=80, end=180, name='Candlestick'):
    import plotly
    import numpy as np
    import plotly.graph_objects as go

    data1 = dataframe.iloc[start:end, :]  # 区间，这里我只是测试，并没有真正用时间来选
    data1 = data1.sort_index(axis=0, ascending=True)
    # 生成新列，以便后面设置颜色
    data1['diag'] = np.empty(len(data1))
    # 设置涨/跌成交量柱状图的颜色
    data1.diag[data1.close > data1.open] = '#fcf8b3'
    data1.diag[data1.close <= data1.open] = '#80ef91'
    layout = go.Layout(title_text=name, title_font_size=30, autosize=True, margin=go.layout.Margin(l=10, r=1, b=10),
                       xaxis=dict(title_text="Candlesticck", type='category'),
                       yaxis=dict(title_text="<b>Price</b>"),
                       yaxis2=dict(title_text="<b>Volume</b>", anchor="x", overlaying="y", side="right"))
    # layout的参数超级多，因为它用一个字典可以集成所有图的所有格式
    # 这个函数里layout值得注意的是 type='category'，设置x轴的格式不是candlestick自带的datetime形式，
    # 因为如果用自带datetime格式总会显示出周末空格，这个我找了好久才解决周末空格问题。。。
    candle = go.Candlestick(x=data1.index,
                            open=data1.open, high=data1.high,
                            low=data1.low, close=data1.close, increasing_line_color='#f6416c',
                            decreasing_line_color='#7bc0a3', name="Price")
    vol = go.Bar(x=data1.index,
                 y=data1.volume, name="Volume", marker_color=data1.diag, opacity=0.5, yaxis='y2')
    # 这里一定要设置yaxis=2, 确保成交量的y轴在右边，不和价格的y轴在一起
    data = [candle, vol]
    fig = go.Figure(data, layout)
    plotly.offline.plot(fig,filename='dayK.html', auto_open=False)
    return 'dayK.html'


if __name__ == '__main__':
    # today = time.strftime("%Y-%m-%d", time.localtime())
    # kk = db.get_collection('dayK').find({'$and': [{"date": {'$ne': today}}, {"code": '603991'}]})
    # df = pd.DataFrame(list(kk))
    # df = df.sort_values(by='date', ascending=False)
    # topN = df[:60 + 1]['pressure'].max()
    # print(df, topN)

    client = pymongo.MongoClient(host="127.0.0.1", port=27017)
    db = client['quant']
    result = db.get_collection('dayK').find({'code':'603990'})

    stock = pd.DataFrame(list(result))

    # 先用tushare下载数据
    import tushare as ts

    data = ts.get_hist_data('603222')


    # 定义画图函数


    can_vol(dataframe=data)