# -*- coding: utf-8 -*-#
import random
from datetime import datetime,date,timedelta
import json
import io
import re
from threading import Thread
import matplotlib.pyplot as plt
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
from tqdm import tqdm
from datetime import datetime, date, timedelta
import scipy.signal as signal
from sklearn.model_selection import train_test_split
import sklearn
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei', 'FangSong']  # 汉字字体,优先使用楷体，如果找不到楷体，则使用黑体
mpl.rcParams['font.size'] = 12  # 字体大小
mpl.rcParams['axes.unicode_minus'] = False  # 正常显示负号



pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


client = pymongo.MongoClient(host="192.168.0.28", port=27017)
db = client['quant']


headers = {
    # 'Accept': '*/*',
    # 'Accept-Encoding': 'gzip, deflate',
    # 'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Cookie': '__51cke__=; Hm_lvt_34e0d77f0c897023357dcfa7daa006f3=1626846961; d_ddx=1626846965; Hm_lpvt_34e0d77f0c897023357dcfa7daa006f3=1626846985; __tins__1523105=%7B%22sid%22%3A%201626849104630%2C%20%22vd%22%3A%202%2C%20%22expires%22%3A%201626851989983%7D; __51laig__=11',
    # 'Host': 'ddx.gubit.cn',
    # 'Referer': 'http://ddx.gubit.cn/xg/xuangu2.html',
    # 'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
}


def async_(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

import sys
from Ui_Giulia import Ui_MainWindow
import tushare as ts
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import plotly.graph_objects as go
from PyQt5 import QtCore, QtGui, QtWidgets
from selectStock import async_

pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)







def voice():
    # 语音播报模块
    import pyttsx3

    msg = ''' here you are ,are you ok
        '''
    # 模块初始化
    engine = pyttsx3.init()
    volume = engine.getProperty('volume')

    # 标准的粤语发音
    voices = engine.setProperty('voice', "com.apple.speech.synthesis.voice.sin-ji")

    # 普通话发音
    # voices = engine.setProperty(
    #     'voice', "com.apple.speech.synthesis.voice.ting-ting.premium")

    # 台湾甜美女生普通话发音
    # voices = engine.setProperty(
    #     'voice', "com.apple.speech.synthesis.voice.mei-jia")
    print('准备开始语音播报...')
    # 输入语音播报词语
    engine.setProperty('volume', 0.7)
    engine.say(msg)

    engine.runAndWait()



def sendMSG(msg='test'):
    KEY = '580f5ca93c8f068fb01ed010d4815f5f'
    data = {
        "msg": msg,  # 需要发送的消息
        "qq": "694749274"  # 需要接收消息的QQ号码
    }

    url = 'https://qmsg.zendee.cn/send/' + KEY
    resp = requests.post(url, data=data)
    print(resp.json())




def support(code='',ktype='30'):
    # day = 1440 min
    df = ts.get_k_data('600639', ktype='30')
    df['support'] = df.apply(lambda x: min(x['open'], x['close']), axis=1)
    df['pressure'] = df.apply(lambda x: max(x['open'], x['close']), axis=1)
    sup = df['support'][0:48].values
    pre = df['pressure'][0:48].values
    print(sup)
    print(pre)
    # x=np.array([
    #     0, 6, 25, 20, 15, 8, 15, 6, 0, 6, 0, -5, -15, -3, 4, 10, 8, 13, 8, 10, 3,1, 20, 7, 3, 0 ])
    plt.figure(figsize=(16, 4))
    plt.plot(np.arange(len(sup)), sup)
    plt.plot(np.arange(len(pre)), pre)
    # print(x[signal.argrelextrema(x, np.greater)])
    # print(signal.argrelextrema(x, np.greater))
    print('极大值坐标', signal.argrelextrema(pre, np.greater)[0])
    print('极大值', pre[signal.argrelextrema(pre, np.greater)])
    print('极小值', sup[signal.argrelextrema(-sup, np.greater)])
    print('坐标', signal.argrelextrema(-sup, np.greater)[0])
    plt.plot(signal.argrelextrema(sup, np.greater)[0], sup[signal.argrelextrema(sup, np.greater)], 'o')  # 极大值
    plt.plot(signal.argrelextrema(-sup, np.greater)[0], sup[signal.argrelextrema(-sup, np.greater)], '+')  # 极小值

    plt.plot(signal.argrelextrema(pre, np.greater)[0], pre[signal.argrelextrema(pre, np.greater)], 'o')  # 极大值
    plt.plot(signal.argrelextrema(-pre, np.greater)[0], pre[signal.argrelextrema(-pre, np.greater)], '+')  # 极小值
    # plt.plot(peakutils.index(-x),x[peakutils.index(-x)],'*')
    plt.show()



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
    xnam='ma{n}'.format(n=n)
    #ds5 = pd.Series(pd.rolling_mean(df[ksgn], n), name =xnam)
    ds2=pd.Series(df[ksgn], name =xnam,index=df.index);
    ds5 = ds2.rolling(center=False,window=n).mean()
    #print(ds5.head()); print(df.head())
    #
    df = df.join(ds5)
    #
    return df

