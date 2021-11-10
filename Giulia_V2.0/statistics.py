# -*- coding: utf-8 -*-#
import os
import sys
import time

import matplotlib.pyplot as plt
import pandas as pd
import requests
import prettytable as pt
import plotly.graph_objs as go
from plotly import subplots
from plotly.offline import iplot,init_notebook_mode
import plotly.offline as of
import plotly as py
pyplt = py.offline.plot
import tushare as ts
pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


headers = {
    # 'Referer': 'http://data.eastmoney.com/bkzj/hy.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
}

def stat(code):

    """区间成交量统计"""
    df = ts.get_today_ticks(code=code,)
    df['amount'] = df['price']* df['vol']*100
    buy = df[df['type']=='买入']
    sale = df[df['type']=='卖出']
    s = sale.groupby(['price'])['vol'].sum()
    b = buy.groupby(['price'])['vol'].sum()
    t = df.groupby(['price'])['vol'].sum()
    print(df)
    print('买入总成交：',buy['vol'].sum(),'手')
    print('卖出总成交：',sale['vol'].sum(),'手')
    print('总买入：',buy['amount'].sum())
    print('总卖出：',sale['amount'].sum())
    print('净买入额：',(buy['amount'].sum()-sale['amount'].sum())/10000,'万')

    # fig = subplots.make_subplots(rows=3, cols=1)
    # traceS = go.Bar(x = list(s.to_dict().values()),y = list(s.to_dict().keys()),name='卖出',marker=dict(color='green'),orientation = 'h')
    # traceB = go.Bar(x = list(b.to_dict().values()),y = list(b.to_dict().keys()),name='买入',marker=dict(color='red'),orientation = 'h')
    # # traceT
    # # = go.Bar(x = list(t.to_dict().keys()),y = list(t.to_dict().values()),name='总数',marker=dict(color='blue'))
    # fig.append_trace(traceS,1,1)
    # fig.append_trace(traceB,2,1)
    # fig.add_trace(traceB,row=3,col=1)
    # fig.add_trace(traceS,row=3,col=1)
    # fig.update_layout(barmode='stack')
    # fig.show()


def fundStock(code:str):
    """个股资金查询"""

    code = '1.' + code if code.startswith('6') else '0.' + code
    while True:

        os.system("cls")  # 清屏需在终端中运行
        url = 'http://push2.eastmoney.com/api/qt/stock/get?ut=b2884a393a59ad64002292a3e90d46a5&secid={}&fields=f469,f137,f193,f140,f194,f143,f195,f146,f196,f149,f197,f470,f434,f454,f435,f455,f436,f456,f437,f457,f438,f458,f471,f459,f460,f461,f462,f463,f464,f465,f466,f467,f468,f170,f119,f291'.format(code)
        resp = requests.get(url,headers=headers)
        data = resp.json()['data']
        # print('涨幅：{}%'.format(data['f170']/100))
        # print('主力净流入：{}万，主力净占比：{}万'.format(data['f137']/10000,data['f193']/100))
        # print('超大净流入：{}万，超大净占比：{}万'.format(data['f140']/10000,data['f194']/100))
        # print('大单净流入：{}万，大单净占比：{}万'.format(data['f143']/10000,data['f195']/100))
        # print('中单净流入：{}万，中单净占比：{}万'.format(data['f146']/10000,data['f196']/100))
        # print('小单净流入：{}万，小单净占比：{}万'.format(data['f149']/10000,data['f197']/100))
        tb = pt.PrettyTable()
        tb.field_names =[' '.format(data['f170']/100),'今日（万）{}%'.format(data['f170']/100),'今日占比','5日（万）{}%'.format(data['f119']/100),'5日占比','10日（万）{}%'.format(data['f291']/100),'10日占比']
        tb.add_row(['主力',data['f137']/10000,data['f193']/100,data['f434']/10000,data['f454']/100,data['f459']/10000,data['f460']/100])
        tb.add_row(['超大',data['f140']/10000,data['f194']/100,data['f435']/10000,data['f455']/100,data['f461']/10000,data['f462']/100])
        tb.add_row(['大单',data['f143']/10000,data['f195']/100,data['f436']/10000,data['f456']/100,data['f463']/10000,data['f464']/100])
        tb.add_row(['中单',data['f146']/10000,data['f196']/100,data['f437']/10000,data['f457']/100,data['f465']/10000,data['f466']/100])
        tb.add_row(['小单',data['f149']/10000,data['f197']/100,data['f438']/10000,data['f458']/100,data['f467']/10000,data['f468']/100])

        print(tb)

        time.sleep(5)




if __name__ == '__main__':

    # code = input('代码：')
    # stat('601727')

    fundStock('002169')

