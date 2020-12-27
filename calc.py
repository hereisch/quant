# -*- coding: utf-8 -*-#
import json
import os
import re
import requests
import time



if __name__ == '__main__':

    price = float(input('买入单价：'))
    count = int(input('买入股数：'))
    sale = float(input('卖出单价：'))
    # （买入总成本 + 卖出过户费）÷(1 - 印花税率 - 交易佣金率)÷股票数量

    # （买入总成本 + 卖出过户费）
    buy = (price*count)*(1+0.0025+0.0002)

    cost = (sale*count*0.0002+buy)/(1-0.001-0.0025)/count
    profit = sale*count*(1-(0.001+0.0002+0.00025))
    print('------------------------------------------')
    print('单股成本：',cost,'收益：',profit,'买入成本：',buy)