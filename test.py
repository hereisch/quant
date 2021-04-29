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
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as po


pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


client = pymongo.MongoClient(host="192.168.0.28", port=27017)
db = client['quant']


if __name__ == '__main__':
    # today = time.strftime("%Y-%m-%d", time.localtime())
    # kk = db.get_collection('dayK').find({'$and': [{"date": {'$ne': today}}, {"code": '603991'}]})
    # df = pd.DataFrame(list(kk))
    # df = df.sort_values(by='date', ascending=False)
    # topN = df[:60 + 1]['pressure'].max()
    # print(df, topN)



    fig = make_subplots(rows=1, cols=2, column_widths=[0.7, 0.3])
    fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]),row=1, col=1)
    fig.add_trace(go.Scatter(x=[20, 30, 40], y=[50, 60, 70]),row=1, col=2)
    fig.update_layout(
        xaxis=dict(
            # 链接到x2轴
            scaleanchor="x2",scaleratio = 1))
    layout = html.Div(
        children=[
            dcc.Graph(
                figure=fig,
                config=dict(
                    modeBarButtonsToRemove=["toggleSpikelines","hoverCompareCartesian"],
                    scrollZoom = True,))])
    po.plot(fig, )
