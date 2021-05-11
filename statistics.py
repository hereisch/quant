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
    t = df.groupby(['price'])['vol'].sum()

    print('买入总成交：',buy['vol'].sum(),'手')
    print('卖出总成交：',sale['vol'].sum(),'手')
    print('总买入：',buy['amount'].sum())
    print('总卖出：',sale['amount'].sum())
    print('净买入额：',(buy['amount'].sum()-sale['amount'].sum())/10000,'万')

    fig = subplots.make_subplots(rows=3, cols=1)
    traceS = go.Bar(x = list(s.to_dict().values()),y = list(s.to_dict().keys()),name='卖出',marker=dict(color='green'),orientation = 'h')
    traceB = go.Bar(x = list(b.to_dict().values()),y = list(b.to_dict().keys()),name='买入',marker=dict(color='red'),orientation = 'h')
    # traceT
    # = go.Bar(x = list(t.to_dict().keys()),y = list(t.to_dict().values()),name='总数',marker=dict(color='blue'))
    fig.append_trace(traceS,1,1)
    fig.append_trace(traceB,2,1)
    fig.add_trace(traceB,row=3,col=1)
    fig.add_trace(traceS,row=3,col=1)
    fig.update_layout(barmode='stack')
    fig.show()


if __name__ == '__main__':

    code = '600059'
    stat(code)