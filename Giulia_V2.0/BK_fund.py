# -*- coding: utf-8 -*-#
import json
import os
import re
import pymongo
import requests
import time
from CONSTANT import MONGOHOST
from datetime import datetime, date, timedelta
from tqdm import tqdm,trange
import pandas as pd
pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

headers = {
    # 'Referer': 'http://data.eastmoney.com/bkzj/hy.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
}

client = pymongo.MongoClient(host=MONGOHOST, port=27017)
db = client['quant']



mappingEN = {
    "f2": "zxj",
    "f3": "zdf",
    "f127": "zdf",
    "f109": "zdf",
    "f160": "zdf",
    "f12": "code",
    "f14": "name",
    "f62": "zlje",
    "f184": "zljzb",
    "f66": "cddje",
    "f69": "cddjzb",
    "f72": "ddje",
    "f75": "ddjzb",
    "f78": "zdje",
    "f81": "zdjzb",
    "f84": "xdje",
    "f87": "xdjzb",
    "f267": "zlje",
    "f268": "zljzb",
    "f269": "cddje",
    "f270": "cddjzb",
    "f271": "ddje",
    "f272": "ddjzb",
    "f273": "zdje",
    "f274": "zdjzb",
    "f275": "xdje",
    "f276": "xdjzb",
    "f164": "zlje",
    "f165": "zljzb",
    "f166": "cddje",
    "f167": "cddjzb",
    "f168": "ddje",
    "f169": "ddjzb",
    "f170": "zdje",
    "f171": "zdjzb",
    "f172": "xdje",
    "f173": "xdjzb",
    "f174": "zlje",
    "f175": "zljzb",
    "f176": "cddje",
    "f177": "cddjzb",
    "f178": "ddje",
    "f179": "ddjzb",
    "f180": "zdje",
    "f181": "zdjzb",
    "f182": "xdje",
    "f183": "xdjzb",
    "f205": "zdcode",
    "f204": "zdname",
    "f258": "zdcode",
    "f257": "zdname",
    "f261": "zdcode",
    "f260": "zdname",
    "f225": "zlpm1",
    "f263": "zlpm5",
    "f264": "zlpm10"
}

mappingCN = {
    "f2": "最新价",
    "f3": "涨跌幅",
    "f127": "zdf",
    "f109": "zdf",
    "f160": "zdf",
    "f12": "code",
    "f14": "name",
    "f62": "主力净额",
    "f184": "主力净占比",
    "f64":"超大单流入",
    "f65":"超大单流出",
    "f66": "超大单净额",
    "f69": "超大单净占比",
    "f70": "大单流入",
    "f71": "大单流出",
    "f72": "大单净额",
    "f75": "大单净占比",
    "f76": "中单流入",
    "f77": "中单流出",
    "f78": "中单净额",
    "f81": "中单净占比",
    "f82": "小单流入",
    "f83": "小单流出",
    "f84": "小单净额",
    "f87": "小单净占比",
    "f267": "zlje",
    "f268": "zljzb",
    "f269": "cddje",
    "f270": "cddjzb",
    "f271": "ddje",
    "f272": "ddjzb",
    "f273": "zdje",
    "f274": "zdjzb",
    "f275": "xdje",
    "f276": "xdjzb",
    "f164": "zlje",
    "f165": "zljzb",
    "f166": "cddje",
    "f167": "cddjzb",
    "f168": "ddje",
    "f169": "ddjzb",
    "f170": "zdje",
    "f171": "zdjzb",
    "f172": "xdje",
    "f173": "xdjzb",
    "f174": "zlje",
    "f175": "zljzb",
    "f176": "cddje",
    "f177": "cddjzb",
    "f178": "ddje",
    "f179": "ddjzb",
    "f180": "zdje",
    "f181": "zdjzb",
    "f182": "xdje",
    "f183": "xdjzb",
    "f205": "领涨股代码",
    "f204": "领涨股",
    "f258": "zdcode",
    "f257": "zdname",
    "f261": "zdcode",
    "f260": "zdname",
    "f225": "zlpm1",
    "f263": "zlpm5",
    "f264": "zlpm10",
    "f124": "time",
}


