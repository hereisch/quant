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
from plotly.subplots import make_subplots
import plotly.offline as po
import plotly
import numpy as np
import plotly.graph_objects as go
from plotly import subplots


pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


client = pymongo.MongoClient(host="192.168.0.28", port=27017)
db = client['quant']


def intervalStat(code,):

    """区间成交量统计"""
    df = ts.get_today_ticks(code)
    df['amount'] = df['price']* df['vol']*100
    buy = df[df['type']=='买入']
    sale = df[df['type']=='卖出']
    s = sale.groupby(['price'])['vol'].sum()
    b = buy.groupby(['price'])['vol'].sum()
    t = df.groupby(['price'])['vol'].sum()

    print('买入总成交：',buy['vol'].sum(),'手')
    print('卖出总成交：',sale['vol'].sum(),'手')
    print('总买入：',buy['amount'].sum())
    print('总卖出：',sale['amount'].sum())
    print('净买入额：',(buy['amount'].sum()-sale['amount'].sum())/10000,'万')

    # fig = subplots.make_subplots(rows=3, cols=1)
    traceS = go.Bar(x = list(s.to_dict().values()),y = list(s.to_dict().keys()),name='卖出',marker=dict(color='green'),orientation = 'h')
    traceB = go.Bar(x = list(b.to_dict().values()),y = list(b.to_dict().keys()),name='买入',marker=dict(color='red'),orientation = 'h')
    # traceT
    # = go.Bar(x = list(t.to_dict().keys()),y = list(t.to_dict().values()),name='总数',marker=dict(color='blue'))
    layout = go.Layout(barmode='stack')
    # figT = go.Figure(data=[traceB,traceS],layout=layout)
    # plotly.offline.plot(figT, filename= 'Total.html', auto_open=False)
    # figB = go.Figure(data=traceB)
    # plotly.offline.plot(figB, filename='Buy.html', auto_open=False)
    # figS = go.Figure(data=traceS)
    # plotly.offline.plot(figS, filename= 'Sale.html', auto_open=False)
    figTick = subplots.make_subplots(rows=2, cols=1)
    traceTick = go.Scatter(x=df.index,y=df['price'],marker=dict(color='gray'))
    buy = df[df['type']=='买入']
    sale = df[df['type']=='卖出']
    mid = df[df['type']=='-']
    BUY = go.Bar(x=buy.index,y=buy['vol'],marker=dict(color='red'))
    SALE = go.Bar(x=buy.index,y=sale['vol'],marker=dict(color='green'))
    MID = go.Bar(x=buy.index,y=mid['vol'],marker=dict(color='gray'))
    # po.iplot([trace,BUY,SALE,MID])

    layout = go.Layout(margin=go.layout.Margin(l=1, r=1, b=10),
                       yaxis=dict(title_text="<b>Price</b>"),
                       yaxis2=dict(title_text="<b>Volume</b>", anchor="x", overlaying="y", side="right"))
    df['color'] = ''
    df.color[df.type=='买入'] = 'red'
    df.color[df.type=='卖出'] = 'green'
    df.color[df.type=='-'] = 'gray'
    vol = go.Bar(x=df.index,y=df['vol'],marker_color=df['color'],yaxis='y2')
    data = [ traceTick,vol]
    fig = go.Figure(data,layout)
    po.plot(fig)
    # fig.append_trace(trace,1,1)
    # fig.append_trace(BUY,2,1)
    # fig.append_trace(SALE,2,1)
    # fig.append_trace(MID,2,1)
    # fig.show()



if __name__ == '__main__':
    # today = time.strftime("%Y-%m-%d", time.localtime())
    # kk = db.get_collection('dayK').find({'$and': [{"date": {'$ne': today}}, {"code": '603991'}]})
    # df = pd.DataFrame(list(kk))
    # df = df.sort_values(by='date', ascending=False)
    # topN = df[:60 + 1]['pressure'].max()
    # print(df, topN)

    client = pymongo.MongoClient(host="192.168.0.28", port=27017)
    db = client['quant']
    result = db.get_collection('dayK').find({'code':'603990'})



    intervalStat('600639')