def stat():
    df = ts.get_tick_data('002547', date='2021-06-10', src='tt')
    print(df)
    buy = df[df['type'] == '买盘']
    sale = df[df['type'] == '卖盘']
    s = sale.groupby(['price'])['volume'].sum()
    b = buy.groupby(['price'])['volume'].sum()
    t = df.groupby(['price'])['volume'].sum()
    print('买入总成交：', buy['volume'].sum(), '手')
    print('卖出总成交：', sale['volume'].sum(), '手')
    print('总买入：', buy['amount'].sum())
    print('总卖出：', sale['amount'].sum())
    print('净买入额：', (buy['amount'].sum() - sale['amount'].sum()) / 10000, '万')



def fund(code):

    code = '1.' + code if code.startswith('6') else '0.' + code
    url = 'http://push2.eastmoney.com/api/qt/stock/fflow/kline/get?lmt=0&klt=1&fields1=f1%2Cf2%2Cf3%2Cf7&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61%2Cf62%2Cf63%2Cf64%2Cf65&ut=b2884a393a59ad64002292a3e90d46a5&secid={}'.format(code)
    resp = requests.get(url,headers=headers)
    data = resp.json()['data']['klines']
    df = pd.DataFrame(data,columns=['dd'])
    new = df['dd'].str.split(',',6,expand=True)
    new.columns = ['time','ZLJE','XDJE','ZDJE','DDJE','CDJE']
    new['time'] = new['time'].str.extract("(\d\d:\d\d)")
    new['ZLJE'] = new['ZLJE'].astype(float)/10000
    new['XDJE'] = new['XDJE'].astype(float)/10000
    new['ZDJE'] = new['ZDJE'].astype(float)/10000
    new['DDJE'] = new['DDJE'].astype(float)/10000
    new['CDJE'] = new['CDJE'].astype(float)/10000
    # print(new)
    return new



def getDDXData():
    base = db.get_collection('base').find()
    industry = {i['code']: i['name'] for i in base}
    res = db.get_collection('NMC').find()
    nmc = {i['code']: round(i['nmc'] / 10000, 2) for i in res}

    ddx_config = ['代码', '最新价', '涨幅', '换手率', '量比', 'DDX1日', 'DDY1日', 'DDZ', 'DDX3日', 'DDX5日', 'DDX10日', 'DDX60日', 'DDX5红', 'DDX10红', 'DDX连红', 'DDX连增', '涨幅3日', '涨幅5日', '涨幅10日', 'DDY3日', 'DDY5日',
                  'DDY10日','DDY60日', '成交量(万)', 'BBD(万)', '通吃率1日', '通吃率5日', '通吃率10日', '通吃率20日', '单数比', '特大差', '大单差', '中单差', '小单差', '主动率1日', '主动率5日', '主动率10日', '流通盘(万股)', '小单买入']

    abcddx_config = ['code', 'spj', 'zf', 'huanshou', 'liangbi', 'ddx', 'ddy', 'ddz', 'ddx3', 'ddx5', 'ddx10', 'ddx60', '5ddx', '10ddx', 'ddxlh', 'ddxlz', 'zf3', 'zf5', 'zf10', 'ddy3', 'ddy5',
                     'ddy10',
                     'ddy60', 'cjl', 'bbd', 'tcl1', 'tcl5', 'tcl10', 'tcl20', 'dsb', 'tdc', 'ddc', 'zdc', 'xdc', 'zdl1', 'zdl5', 'zdl10', 'wtp', 'unknow']
    data = []
    for i in tqdm(range(1,221)):
        url_sz = 'http://ddx.gubit.cn/xg/ddxlist.php?orderby=8&isdesc=1&page={}&t={}'.format(i, random.random())
        respSZ = requests.get(url_sz, headers=headers)
        try:
            data += respSZ.json()['data']
        except Exception as e:
            print(e)
            print('SZ...',respSZ.text)

        time.sleep(0.2)
    today = time.strftime("%Y-%m-%d", time.localtime())
    df = pd.DataFrame(data, columns=ddx_config)
    df['代码'] = df['代码'].apply(lambda x: str('{:0>6d}'.format(x)))
    # filt = df['代码'].str.contains('^(?!68|605|300|301|001296)')
    # df = df[filt]
    df = df.drop_duplicates()
    df['名称'] = df['代码'].apply(lambda x: industry[x] if x in industry else '新股')
    df['市值'] = df['代码'].apply(lambda x: nmc[x] if x in nmc else 0)
    df['date'] = today
    # df = df.sort_values(by=['DDX1日'], ascending=(False))
    df = df.to_json(orient='records',)
    # db.get_collection('test_stock')
    return df