def fundBK():
    """获取板块资金流向，个股资金流向"""
    today = time.strftime("%Y-%m-%d", time.localtime())
    close_time = datetime.strptime(str(datetime.now().date()) + '15:00', '%Y-%m-%d%H:%M')
    now_time = datetime.now()
    if now_time > close_time:

        # 板块资金流向
        BKurl = 'http://push2.eastmoney.com/api/qt/clist/get?fid=f62&po=1&pz=80&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A90+t%3A2&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13'
        resp = requests.get(BKurl, headers=headers)
        data = json.loads(resp.text)['data']
        num = data['total']
        print('板块数：', num)
        for i in data['diff']:
            item = {'BK': i['f12'], 'industry': i['f14'], 'index': i['f2'], 'change': i['f3'], '主力净额': i['f62'], '主力净占比': i['f184'], '超大单净额': i['f66'], '超大单净占比': i['f69'],
                    '大单净额': i['f72'], '大单净占比': i['f75'], '中单净额': i['f78'], '中单净占比': i['f81'], '小单净额': i['f84'], '小单净占比': i['f87'], 'date': today}
            if not db.get_collection('BK_fund').find_one(item):
                db.get_collection('BK_fund').insert(item)
                print(item)

        # 行业板块股票资金流向
        res = db.get_collection('BK_fund').aggregate([{'$group': {'_id': {'BK': '$BK', 'industry': '$industry'}}}])
        res = list(res)
        for j in tqdm(res):
            time.sleep(1)
            url = 'http://push2.eastmoney.com/api/qt/clist/get?fid=f62&po=1&pz=100&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=b%3A{}&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13'.format(
                j['_id']['BK'])
            resp = requests.get(url, headers=headers)
            data = json.loads(resp.text)['data']
            if data:
                num = data['total']
                print(num, j)
                for i in data['diff']:
                    item = {'BK': j['_id']['BK'], 'industry': j['_id']['industry'], 'code': i['f12'], 'name': i['f14'], 'price': i['f2'], 'change': i['f3'], '主力净额': i['f62'], '主力净占比': i['f184'],
                            '超大单净额': i['f66'], '超大单净占比': i['f69'],
                            '大单净额': i['f72'], '大单净占比': i['f75'], '中单净额': i['f78'], '中单净占比': i['f81'], '小单净额': i['f84'], '小单净占比': i['f87'], 'date': today}
                    if not db.get_collection('BK_stock').find_one(item) and i['f2'] != '-':
                        db.get_collection('BK_stock').insert(item)
                        # print(item)


