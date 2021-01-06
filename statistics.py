# -*- coding: utf-8 -*-#
import matplotlib.pyplot as plt
import pandas as pd
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

def stat(code):

    """区间成交量统计"""
    df = ts.get_today_ticks(code)
    df['amount'] = df['price']* df['vol']*100
    buy = df[df['type']=='买入']
    sale = df[df['type']=='卖出']
    s = sale.groupby(['price'])['vol'].sum()
    b = buy.groupby(['price'])['vol'].sum()

    print('买入总成交：',buy['vol'].sum(),'手')
    print('卖出总成交：',sale['vol'].sum(),'手')
    print('总买入：',buy['amount'].sum())
    print('总卖出：',sale['amount'].sum())
    print('净买入额：',(buy['amount'].sum()-sale['amount'].sum())/10000,'万')

    fig = subplots.make_subplots(rows=2, cols=1)
    traceS = go.Bar(x = list(s.to_dict().keys()),y = list(s.to_dict().values()),name='卖出',marker=dict(color='green'))
    traceB = go.Bar(x = list(b.to_dict().keys()),y = list(b.to_dict().values()),name='买入',marker=dict(color='red'))
    fig.append_trace(traceS,1,1)
    fig.append_trace(traceB,2,1)
    fig.show()


if __name__ == '__main__':

    code = input('股票代码：')
    stat(code)