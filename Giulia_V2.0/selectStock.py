# -*- coding: utf-8 -*-#
import json
import locale
import os
import random
from threading import Thread
from datetime import datetime,date,timedelta
import time
import pymongo
import tushare as ts
import pandas as pd
from tqdm import tqdm
from PyQt5.QtWidgets import QMainWindow
import os
from Ui_Giulia import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

client = pymongo.MongoClient(host="192.168.0.28", port=27017)
db = client['quant']

locale.setlocale(locale.LC_CTYPE, 'chinese')


def async_(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper


class Select():

    def __init__(self,init=True):
        """
        初始化，筛除688,300，ST，退市股，新股，低价股，下跌股
        """
        if init:
            self.data = ts.get_today_all() #今日复盘
            # data = ts.get_day_all(date='2021-02-18')   #历史复盘
            filt = self.data['code'].str.contains('^(?!688|605|300)')
            self.data = self.data[filt]
            filt = self.data['name'].str.contains('^(?!S|退市|\*ST)')
            self.data = self.data[filt]
            self.data = self.data.drop_duplicates()
            data = self.data[self.data['trade']>=2]
            data = data[data['changepercent']>0]
            data = data.to_json(orient='records')
            db.get_collection('today').remove()
            base = db.get_collection('base').find()
            industry = {i['code']: i['industry'] for i in base}
            self.intersect = {}
            for i in eval(data):
                db.get_collection('today').insert(i)
            res = db.get_collection('today').find()
            for i in res:
                try:
                    db.get_collection('today').update_many({'code':i['code']},{'$set':{'industry':industry[i['code']]}})
                except :
                    pass

            # 剔除新股
            try:
                newStock = ts.new_stocks()
                if not newStock.empty:
                    for i in newStock['code'].tolist():
                        db.get_collection('today').remove({'code':i},multi=True)
            except Exception as e:
                print('newStock Error',e)

            # 剔除停牌
            db.get_collection('today').remove({'open': 0})


    def uniqDayK(self):
        """
        dayK数据去重
        :return:
        """
        kk = db.get_collection('dayK').aggregate([{'$group': {'_id': {'date': "$date", 'code': "$code"}}}])
        for i in tqdm(kk):
            count = db.get_collection('dayK').count(i['_id'])
            if count > 1:
                print(count, i['_id'])
                db.get_collection('dayK').delete_one(i['_id'])


    def updBase(self):
        db.get_collection('base').remove()
        pro = ts.pro_api()
        data = pro.stock_basic()
        data.rename(columns={'symbol': 'code'}, inplace=True)
        for idx, i in data.iterrows():
            print(dict(i))
            db.get_collection('base').insert(dict(i))


    def download(self,):
        """
        增量获取数据
        :return:
        """
        res = db.get_collection('today').distinct('code')
        for i in tqdm(res):
            # 查询库中是否有历史数据
            kk = db.get_collection('dayK').find({'code':i})
            kk = list(kk)

            if kk:
                # 有，获取最大日期+1，获取数据
                df = pd.DataFrame(kk)
                lastday = df['date'].max()
                nextday = (datetime.strptime(lastday, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
                today = time.strftime("%Y-%m-%d", time.localtime())
                if nextday <= today:
                    time.sleep(0.1)
                    # 每日18:10后更新当日数据
                    data = ts.get_hist_data(i,start=nextday)
                    if not data.empty:
                        data['pressure'] = data.apply(lambda x: max(x['open'], x['close']), axis=1)
                        data = json.loads(data.to_json(orient='index'))
                        for k, v in data.items():
                            # print(k, v)
                            v['date'] = k
                            v['code'] = i
                            db.get_collection('dayK').insert(v)

            else:
                # 无，全量获取数据
                # 次新数据少于300天，删除自选 len(index)<300
                #     time.sleep(0.5)
                    data = ts.get_hist_data(i)
                    # 开盘价和收盘价对比取压力值pressure
                    data['pressure'] = data.apply(lambda x:max(x['open'],x['close']),axis=1)
                    data = json.loads(data.to_json(orient='index'))
                    for k,v in data.items():
                        # print(k,v)
                        v['date'] = k
                        v['code'] = i
                        db.get_collection('dayK').insert(v)


    def topN(self,Coll='today'):
        """
        N日内最高价
        :param N:
        :return:
        """
        print('N日新高......')
        today = time.strftime("%Y-%m-%d", time.localtime())
        yesterday = (date.today() + timedelta(-1)).strftime('%Y%m%d')
        pro = ts.pro_api()
        lastTrade = pro.trade_cal(exchange='', start_date='20210601', end_date=yesterday)
        lastTrade = lastTrade[lastTrade['is_open']==1]
        lastTrade = lastTrade['cal_date'].iloc[-1]
        lastTrade = lastTrade[:4] +'-'+ lastTrade[4:6] +'-'+ lastTrade[6:]
        topday = [3, 5, 13, 21, 34, 55, 89, 144, 233]
        if time.localtime().tm_hour >= 15:
            res = db.get_collection('dayK').find({'date': today})
        else:
            res = db.get_collection('dayK').find({'date': lastTrade})
        self.intersect = {i.pop('code'): i for i in res}
        res = db.get_collection(Coll).find()
        for i in tqdm(res):
            self.topN_child(today=today,i=i,topday=topday,Coll=Coll)
        # db.get_collection(Coll).remove({'top3': None})


    @async_
    def topN_child(self,today=None,i=None,topday=None,Coll=None):
        kk = db.get_collection('dayK').find({'$and': [{"date": {'$ne': today}}, {"code": i['code']}]}).sort('date', -1)
        df = pd.DataFrame(list(kk))
        count = 0
        topItem = {}
        for d in topday:
            try:
                topN = df[:d + 1]['pressure'].max()
                if i['trade'] >= topN:
                    price = str(topN)
                    count += 1
                else:
                    price = topN
                topItem['top' + str(d)] = price
            except :
                pass
        topItem['count'] = count
        try:
            # topItem['ma5'] = round(self.intersect[i['code']]['ma5'] / self.intersect[i['code']]['ma10']-1,3)
            topItem['ma5'] = str(self.intersect[i['code']]['ma5']) if self.intersect[i['code']]['ma5'] > self.intersect[i['code']]['ma10'] else self.intersect[i['code']]['ma5']
            # topItem['ma10'] = round(self.intersect[i['code']]['ma10'] / self.intersect[i['code']]['ma20']-1,3)
            topItem['ma10'] = str(self.intersect[i['code']]['ma10']) if self.intersect[i['code']]['ma10'] > self.intersect[i['code']]['ma20'] else self.intersect[i['code']]['ma10']
        except Exception as e:
            print('MA5 error',Coll,e)

        db.get_collection(Coll).update({'code': i['code']}, {'$set': topItem})


    def vol(self):
        now_time = datetime.now()
        # open_time = datetime.strptime(str(datetime.now().date()) + '9:30', '%Y-%m-%d%H:%M')
        close_time = datetime.strptime(str(datetime.now().date()) + '15:00', '%Y-%m-%d%H:%M')
        print('成交量比......')
        # today = time.strftime("%Y-%m-%d", time.localtime())
        res = db.get_collection('today').find()
        for i in tqdm(res):
            self.vol_child(now_time=now_time,close_time=close_time,i=i)

    @async_
    def vol_child(self,now_time=None,close_time=None,i=None):
        kk = db.get_collection('dayK').find({"code": i['code']}).sort('date', -1)
        df = pd.DataFrame(list(kk))
        try:
            # df = df.sort_values(by='date', ascending=False)
            if now_time < close_time:
                # 当天盘中
                volRatio = round(i['volume'] / df['volume'][0] / 100, 2)
            else:
                # 盘后,!!!!!!需先下载当日数据
                volRatio = round(df['volume'][0] / df['volume'][1], 2)
            db.get_collection('today').update({'code': i['code']}, {'$set': {'volRatio': volRatio}})
        except Exception as e:
            print(i, e)


    def impactPool(self,debug=False):
        if not debug:
            time.sleep(60)   # 等topN执行完毕
        calendar = ['today', 'yesterday', 'day3ago', 'day4ago', 'day5ago', 'day6ago', 'day7ago', ]
        today = time.strftime("%Y-%m-%d", time.localtime())
        limitUp = db.get_collection('today').find({'changepercent': {'$gte': 9}}).sort('changepercent', -1)
        limitUp = list(limitUp)
        db.get_collection('impact2to3').remove()
        db.get_collection('impact1to2').remove()
        for i in limitUp:
            # 当日盘后
            res = db.get_collection('dayK').find({'code': i['code']}).sort('date', -1)
            markUp = [j['p_change'] for j in res[:7]]
            item = {'code': i['code'], 'name': i['name'],'count':i['count'],'date': today,'price':i['trade'],'contBoard':''}
            item.update(dict(zip(calendar, markUp)))
            # 二进三
            if markUp[0] > 9 and markUp[1] > 9:
                db.get_collection('impact2to3').insert(item)
            # 一进二
            elif markUp[0] > 9 and markUp[1] < 9:
                db.get_collection('impact1to2').insert(item)

    @async_
    def riseN(self,N=10,p_change=0,coll='riseN'):
        """
        N日内主升浪,默认10日,每日盘后更新，复盘用
        :param N:  N日内
        :param p_change: 强势/小阳线
        :param coll:
        riseN : 小连阳,p > 0
        strong : 强势票, p > 9
        :return:
        """
        if type(N) != int or N < 3:
            print('日期错误,N大于3...')
            return
        print(N,'日主升浪...')
        today = time.strftime("%Y-%m-%d", time.localtime())
        db.get_collection(coll).remove()
        ago10 = (date.today() + timedelta(-N)).strftime('%Y-%m-%d')
        baseMap = db.get_collection('base').find()
        baseMap = {j['code']: j['name'] for j in baseMap}
        rise = db.get_collection("dayK").aggregate([{'$match': {'p_change': {'$gte': p_change}, 'date': {'$gte': ago10}}}, {'$group': {'_id': '$code', 'riseNum': {'$sum': 1}}}, {'$sort': {'riseNum': -1}}])
        for i in rise:
            if i['riseNum'] > 2 :
                trade = self.data[self.data['code'] == i['_id']]
                trade = trade['open'].iloc[0]
                db.get_collection(coll).insert({'date':today,'code': i['_id'], 'name': baseMap[i['_id']], 'riseNum': i['riseNum'],'trade':trade})
        self.topN(Coll=coll)


# @async_
def downStock():
    # 每日15:30后
    print('开始下载数据....', time.strftime('%Y年%m月%d日%H时%M分%S秒'))
    s = Select(init=True)
    s.download()
    s.topN()
    s.vol()
    # s.uniqDayK()
    print('数据下载完毕....', time.strftime('%Y年%m月%d日%H时%M分%S秒'))
    # 收盘前不可用
    now_time = datetime.now()
    close_time =datetime.strptime(str(datetime.now().date())+'15:30', '%Y-%m-%d%H:%M')
    if now_time > close_time:
        s.riseN()
        s.riseN(p_change=9,coll='strong')  # N日内强势票
        s.impactPool()


@async_
def refresh():

    print('开始刷新....', time.strftime('%Y年%m月%d日%H时%M分%S秒'))
    s = Select(init=True)
    s.topN()
    s.vol()
    print('刷新完毕....',time.strftime('%Y年%m月%d日%H时%M分%S秒'))
    # 收盘前不可用
    # now_time = datetime.now()
    # close_time = datetime.strptime(str(datetime.now().date()) + '15:30', '%Y-%m-%d%H:%M')
    # if now_time > close_time:
    #     s.impactPool()



if __name__ == '__main__':

    """
    db.getCollection("dayK").aggregate([{$match:{'p_change':{$gte:9},'date':{$gte:'2021-05-01'}}},{$group:{_id:'$code',count:{$sum:1}}},{$sort:{count:-1}}])
    统计某段时间涨停票个数
    """

    downStock()
    # refresh()

#################################################################


    # print('Debug....')
    # s = Select(init=False)
    # s.topN()
    # s.riseN()
    # s.impactPool(debug=True)
    # s.riseN()