def gbr():

    """
    DDX 市值 预测第二天价格
    :return:
    """
    seed = 3
    np.random.seed(seed)  # Numpy module.
    random.seed(seed)  # Python random module.
    sklearn.utils.check_random_state(seed)

    # 特征列
    # ddx_config = ['最新价','涨幅', 'DDX1日', 'DDX3日', 'DDX5日', 'DDX10日', '涨幅3日', '涨幅5日', '涨幅10日',
    # '通吃率1日', '通吃率5日', '通吃率10日', '通吃率20日', '特大差', '大单差', '主动率1日', '主动率5日', '主动率10日', ] #best mse 2.1373
    ddx_config = [
		'最新价',
		'涨幅',
		 'DDX1日',
		 'DDX3日',
		 'DDX5日',
		 'DDX10日',
		 '涨幅3日',
		 '涨幅5日',
		 '涨幅10日',
		 '通吃率1日',
		 '通吃率5日',
		 '通吃率10日',
		 '通吃率20日',
		 '特大差',
		 '大单差',
		 '主动率1日',
		 '主动率5日',
		 '主动率10日',

        # '市值',

]
    # ddx_config = ['代码', '最新价', '涨幅', '换手率', '量比', 'DDX1日', 'DDY1日', 'DDZ', 'DDX3日', 'DDX5日', 'DDX10日', 'DDX60日', 'DDX5红', 'DDX10红', 'DDX连红', 'DDX连增', '涨幅3日', '涨幅5日', '涨幅10日', 'DDY3日', 'DDY5日',
    #               'DDY10日', 'DDY60日', '成交量(万)', 'BBD(万)', '通吃率1日', '通吃率5日', '通吃率10日', '通吃率20日', '单数比', '特大差', '大单差', '中单差', '小单差', '主动率1日', '主动率5日', '主动率10日', '流通盘(万股)', '小单买入']
    res = pd.DataFrame(db.get_collection('DDX').find({'$and': [{'市值': {'$ne': 0}}, {'DDX10日': {'$ne': 0}},{'date':{'$ne':'2021-12-31'}},{'next_price':{'$ne':None}},]}))
    # print(res)
    # filt = res['代码'].str.contains('^(?!688|605|300|301|8|43)')
    # res = res[filt]
    data = res[ddx_config].values
    label = res[['next_price']].values

    params = {'n_estimators': 800, 'max_depth': 5, 'min_samples_split': 2, 'learning_rate': 0.01, 'loss': 'ls'}

    trainX, testX, trainY, testY = train_test_split(data, label, train_size=0.7, random_state=0)
    gbr = GradientBoostingRegressor(**params)
    gbr.fit(trainX, trainY.ravel())
    pred = gbr.predict(testX)
    mse = mean_squared_error(testY, pred)
    count = 0
    for idx,y in enumerate(testY):
        # if abs((y[0]-pred[idx])/y[0]) < 0.02:
        print('预测:{}，实际:{}，误差:{},比例:{}%'.format(round(pred[idx],2),y[0],round(y[0]-pred[idx],2),100*round((y[0]-pred[idx])/y[0],2)))
        count += abs(100*round((y[0]-pred[idx])/y[0],2))
    print("MSE: %.4f" % mse)
    print('平均误差：',count/len(pred))
    print('训练数据：',trainX.shape,'测试数据：',testX.shape)


    if mse <= 5:

        test_score = np.zeros((params['n_estimators'],), dtype=np.float64)
        for i, y_pred in enumerate(gbr.staged_predict(testX)):
            test_score[i] = gbr.loss_(testY, y_pred)

        plt.figure(figsize=(12,18))
        plt.subplot(2,1, 1)
        plt.title('Deviance:\n{}\nMSE:{}'.format(params, np.around(mse, 4)))
        plt.plot(np.arange(params['n_estimators']) + 1, gbr.train_score_, 'b-', label='Training Set Deviance')
        plt.plot(np.arange(params['n_estimators']) + 1, test_score, 'r-', label='Test Set Deviance')
        plt.legend(loc='upper right')
        plt.xlabel('Boosting Iterations')
        plt.ylabel('Deviance')

        feature_importance = gbr.feature_importances_
        feature_importance = 100.0 * (feature_importance / feature_importance.max())
        sorted_idx = np.argsort(feature_importance)
        feature_names = [ddx_config[i] for i in sorted_idx]
        pos = np.arange(sorted_idx.shape[0]) + .5
        plt.subplot(2,1, 2)
        plt.barh(pos, feature_importance[sorted_idx], align='center')
        plt.yticks(pos, feature_names)
        plt.xlabel('Relative Importance')
        plt.title('Variable Importance')
        # print(feature_names)
        # print(feature_importance[sorted_idx])
        plt.show()




