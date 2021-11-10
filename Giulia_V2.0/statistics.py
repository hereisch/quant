# -*- coding: utf-8 -*-#
import os
import sys
import time
from datetime import datetime
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
from colorama import init, Fore, Back, Style
init(autoreset=False)



class Colored(object):
    #  前景色:红色  背景色:默认
    def red(self, s):
        return Fore.LIGHTRED_EX + s + Fore.RESET
    #  前景色:绿色  背景色:默认
    def green(self, s):
        return Fore.LIGHTGREEN_EX + s + Fore.RESET
    def yellow(self, s):
        return Fore.LIGHTYELLOW_EX + s + Fore.RESET
    def white(self,s):
        return Fore.LIGHTWHITE_EX + s + Fore.RESET
    def blue(self,s):
        return Fore.LIGHTBLUE_EX + s + Fore.RESET
    def magenta(self,s):
        return Fore.LIGHTMAGENTA_EX + s + Fore.RESET
    def cyan(self,s):
        return Fore.LIGHTCYAN_EX + s + Fore.RESET



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
    color = Colored()
    code = '1.' + code if code.startswith('6') else '0.' + code
    close_time = datetime.strptime(str(datetime.now().date()) + '15:00', '%Y-%m-%d%H:%M')
    now_time = datetime.now()
    while True:

        os.system("cls")  # 清屏需在终端中运行
        market = ts.get_realtime_quotes('sh000001')
        deal_detail = ts.get_realtime_quotes(code[2:])
        sh = market['price'][0]
        sh_percent = round((float(sh)-float(market['pre_close'][0]))/float(market['pre_close'][0])*100,2)
        url = 'http://push2.eastmoney.com/api/qt/stock/get?ut=b2884a393a59ad64002292a3e90d46a5&secid={}&fields=f469,f137,f193,f140,f194,f143,f195,f146,f196,f149,f197,f470,f434,f454,f435,f455,f436,f456,f437,f457,f438,f458,f471,f459,f460,f461,f462,f463,f464,f465,f466,f467,f468,f170,f119,f291'.format(code)
        resp = requests.get(url,headers=headers)
        data = resp.json()['data']
        # print('涨幅：{}%'.format(data['f170']/100))
        # print('主力净流入：{}万，主力净占比：{}万'.format(data['f137']/10000,data['f193']/100))
        # print('超大净流入：{}万，超大净占比：{}万'.format(data['f140']/10000,data['f194']/100))
        # print('大单净流入：{}万，大单净占比：{}万'.format(data['f143']/10000,data['f195']/100))
        # print('中单净流入：{}万，中单净占比：{}万'.format(data['f146']/10000,data['f196']/100))
        # print('小单净流入：{}万，小单净占比：{}万'.format(data['f149']/10000,data['f197']/100))
        
        change = color.red(str(data['f170']/100)+'%') if data['f170'] > 0 else color.green(str(data['f170']/100)+'%')
        change5 = color.red(str(data['f119']/100)+'%') if data['f119'] > 0 else color.green(str(data['f119']/100)+'%')
        change10 = color.red(str(data['f291']/100)+'%') if data['f291'] > 0 else color.green(str(data['f291']/100)+'%')
        
        
        ZLZJ = color.red(str(data['f137']/10000)) if data['f137'] >0 else color.green(str(data['f137']/10000))
        ZLZB = color.red(str(data['f193']/100)) if data['f193'] >0 else color.green(str(data['f193']/100))
        ZLZJ5 = color.red(str(data['f434']/10000)) if data['f434'] >0 else color.green(str(data['f434']/10000))
        ZLZB5 = color.red(str(data['f454']/100)) if data['f454'] >0 else color.green(str(data['f454']/100))
        ZLZJ10 = color.red(str(data['f459']/10000)) if data['f459'] >0 else color.green(str(data['f459']/10000))
        ZLZB10 = color.red(str(data['f460']/100)) if data['f460'] >0 else color.green(str(data['f460']/100))

        CDZJ = color.red(str(data['f140']/10000)) if data['f140'] >0 else color.green(str(data['f140']/10000))
        CDZB = color.red(str(data['f194']/100)) if data['f194'] >0 else color.green(str(data['f194']/100))
        CDZJ5 = color.red(str(data['f435']/10000)) if data['f435'] >0 else color.green(str(data['f435']/10000))
        CDZB5 = color.red(str(data['f455']/100)) if data['f455'] >0 else color.green(str(data['f455']/100))
        CDZJ10 = color.red(str(data['f461']/10000)) if data['f461'] >0 else color.green(str(data['f461']/10000))
        CDZB10 = color.red(str(data['f462']/100)) if data['f462'] >0 else color.green(str(data['f462']/100))

        DDZJ = color.red(str(data['f143']/10000)) if data['f143'] >0 else color.green(str(data['f143']/10000))
        DDZB = color.red(str(data['f195']/100)) if data['f195'] >0 else color.green(str(data['f195']/100))
        DDZJ5 = color.red(str(data['f436']/10000)) if data['f436'] >0 else color.green(str(data['f436']/10000))
        DDZB5 = color.red(str(data['f456']/100)) if data['f456'] >0 else color.green(str(data['f456']/100))
        DDZJ10 = color.red(str(data['f463']/10000)) if data['f463'] >0 else color.green(str(data['f463']/10000))
        DDZB10 = color.red(str(data['f464']/100)) if data['f464'] >0 else color.green(str(data['f464']/100))

        ZDZJ = color.red(str(data['f146']/10000)) if data['f146'] >0 else color.green(str(data['f146']/10000))
        ZDZB = color.red(str(data['f196']/100)) if data['f196'] >0 else color.green(str(data['f196']/100))
        ZDZJ5 = color.red(str(data['f437']/10000)) if data['f437'] >0 else color.green(str(data['f437']/10000))
        ZDZB5 = color.red(str(data['f457']/100)) if data['f457'] >0 else color.green(str(data['f457']/100))
        ZDZJ10 = color.red(str(data['f465']/10000)) if data['f465'] >0 else color.green(str(data['f465']/10000))
        ZDZB10 = color.red(str(data['f466']/100)) if data['f466'] >0 else color.green(str(data['f466']/100))

        XDZJ = color.red(str(data['f149']/10000)) if data['f149'] >0 else color.green(str(data['f149']/10000))
        XDZB = color.red(str(data['f197']/100)) if data['f197'] >0 else color.green(str(data['f197']/100))
        XDZJ5 = color.red(str(data['f438']/10000)) if data['f438'] >0 else color.green(str(data['f438']/10000))
        XDZB5 = color.red(str(data['f458']/100)) if data['f458'] >0 else color.green(str(data['f458']/100))
        XDZJ10 = color.red(str(data['f467']/10000)) if data['f467'] >0 else color.green(str(data['f467']/10000))
        XDZB10 = color.red(str(data['f468']/100)) if data['f468'] >0 else color.green(str(data['f468']/100))
        
        
        # tb = pt.PrettyTable()
        # tb.field_names =['','今日（万）{}'.format(change),'今日占比','5日（万）{}'.format(change5),'5日占比','10日（万）{}'.format(change10),'10日占比']
        # tb.add_row([color.magenta('主力'),ZLZJ,ZLZB,ZLZJ5,ZLZB5,ZLZJ10,ZLZB10])
        # tb.add_row([color.red('超大'),CDZJ,CDZB,CDZJ5,CDZB5,CDZJ10,CDZB10])
        # tb.add_row([color.yellow('大单'),DDZJ,DDZB,DDZJ5,DDZB5,DDZJ10,DDZB10])
        # tb.add_row([color.cyan('中单'),ZDZJ,ZDZB,ZDZJ5,ZDZB5,ZDZJ10,ZDZB10])
        # tb.add_row([color.green('小单'),XDZJ,XDZB,XDZJ5,XDZB5,XDZJ10,XDZB10])

        
        # tb_deal = pt.PrettyTable()
        # tb_deal.field_names = ['','买价','买量',' ','卖价','卖量']
        # tb_deal.add_row([color.red('买一'),color.red(deal_detail['b1_p'][0]),color.red(deal_detail['b1_v'][0]),color.green('卖一'),color.green(deal_detail['a1_p'][0]),color.green(deal_detail['a1_v'][0])])
        # tb_deal.add_row(['买二',deal_detail['b2_p'][0],deal_detail['b2_v'][0],'卖二',deal_detail['a2_p'][0],deal_detail['a2_v'][0]])
        # tb_deal.add_row(['买三',deal_detail['b3_p'][0],deal_detail['b3_v'][0],'卖三',deal_detail['a3_p'][0],deal_detail['a3_v'][0]])
        # tb_deal.add_row(['买四',deal_detail['b4_p'][0],deal_detail['b4_v'][0],'卖三',deal_detail['a4_p'][0],deal_detail['a4_v'][0]])
        # tb_deal.add_row(['买五',deal_detail['b5_p'][0],deal_detail['b5_v'][0],'卖三',deal_detail['a5_p'][0],deal_detail['a5_v'][0]])




        ptb = pt.PrettyTable()
        ptb.field_names = [' ','今日（万）{}'.format(change),'今日占比','5日（万）{}'.format(change5),'5日占比','10日（万）{}'.format(change10),'10日占比','竞买','买价','买量','竞卖','卖价','卖量',]
        ptb.add_row([color.magenta('主力'),ZLZJ,ZLZB,ZLZJ5,ZLZB5,ZLZJ10,ZLZB10,color.red('买一'),color.red(deal_detail['b1_p'][0]),color.red(deal_detail['b1_v'][0]),color.green('卖一'),color.green(deal_detail['a1_p'][0]),color.green(deal_detail['a1_v'][0]),])
        ptb.add_row([color.red('超大'),CDZJ,CDZB,CDZJ5,CDZB5,CDZJ10,CDZB10,'买二',deal_detail['b2_p'][0],deal_detail['b2_v'][0],'卖二',deal_detail['a2_p'][0],deal_detail['a2_v'][0],])
        ptb.add_row([color.yellow('大单'),DDZJ,DDZB,DDZJ5,DDZB5,DDZJ10,DDZB10,'买三',deal_detail['b3_p'][0],deal_detail['b3_v'][0],'卖三',deal_detail['a3_p'][0],deal_detail['a3_v'][0],])
        ptb.add_row([color.cyan('中单'),ZDZJ,ZDZB,ZDZJ5,ZDZB5,ZDZJ10,ZDZB10,'买四',deal_detail['b4_p'][0],deal_detail['b4_v'][0],'卖三',deal_detail['a4_p'][0],deal_detail['a4_v'][0],])
        ptb.add_row([color.green('小单'),XDZJ,XDZB,XDZJ5,XDZB5,XDZJ10,XDZB10,'买五',deal_detail['b5_p'][0],deal_detail['b5_v'][0],'卖三',deal_detail['a5_p'][0],deal_detail['a5_v'][0],])


        # tb_market = pt.PrettyTable()
        # tb_market.field_names = ['上证指数','上证涨跌%','名称','现价','涨跌%','昨收']
        # tb_market.add_row([sh,sh_percent,deal_detail['name'][0],deal_detail['price'][0],round((float(deal_detail['price'][0])-float(deal_detail['pre_close'][0]))/float(deal_detail['pre_close'][0])*100,2),deal_detail['pre_close'][0]])
        
        if market['price'][0] > market['pre_close'][0]:
            title = color.red('{}/{}%↑'.format(sh,sh_percent))  
        else:
            title = color.green('{}/{}%↓'.format(sh,sh_percent))

        if deal_detail['price'][0] > deal_detail['pre_close'][0]:
            p = color.red(str(deal_detail['price'][0])+'↑')
        else:
            p = color.green(str(deal_detail['price'][0])+'↓')
        if data['f170'] > 0:
            c = color.red('{}%↑'.format(data['f170']/100))
        else:
            c = color.green('{}%↓'.format(data['f170']/100))
        
        print('上证:',title)
        print('{}\t现价:{}\t涨幅:{}\t昨收:{}'.format(deal_detail['name'][0],p,c,deal_detail['pre_close'][0]))
        print(ptb)
        # print(tb_deal)
        # print(tb)
        

        if datetime.now() < close_time:

            time.sleep(5)
        else:
            print('休市.....')
            break



if __name__ == '__main__':

    # code = input('代码：')
    # stat('601727')

    fundStock('002169')

