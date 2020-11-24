# -*- coding: utf-8 -*-#
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objs as go
from plotly import subplots
from plotly.offline import iplot,init_notebook_mode
import plotly.offline as of
import plotly
import tushare as ts


def MACD(df, n_fast, n_slow, ksgn='close'):
    '''
    def MACD(df, n_fast, n_slow):
      #MACD指标信号和MACD的区别, MACD Signal and MACD difference
	MACD是查拉尔·阿佩尔(Geral Appel)于1979年提出的，由一快及一慢指数移动平均（EMA）之间的差计算出来。
	“快”指短时期的EMA，而“慢”则指长时期的EMA，最常用的是12及26日EMA：

    【输入】
        df, pd.dataframe格式数据源
        n，时间长度
        ksgn，列名，一般是：close收盘价
    【输出】
        df, pd.dataframe格式数据源,
        增加了3栏：macd,sign,mdiff
    '''
    xnam = 'macd'.format(n=n_fast, n2=n_slow)
    xnam2 = 'msign'.format(n=n_fast, n2=n_slow)
    xnam3 = 'mdiff'.format(n=n_fast, n2=n_slow)
    EMAfast = df[ksgn].ewm(span=n_fast, min_periods=n_slow - 1).mean()
    EMAslow = df[ksgn].ewm(span=n_slow, min_periods=n_slow - 1).mean()
    MACD = pd.Series(EMAfast - EMAslow, name=xnam)
    MACDsign = MACD.ewm(span=9, min_periods=8).mean()
    MACDsign.name = xnam2
    MACDdiff = pd.Series(MACD - MACDsign, name=xnam3)
    df = df.join(MACD)
    df = df.join(MACDsign)
    df = df.join(MACDdiff)
    return df


def MA(df, n,ksgn='close'):
    '''
    def MA(df, n,ksgn='close'):
    #Moving Average
    MA是简单平均线，也就是平常说的均线
    【输入】
        df, pd.dataframe格式数据源
        n，时间长度
        ksgn，列名，一般是：close收盘价
    【输出】
        df, pd.dataframe格式数据源,
        增加了一栏：ma_{n}，均线数据
    '''
    xnam='ma_{n}'.format(n=n)
    #ds5 = pd.Series(pd.rolling_mean(df[ksgn], n), name =xnam)
    ds2=pd.Series(df[ksgn], name =xnam,index=df.index);
    ds5 = ds2.rolling(center=False,window=n).mean()
    #print(ds5.head()); print(df.head())
    #
    df = df.join(ds5)
    #
    return df



def draw():

    code = input("input code:")
    df = pd.read_csv('TQDat/day/stk/{}.csv'.format(code))
    df = df.sort_index(ascending=False)
    layout = go.Layout(title='quant')

    close = go.Scatter(x=df['date'],y=df['close'],mode='lines',name='close',line=dict(color='rgba(255, 182, 193)', width=1)
        #     marker=dict(
        #     size='16',
        #     color = np.random.randn(500)
        #     colorscale=colorscale,
        #     showscale=True
        #   )
    )
    open = go.Scatter(x=df['date'],y=df['open'],mode='lines',name='open',line=dict(color='rgba(255, 10, 10)', width=1))


    mean = df[['open', 'high', 'low', 'close']].mean(1)
    avg = go.Scatter(x=df['date'],y=mean,mode='lines',name='avg',line=dict(color='rgba(100, 182, 193)', width=1))


    m5 = MA(df,5,)
    m10 = MA(df,10,)
    m26 = MA(df,26,)
    ma5 = go.Scatter(x=df['date'],y=m5['ma_5'],name='ma5')
    ma10 = go.Scatter(x=df['date'],y=m10['ma_10'],name='ma10')
    ma26 = go.Scatter(x=df['date'],y=m26['ma_26'],name='ma26')

    macd = MACD(df,5,26)
    macd_up = go.Bar(x=macd[macd.macd>0]['date'],y=macd[macd.macd>0]['macd'],name='macd_up',marker=dict(color='red'))
    macd_down = go.Bar(x=macd[macd.macd<0]['date'],y=macd[macd.macd<0]['macd'],name='macd_down',marker=dict(color='green'))


    '''
    marker ----> 图形的样式，可单个数据使用或者字典
    '''
    # 传入绘图数据
    data = [close, open]

    # 绘图
    # of.plot(data)
    '''将graph部分和layout部分组合成figure对象'''
    fig = subplots.make_subplots(rows=2, cols=1, )
    # fig = go.Figure(data=data,layout=layout)
    fig.append_trace(close, 1, 1)
    # fig.append_trace(open, 1, 1)
    # fig.append_trace(avg, 1, 1)
    fig.append_trace(ma5, 1, 1)
    fig.append_trace(ma10, 1, 1)
    fig.append_trace(ma26, 1, 1)
    fig.append_trace(macd_up, 1, 1)
    fig.append_trace(macd_down, 1, 1)


    '''启动绘图直接绘制figure对象'''
    # plotly.offline.init_notebook_mode()
    # plotly.offline.iplot(fig, filename='basic-scatter')
    fig.show()


if __name__ == '__main__':


    draw()

    # code = input("input code:")
    # df = pd.read_csv('TQDat/day/stk/{}.csv'.format(code))
    # df = df.sort_index(ascending=False)
    # macd = MACD(df,5,26)
    # print(macd)