def xgbr():

    """
    DDX 市值 预测第二天价格
    :return:
    """
    seed = 3
    np.random.seed(seed)  # Numpy module.
    random.seed(seed)  # Python random module.
    sklearn.utils.check_random_state(seed)

    # 特征列
    # ddx_config = ['最新价','涨幅', 'DDX1日', 'DDX3日', 'DDX5日', 'DDX10日', '涨幅3日', '涨幅5日', '涨幅10日',
    # '通吃率1日', '通吃率5日', '通吃率10日', '通吃率20日', '特大差', '大单差', '主动率1日', '主动率5日', '主动率10日', ] #best mse 2.1373  误差17.5
    ddx_config = [
		'最新价',
		'涨幅',
		 'DDX1日',
		 'DDX3日',
		 'DDX5日',
		 'DDX10日',
		 '涨幅3日',
		 '涨幅5日',
		 '涨幅10日',
		 '通吃率1日',
		 '通吃率5日',
		 '通吃率10日',
		 '通吃率20日',
		 '特大差',
		 '大单差',
		 '主动率1日',
		 '主动率5日',
		 '主动率10日',

        '市值',
        'open','high','low','ma5','ma10','ma20',
        # 'BBD(万)',

]

    today = time.strftime("%Y-%m-%d", time.localtime())
    res = pd.DataFrame(db.get_collection('DDX').find({'$and': [{'市值': {'$ne': 0}}, {'DDX10日': {'$ne': 0}},{'date':{'$ne':today}},{'open':{'$ne':None}},{'next_price':{'$ne':None}},]}))
    # print(res)
    # filt = res['代码'].str.contains('^(?!688|605|300|301|8|43)')
    # res = res[filt]

    res = res[(res['最新价']<20) & (res['最新价'] >5) & (res['市值'] <200) ]
    # res['BBD(万)'] = res['BBD(万)']/10000
    data = res[ddx_config].values
    label = res[['next_price']].values
    evals_result = {}
    params = {'n_estimators': 1500, 'max_depth': 4,  'learning_rate': 0.01,'objective':'reg:squarederror','min_child_weight':2,'evals_result':evals_result ,'silent':True}

    trainX, testX, trainY, testY = train_test_split(data, label, train_size=0.7, random_state=0)
    gbr = xgb.XGBRegressor(**params)
    evalset = [(trainX, trainY), (testX, testY)]

    gbr.fit(trainX, trainY.ravel(),eval_set=evalset)
    pred = gbr.predict(testX)
    mse = mean_squared_error(testY, pred)
    count= 0
    for idx,y in enumerate(testY):
        if abs((y[0]-pred[idx])/y[0]) > 0.03:
        # if y[0] < testX[idx][0]:
            print('最新价：{}，预测:{}，实际:{}，误差:{},比例:{}%'.format(testX[idx][0],round(pred[idx],2),y[0],round(y[0]-pred[idx],2),100*round((y[0]-pred[idx])/y[0],2)))
        count += abs(100*round((y[0]-pred[idx])/y[0],2))
    print("MSE: %.4f" % mse)
    print('平均误差：',count/len(pred))
    print('训练数据：', trainX.shape, '测试数据：', testX.shape)


    if mse < 50:

        train_score = gbr.evals_result()['validation_0']['rmse']
        test_score = gbr.evals_result()['validation_1']['rmse']
        plt.figure(figsize=(14, 20))
        plt.subplot(2, 1,1)
        plt.title('Deviance:\n{}\nMSE:{}'.format(params, np.around(mse, 4)))
        plt.plot(np.arange(params['n_estimators']) + 1, train_score, 'b-', label='Training Set Deviance')
        plt.plot(np.arange(params['n_estimators']) + 1, test_score, 'r-', label='Test Set Deviance')
        plt.legend(loc='upper right')
        plt.xlabel('Boosting Iterations')
        plt.ylabel('Deviance')

        feature_importance = gbr.feature_importances_
        sorted_idx = np.argsort(feature_importance)
        feature_names = [ddx_config[i] for i in sorted_idx]
        feature_importance = 100.0 * (feature_importance / feature_importance.max())
        sorted_idx = np.argsort(feature_importance)
        pos = np.arange(sorted_idx.shape[0]) + .5
        plt.subplot( 2,1, 2)
        plt.barh(pos, feature_importance[sorted_idx], align='center')
        plt.yticks(pos, feature_names)
        plt.xlabel('Relative Importance')
        plt.title('Variable Importance')
        plt.show()


