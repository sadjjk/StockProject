import json
import os
import pickle

import requests
import tushare as ts
from requests.adapters import HTTPAdapter

from config import *
from helps import add_code_sign, check_func, check_response

logging.basicConfig(level=logging.ERROR,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')



def get_hs300():

    if os.path.exists('.stock_hs300'):
        with open('.stock_hs300','rb') as f :
            stock_list = pickle.load(f)

    else:

        stock_list = list(ts.get_hs300s().code.values)
        with open('.stock_hs300','wb') as f:
            pickle.dump(stock_list, f)

    return  stock_list


def get_my_stock():

    if os.path.exists('.my_stock'):
        with open('.my_stock','rb') as f :
            stock_list = pickle.load(f)

    else:

        stock_list =[

            '600104',
            '000963',
            '002415'
        ]
        with open('.my_stock','wb') as f:
            pickle.dump(stock_list, f)

    return  stock_list

def add_my_stock(new_code):

    if os.path.exists('.my_stock'):
        with open('.my_stock','rb') as f :
            stock_list = pickle.load(f)
    else:
        stock_list = []

    if new_code not in stock_list:
        stock_list.append(new_code)
        with open('.my_stock','wb') as f:
            pickle.dump(stock_list, f)



@check_func
def get_stock_detail(stock_code_list,step = 80):

    stock_details_list = []

    stock_code_list  =  [add_code_sign(code) for code in stock_code_list ]

    for i in range(0,len(stock_code_list),step):

        stock_code_str = ",".join(stock_code_list[i:i+step])

        r = requests.get(SINA_STOCK_URL + stock_code_str,headers =HEADERS)

        check_response(r)

        r_list = r.text.splitlines()
        for line in r_list:

            stock_id = line[line.find("=")-8 : line.find("=")]

            stock_detail = line[line.find("\"") + 1:line.rindex("\"")]
            if len(stock_detail) > 0:
                stock_detail = stock_detail.split(",")

                stock_name =  stock_detail[0]
                stock_current_price = float(stock_detail[3])
                stock_yes_close = float(stock_detail[2])
                stock_price_diff = round(float(stock_detail[3]) - stock_yes_close,2)
                stock_range =  round(stock_price_diff / stock_yes_close * 100 ,2)
                stock_volumn = int(stock_detail[8])

                stock_details_list.append([stock_id,
                                           stock_name,
                                           stock_current_price,
                                           stock_price_diff,
                                           stock_range,
                                           stock_volumn,
                                           stock_yes_close])

    return  stock_details_list


@check_func
def get_stock_minute(code):

    minute_data = []
    minute_sum_price = 0
    minute_volume_sum = 0

    code = add_code_sign(code)


    r = requests.get(TENCENT_STOCK_MINUTE_URL % code,headers = HEADERS)

    check_response(r)
    minute_list = r.text.splitlines()[2:][:-1]
    for index, minute_line in enumerate(minute_list):
        minute_line = minute_line[:minute_line.find("\\")]
        minute_line = minute_line.split(" ")
        minute_sum_price += float(minute_line[1])
        minute_avg_price = round(minute_sum_price / (index + 1), 2)
        minute_volume = int(minute_line[2]) - minute_volume_sum
        minute_volume_sum = int(minute_line[2])
        minute_data.append([str(minute_line[0]), float(minute_line[1]), minute_avg_price, int(minute_volume)])

    return minute_data


@check_func
def get_stock_history(code):

    history_data = []
    code = add_code_sign(code)

    r = requests.get(TENCENT_STOCK_HISTORY_URL % code,headers = HEADERS)

    check_response(r)

    history_list = r.text.split("\\n\\")[2:][:-1]
    for history_line in history_list:
        history_line = history_line.strip().split(" ")
        date = history_line[0]
        date = '%s-%s-%s' % ('20' + date[:2], date[2:4], date[4:6])
        history_data.append([date, float(history_line[1]),
                             float(history_line[2]),
                             float(history_line[3]),
                             float(history_line[4]),
                             int(history_line[5])])

    return history_data


@check_func
def get_market_index():

    SH_MARKET_CODE = '1.000001' # 上证
    SZ_MARKEY_CODE = '0.399001' # 深证
    GEM_MARKET_CODE = '0.399006' # 创业板
    r = requests.get(EASTMONEY_MARKEY_INDEX_URL + ','.join([SH_MARKET_CODE,
                                                           SZ_MARKEY_CODE,
                                                           GEM_MARKET_CODE]),headers = HEADERS)
    check_response(r)

    data = json.loads(r.text)['data']['diff']

    data[0]['f1'] = '上证 '
    data[1]['f1'] = '深证 '
    data[2]['f1'] = '创业板'

    data[0]['f12'] = 'sh000001'
    data[1]['f12'] = 'sz399001'
    data[2]['f12'] = 'sz399006'

    for index_data in data:
        index_data['f3'] = str(float(index_data['f3']) /100)  # 涨跌幅
        index_data['f4'] = str(float(index_data['f4']) /100) # 涨跌值
        index_data['f6'] = str(round(float(index_data['f6'] /100000000),2)) + '亿元'
        index_data['f104'] = '涨:' + str(index_data['f104'])
        index_data['f106'] = '平:' + str(index_data['f106'])
        index_data['f105'] = '跌:' + str(index_data['f105'])

    return data



# 获取Top Banner
@check_func
def top_ten_stock(stock_field,unit):
    stock_name = 'f14'
    stock_code = 'f12'
    stock_range  ='f3'

    s = requests.session()
    s.mount('http://',HTTPAdapter(max_retries=3))
    r = s.get(EASTMONEY_STOCK_RANK_URL % (stock_field,','.join([stock_field,
                                                         stock_code,
                                                         stock_name,
                                                         stock_range])),headers = HEADERS)

    check_response(r)

    data = json.loads(r.text)['data']['diff']

    data = list(data.values())

    for index_data in data:

        index_data['f3'] = '%.2f' % (float(index_data['f3']) /100) # 涨跌幅
        index_data[stock_field] = '%.2f' % round(float(index_data[stock_field]) / unit , 2)

    return data



def get_top_banner():

    top_banner_data =  TOP_BANNER_LIST
    for item in top_banner_data:

        data = top_ten_stock(item['field_name'],unit=item['unit_num'])

        item['data']  = data

    return top_banner_data



if __name__ == '__main__':


    # stock_list = get_my_stock()

    # get_hs300()

    # data = get_stock_minute('AAAAA')

    data = top_ten_stock('f2',unit=100)
    # data = get_top_banner()

    data


