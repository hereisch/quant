# -*- coding: utf-8 -*-#
import json
import os
import re
import requests
import time


MONGOHOST = '192.168.0.28'

EastmoneyURL={
    # 东财人气榜
    'Eastmoney_hot' : 'https://push2.eastmoney.com/api/qt/ulist.np/get?ut=f057cbcbce2a86e2866ab8877db1d059&fltt=2&invt=2&fields=f14%2Cf148%2Cf3%2Cf12%2Cf2%2Cf13&secids=0.002131,0.300134,0.002047,1.600238,0.300494,1.600522,1.600804,1.600989,0.002011,0.000930,0.002510,0.002487,0.002728,0.000625,0.002056,0.000651,1.605133,1.603458,0.002610,1.601279,1.600982,0.002405,0.002885,1.605199,0.002433,0.002432,0.002263,1.600196,0.300058,1.605333,0.000422,1.603606,1.600742,1.601311,0.300081,0.002852,0.300987,0.300264,0.002255,1.603917,1.603730,0.001267,1.601919,1.603078,0.300059,1.600856,0.300052,1.600519,0.002624,0.002943,0.002806,0.002483,0.001216,1.600905,0.002655,1.601126,0.300296,0.002032,1.605198,0.300113,1.600996,1.600276,0.300507,0.002287,0.000665,1.603355,0.000596,0.002241,1.603985,0.300848,0.300440,1.603090,1.603703,0.300750,0.000661,0.002594,0.002643,0.000858,1.600653,0.300179,0.300376,1.605286,1.601012,0.300199,0.300142,1.600031,0.301180,1.603259,1.600423,1.600030,0.002026,1.603286,1.605050,1.603392,0.002466,1.603028,0.002865,0.000977,0.300139,0.300360,?v=08997332915578472',
    # 盘后历史资金流
    'Eastmoney_history_flow' : 'https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?fields1=f1%2Cf2%2Cf3%2Cf7&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61%2Cf62%2Cf63%2Cf64%2Cf65&secid={}',
    # 个股资金流
    'Eastmoney_flow':'http://push2.eastmoney.com/api/qt/stock/fflow/kline/get?lmt=0&klt=1&fields1=f1%2Cf2%2Cf3%2Cf7&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61%2Cf62%2Cf63%2Cf64%2Cf65&ut=b2884a393a59ad64002292a3e90d46a5&secid={}',
    # 个股历史分价表
    'SinaPriceHis' : 'https://market.finance.sina.com.cn/iframe/pricehis.php?symbol={}&startdate={}&enddate={}',
    #北向资金
    'South2North' : 'https://push2.eastmoney.com/api/qt/kamtbs.rtmin/get?fields1=f1,f2,f3,f4&fields2=f51,f54,f52,f58,f53,f62,f56,f57,f60,f61',


}
if __name__ == '__main__':
    
    pass