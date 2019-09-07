import random

'''
新浪股票接口():
    单支股票
        1.股数当前概述 http://hq.sinajs.cn/list=s_sh603160
        result: var hq_str_s_sh603160="汇顶科技,205.000,1.790,0.88,117,240";
                                       股票名称,当前价格,当前价-昨收价,涨跌幅,成交量,成交金额

        2.股票当前详情 http://hq.sinajs.cn/list=sh603160
        result: var hq_str_sh603160="汇顶科技,205.000,203.210,204.500,205.900,203.220,204.500,204.570,87905,18013863.000,500,204.500,100,204.400,200,204.340,500,204.010,5400,204.000,100,204.570,300,204.670,200,204.770,6300,204.800,700,204.880,2019-08-29,09:31:33,00,";
                                  股票名称,今日开盘价,昨日收盘价,当前价格,今日最高价,今日最低价,买一价,卖一价,成交量,成交金额,买一申报股数,买一报价,买二申报股数,买二报价,...,卖一申报股数,卖一报价,日期,时间

    多支股票
        1.http://hq.sinajs.cn/list=sh603160,sz000858
        2.http://hq.sinajs.cn/list=s_sh603160,s_sz000858

腾讯股票接口
    单支股票
        1.股票当前分时 http://data.gtimg.cn/flashdata/hushen/minute/sz000858.js
        result: min_data="\n\
                date:190829\n\
                0930 134.40 6848\n\
                0931 134.97 9946\n\
                0932 134.60 11949\n\
                时间 当前价 成交量
        存在的问题: 更新的太慢 非实时

        2.股票最近历史 http://data.gtimg.cn/flashdata/hushen/latest/daily/sz000858.js
        result: latest_daily_data="\n\
                num:100 total:5039 start:980427 98:176 99:237 00:238 01:236 02:235 03:239 04:241 05:241 06:207 07:233 08:235 09:237 10:241 11:242 12:242 13:238 14:245 15:184 16:244 17:244 18:243 19:161\n\
                190404 94.66 100.23 101.53 94.19 516297\n\
                190408 104.65 102.00 105.39 100.01 535741\n\
                年月日  开盘价  收盘价 最高价 最低价 成交量

东方财富大盘指数接口
    单只指数
    API: http://push2.eastmoney.com/api/qt/ulist.np/get?fields=f2,f3,f4,f6,f104,f105,f106&secids=1.000001
    result : {"rc":0,"rt":11,"svr":181240774,"lt":1,"full":1,"data":{"total":1,"diff":[{"f2":288624,"f3":-16,"f4":-468,"f6":224751169536.0,"f104":296,"f105":1191,"f106":43}]}}

                                                                                                上证：2886.24 -4.68 -0.16% 2247.51亿元(涨:296 平:43 跌:1191)

    多只指数
    加逗号

东方财富股票排序接口
    API：http://40.push2.eastmoney.com/api/qt/clist/get?&pn=1&pz=10&po=1&fid=f6&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2&fields=f12,f14,f6
    获取相应字段  参数 pn 页数  pz每页个数 po 1:正序/0:倒序 fid 指定某列排序

'''


UserAgents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
#            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36",
#            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
#            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0",
#            "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0"
        ]


# 增加UserAgent
HEADERS = {
    "user-agent": random.choice(UserAgents)}

SINA_STOCK_SHORT_URL = "http://hq.sinajs.cn/list=s_"
SINA_STOCK_URL = "http://hq.sinajs.cn/list="

TENCENT_STOCK_MINUTE_URL = "http://data.gtimg.cn/flashdata/hushen/minute/%s.js"
TENCENT_STOCK_HISTORY_URL = "http://data.gtimg.cn/flashdata/hushen/latest/daily/%s.js"

EASTMONEY_MARKEY_INDEX_URL = 'http://push2.eastmoney.com/api/qt/ulist.np/get?fields=f2,f3,f4,f6,f104,f105,f106&secids='

EASTMONEY_STOCK_RANK_URL = 'http://40.push2.eastmoney.com/api/qt/clist/get?&pn=1&pz=10&po=1&fid=%s&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2&fields=%s'

CURRENT_PRICE = 'f2'  # 当前价
VOLUMN_AMOUNT = 'f6'  # 成交量金额
AMPLITUDE = 'f7'  # 振幅
TURNOVER_RATE = 'f8'  # 换手率

TOP_BANNER_LIST = [
    {
        'field_name': 'f2',
        'chinese_name': '当前价',
        'unit_symbol': '',
        'unit_num': 100,
        'data': []
    },
    {
        'field_name': 'f6',
        'chinese_name': '成交量金额',
        'unit_symbol': '亿元',
        'unit_num': 100000000,
        'data': []
    },
    {
        'field_name': 'f7',
        'chinese_name': '振幅',
        'unit_symbol': '%',
        'unit_num': 100,
        'data': []
    },
    {
        'field_name': 'f8',
        'chinese_name': '换手率',
        'unit_symbol': '%',
        'unit_num': 100,
        'data': []
    }
]
