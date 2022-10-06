# -*- coding: utf-8 -*-#
import json
import os
import re
import requests
import time
import pymongo
from tqdm import tqdm




headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://search.10jqka.com.cn',
    'Referer': 'https://search.10jqka.com.cn/unifiedmobile/?showAd=false&q=%E8%8E%B7%E5%88%A9%E7%AD%B9%E7%A0%81%E5%A4%A7%E4%BA%8E90&ipxA=0&isShowBack=false&qs=ths_mobile_yuyinzhushou&queryType=stock&subtype=non_yuyinzhushou',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
}


data =  {
        'query': '获利筹码大于80,去除st，去除创业板，去除科创板',
        'urp_sort_index':'',
        'urp_sort_way': 'desc',
        # 'condition': '[{"chunkedResult":"获利筹码大于80,_&_去除st,_&_去除创业板,_&_去除科创板","opName":"and","opProperty":"","sonSize":6,"relatedSize":0},{"indexName":"收盘获利","indexProperties":["nodate 1","交易日期 20210615","(0.8"],"source":"new_parser","type":"index","indexPropertiesMap":{"交易日期":"20210615","(":"0.8","nodate":"1"},"reportType":"TRADE_DAILY","dateType":"交易日期","valueType":"_浮点型数值(%)","domain":"abs_股票领域","uiText":"收盘获利>80%","sonSize":0,"queryText":"收盘获利>80%","relatedSize":0,"tag":"收盘获利"},{"opName":"and","opProperty":"","sonSize":4,"relatedSize":0},{"indexName":"股票简称","indexProperties":["不包含st"],"source":"new_parser","type":"index","indexPropertiesMap":{"不包含":"st"},"reportType":"null","valueType":"_股票简称","domain":"abs_股票领域","uiText":"股票简称不包含st","sonSize":0,"queryText":"股票简称不包含st","relatedSize":0,"tag":"股票简称"},{"opName":"and","opProperty":"","sonSize":2,"relatedSize":0},{"indexName":"上市板块","indexProperties":["不包含创业板"],"source":"new_parser","type":"index","indexPropertiesMap":{"不包含":"创业板"},"reportType":"null","valueType":"_上市板块","domain":"abs_股票领域","uiText":"上市板块不包含创业板","sonSize":0,"queryText":"上市板块不包含创业板","relatedSize":0,"tag":"上市板块"},{"indexName":"上市板块","indexProperties":["不包含科创板"],"source":"new_parser","type":"index","indexPropertiesMap":{"不包含":"科创板"},"reportType":"null","valueType":"_上市板块","domain":"abs_股票领域","uiText":"上市板块不包含科创板","sonSize":0,"queryText":"上市板块不包含科创板","relatedSize":0,"tag":"上市板块"}]',
        'codelist':'',
        'is_cache': 0,
        'perpage': 100,
        'page': 1,
        'logid': '2212eb84fc6da24cc25aa1266d1b68d3',
        'ret': 'json_all',
        'sessionid': '69eb13dc472827183fc1753cad23bc11',
        # 'iwc_token': '0ac9571516238928060796915',
        'urp_use_sort': 1,
        'user_id': 'ths_mobile_iwencai_703facea7571da9b0002bae481368c42',
        'uuids[0]': 18369,
        'query_type': 'stock',
        'comp_id': 5716439,
        'business_cat': 'soniu',
        'uuid': 18369,
}

client = pymongo.MongoClient(host="127.0.0.1", port=27017)
db = client['quant']



def jetton():
    print('获取筹码盘...')

    res = db.get_collection('jetton').find()
    for i in res:
        db.get_collection('today').update_many({'code':i['code']},{'$set':{'profit':i['profit']}})


def profit():
    db.get_collection('jetton').remove()
    url = 'https://ai.iwencai.com/urp/v7/landing/getDataList?hexin-v=AxRiEX69CA8m-JzDSk22RvcH5VmFbTRbeqLPCa6SpL4jI7pP1n0I58qhnJD9'
    # token = '0ac95118' + str(time.time()).replace('.','')
    token = '0ac9529d16239976685731253'
    print(token)
    for j in tqdm(range(1, 500)):
        data['page'] = j
        data['iwc_token'] = token
        resp = requests.post(url=url, headers=headers, data=data)
        if resp.json()['answer']['components'][0]['data']['datas']:
            j = resp.json()['answer']['components'][0]['data']['datas'][0]
            for p in list(j.keys()):
                if '收盘获利' in p:
                    chip = p
            for i in resp.json()['answer']['components'][0]['data']['datas']:
                i['profit'] = i[chip]
                db.get_collection('jetton').insert(i)
            time.sleep(3)
        else:
            break


if __name__ == '__main__':

    profit()
    jetton()