def fundHS():
    """沪深个股资金流向"""

    # today = time.strftime("%Y-%m-%d", time.localtime())
    # close_time = datetime.strptime(str(datetime.now().date()) + '15:00', '%Y-%m-%d%H:%M')
    # now_time = datetime.now()

    data = []
    for page in tqdm(range(1,4)):


        # 主力净额排序前300
        url = 'http://push2.eastmoney.com/api/qt/clist/get?' \
              'fid=f62&po=1&pz=100&pn={}&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5' \
              '&fs=m%3A0%2Bt%3A6%2Bf%3A!2%2Cm%3A0%2Bt%3A13%2Bf%3A!2%2Cm%3A0%2Bt%3A80%2Bf%3A!2%2Cm%3A1%2Bt%3A2%2Bf%3A!2%2Cm%3A1%2Bt%3A23%2Bf%3A!2%2Cm%3A0%2Bt%3A7%2Bf%3A!2%2Cm%3A1%2Bt%3A3%2Bf%3A!2' \
              '&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13'.format(page)
        resp = requests.get(url,headers=headers)
        js = resp.json()
        for i in js['data']['diff']:
            # print(i)
            data.append(i)
        time.sleep(1)


        # 主力净占比排序前300
        url2 = 'http://push2.eastmoney.com/api/qt/clist/get?' \
               'fid=f184&po=1&pz=100&pn={}&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5' \
               '&fs=m%3A0%2Bt%3A6%2Bf%3A!2%2Cm%3A0%2Bt%3A13%2Bf%3A!2%2Cm%3A0%2Bt%3A80%2Bf%3A!2%2Cm%3A1%2Bt%3A2%2Bf%3A!2%2Cm%3A1%2Bt%3A23%2Bf%3A!2%2Cm%3A0%2Bt%3A7%2Bf%3A!2%2Cm%3A1%2Bt%3A3%2Bf%3A!2' \
               '&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13'.format(page)
        resp2 = requests.get(url2, headers=headers)
        js2 = resp2.json()
        for i in js2['data']['diff']:
            # print(i)
            data.append(i)
        time.sleep(1)


    data = pd.DataFrame(data)
    data = data.drop_duplicates(subset=['f12'])
    filt = data['f12'].str.contains('^(?!68|605|300|301|20|900|603048|600935|001|603216|603071|002629)')
    data = data[filt]
    filt = data['f14'].str.contains('^(?!S|退市|\*ST|N)')
    data = data[filt]
    data['f62'] = round(data['f62'] / 10000,2)
    data['f66'] = round(data['f66'] / 10000,2)
    data['f72'] = round(data['f72'] / 10000,2)
    data['f78'] = round(data['f78'] / 10000,2)
    data['f84'] = round(data['f84'] / 10000,2)
    data['date'] = pd.to_datetime(data['f124'].values, utc=True, unit='s',).tz_convert("Asia/Shanghai").to_period("D")
    data = data.reset_index(drop=True)
    # print(data)
    return data


def breakThrough():

    """东财平台突破数据"""
    print('GET平台突破数据.....')
    url = 'https://emdczttz.eastmoney.com/Stock/PlatformBreakthrough'
    data = []
    for page in trange(1,11):
        form = {"OrderType":0,"OrderField":"Zdf","pageSize":100,"startIndex":page}
        resp = requests.post(url,headers=headers,data=str(form))
        data += resp.json()['Data'][0]['Data']

        # print(new)
        time.sleep(1)
    df = pd.DataFrame(data, columns=['dd'])
    new = df['dd'].str.split('|', 4, expand=True)
    new.columns = ['code', 'name', 'market', 'new', 'zdf']
    filt = new['code'].str.contains('^(?!688|605|300)')
    new = new[filt]
    filt = new['name'].str.contains('^(?!S|退市|\*ST)')
    new = new[filt]
    new = new.drop_duplicates(subset=['code'])
    new['new'] = new['new'].astype(float)
    new['zdf'] = new['zdf'].astype(float)
    # print(new)
    return new


def priceDistribution(code,start,end):

    if code.startswith('6'):
        code = 'sh' + code
    else:
        code = 'sz' + code

    url = 'https://market.finance.sina.com.cn/iframe/pricehis.php?symbol={}&startdate={}&enddate={}'.format(code,start,end)
    print(url)
    data = pd.read_html(url)
    data = pd.DataFrame(data[0])
    data = data.rename(columns={"成交价(元)": 'price',"成交量(股)":'vol', "占比": 'ratio',"占比图":'amount'})
    data['amount'] = data['price'] * data['vol']
    data = data.sort_values(by='vol',ascending=False)
    data = data.reset_index(drop=True)
    print(data.head(10))
    N = int(input('前N项：'))
    # print(data[:N])
    print('前N日均价:{:.2f},总量(股):{},总额:{},占比:{:.2f}'.format(data['amount'][:N].sum()/data['vol'][:N].sum(),data['vol'][:N].sum(),data['amount'][:N].sum(),data['vol'][:N].sum()/data['vol'].sum()))
    print('总均价:{:.2f}'.format(data['amount'].sum()/data['vol'].sum()))


if __name__ == '__main__':


    # fundBK()
    # fundHS()
    # breakThrough()
    priceDistribution('603569','2021-12-13','2021-12-23')