if __name__ == '__main__':


    client = pymongo.MongoClient(host="192.168.0.28", port=27017)
    db = client['quant']
    now = time.strftime('%m-%d  %H:%M:%S')
    today = time.strftime("%Y-%m-%d", time.localtime())
    yesterday = (date.today() + timedelta(-1)).strftime('%Y-%m-%d')
    day2ago = (date.today() + timedelta(-2)).strftime('%Y-%m-%d')
    # app = QApplication(sys.argv)
    # win = MainWindow()
    # win.show()
    # # win.showMaximized(ter
    # app.exec_()

    # 二进三 复盘查找两连板 昨天，前天 涨幅>9.8 ,进入打板池
    #  T字板 ：open == high == close >9.8  >low
    # 打板池轮询开板，通知
    # 参考   岳阳林纸， 山东墨龙 三星医疗，汇洁股份，圣济堂，锦鸿集团，小康股份，宜宾纸业


    # 补0占位
    # print('{:0>2d}'.format(3))


    # df = ts.get_sina_dd('600023',date='2021-10-28')
    # print(df)
    # a = 'http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill_all.php?num=100&page=1&sort=ticktime&asc=0&volume=40000&type=0&symbol=sh600023'


    # ts.get_sina_dd(code='000755',date='2021-12-02')
    # url = 'https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillList?symbol=sz000755&num=60&page=1&sort=ticktime&asc=0&volume=50000&amount=0&type=0&day=2021-12-02'
    # resp = requests.get(url,headers=headers)
    # print(resp.json())

    # db.get_collection('stk_pool').insert({'code':'605318','day':5})
    # db.get_collection('stk_pool').insert({'code':'002495','day':5})


    # 逻辑回归选股测试
    # 1.获取ddx数据
    # ddx = getDDXData()
    # ddx = json.loads(ddx)
    # for i in ddx:
    #     print(i)
    #     db.get_collection('DDX').insert(i)


    # 2.GBDT+LR选股策略

    # gbr()
    # xgbr()

    # df = pd.read_html('https://www.xilimao.com/qiangshigu/')
    # df = pd.DataFrame(df[0])
    # df['代码'] = df['代码'].apply(lambda x: str('{:0>6d}'.format(x)))
    # del df['#']
    # # ['代码', '名称', '短线主题', '涨幅%', '现价', '封单', '今开%', '总金额', '换手率', '流通市值','总市值', '振幅', '地区', '行业', '首次封板', '连板', '几天几板', '强势原因']
    # print(df)

    res = db.get_collection('DDX').distinct('代码',{'名称':'新股'})
    for i in res:

        kk = db.get_collection('base').find_one({'code':i})
        print(kk)
        db.get_collection('DDX').update_many({'代码':i},{'$set':{'名称':kk['name']}})


    # 5日线选股
    # day = db.get_collection('dayK').distinct('date',)[-3:]
    #
    # day1 = pd.DataFrame(db.get_collection('dayK').find({'$and':[{'date':day[0]},{'$where':'this.close > this.ma5'}]}))
    # day2 = pd.DataFrame(db.get_collection('dayK').find({'$and':[{'date':day[1]},{'$where':'this.close > this.ma5'}]}))
    # day3 = pd.DataFrame(db.get_collection('dayK').find({'$and':[{'date':day[2]},{'$where':'this.close > this.ma5'}]}))
    #
    # stock = pd.merge(day1,day2,on=['code'])
    # stock = pd.merge(stock,day3,on=['code'])
    # print(stock.code)



    # res = db.get_collection('DDX').distinct('代码',{'open':None,})
    # for i in tqdm(res):
    #
    #     df = ts.get_hist_data(i)
    #     try:
    #
    #         d31 = df.iloc[0]
    #         print(i,d31.open,d31.high,d31.low,d31.close)
    #         db.get_collection('DDX').update({'代码':i,'date':'2022-01-10'},{'$set':{'open':d31.open,'high':d31.high,'close':d31.close,'low':d31.low,'ma5':d31.ma5,'ma10':d31.ma10,'ma20':d31.ma20}})
    #         d30 = df.iloc[1]
    #         db.get_collection('DDX').update({'代码':i,'date':'2022-01-07'},{'$set':{'open':d30.open,'high':d30.high,'close':d30.close,'low':d30.low,'ma5':d30.ma5,'ma10':d30.ma10,'ma20':d30.ma20}})
    #         d29 = df.iloc[2]
    #         db.get_collection('DDX').update({'代码':i,'date':'2022-01-06'},{'$set':{'open':d29.open,'high':d29.high,'close':d29.close,'low':d29.low,'ma5':d29.ma5,'ma10':d29.ma10,'ma20':d29.ma20}})
    #         d28 = df.iloc[3]
    #         db.get_collection('DDX').update({'代码': i, 'date': '2022-01-05'},{'$set': {'open': d28.open, 'high': d28.high, 'close': d28.close, 'low': d28.low, 'ma5': d28.ma5, 'ma10': d28.ma10, 'ma20': d28.ma20}})
    #         d27 = df.iloc[4]
    #         db.get_collection('DDX').update({'代码': i, 'date': '2022-01-04'},{'$set': {'open': d27.open, 'high': d27.high, 'close': d27.close, 'low': d27.low, 'ma5': d27.ma5, 'ma10': d27.ma10, 'ma20': d27.ma20}})
    #         d26 = df.iloc[5]
    #         db.get_collection('DDX').update({'代码': i, 'date': '2021-12-31'},{'$set': {'open': d26.open, 'high': d26.high, 'close': d26.close, 'low': d26.low, 'ma5': d26.ma5, 'ma10': d26.ma10, 'ma20': d26.ma20}})
    #         time.sleep(0.5)
    #     except:
    #         pass

    # db.get_collection('DDX').update_many({'next_change':{'$gt':0},},{'$set':{'label':1}})
    # db.get_collection('DDX').update_many({'next_change':{'$lte':0}},{'$set':{'label':0}})

    # 均线多头排列 min30金叉 选股
    # res = db['today'].find({'$where': 'this.trade >= this.ma5 & this.ma5 >= this.ma10 & this.ma10 >= this.ma20'})
    # for i in res:
    #     # print(i)
    #     min30 = ts.get_k_data(i['code'], ktype='30')
    #     min30 = MA(min30, 5)
    #     min30 = MA(min30, 20)
    #     min30 = MA(min30, 60)
    #     new = min30.tail(1)
    #     # print(new)
    #     if float(new.ma5) >= float(new.ma20) >= float(new.ma60) and min30.iloc[-1].ma5 > min30.iloc[-2].ma5:
    #         print(i)
    #     time.sleep(0.1)

    # res = db.get_collection('DDX').find()
    # for i in res:
    #     kk = db.get_collection('dayK').find_one({'code':i['代码'],'date':i['date']})
    #     if kk:
    #         # db.get_collection('DDX').update()
    #         kk.pop('_id')
    #         kk.pop('date')
    #         kk.pop('code')
    #
    #         print(i['代码'],i['date'],kk)
    #         db.get_collection('DDX').update({'代码':i['代码'],'date':i['date']},{'$set':{'open':kk['open'],'high':kk['high'],'close':kk['close'],'low':kk['low'],'ma5':kk['ma5'],'ma10':kk['ma10'],'ma20':kk['ma20']}})