import logging
import time
import traceback
import tushare as ts

'''
定义装饰器，用于检查各个函数的的异常
'''
def check_func(func):
    def inner(*args, **kwargs):    # *argv可以处理变长参数的情况，其中，logger对象是最后一个参数
        start = time.time()
        try:
            res = func(*args, **kwargs)
            end = time.time()
            logging.info('%s total time cost : %.3f seconds \n'
                         'args:%s kwargs:%s' % (func.__name__, (end - start), str(args),str(kwargs)))
            return res
        except:
            logging.error('%s failed \n'
                          'args:%s kwargs:%s' % (func.__name__ ,args,kwargs) + traceback.format_exc())

    return inner


def check_response(r):

    if r.status_code != 200:
        logging.error("API_URL:{}\nSTATUS CODE {}".format(
            r.url, r.status_code
        ))
        raise  ValueError('接口API异常！请检查')

# 股票代码增加前缀标识符
def add_code_sign(code):

    if code[:3] in ['000','002','300','001','003']:
        code = 'sz' + code
    elif code[:3] in ['600','601','603','688']:
        code = 'sh' + code

    return  code

# 交易日判断
def is_trade_time(now_time):
    pro = ts.pro_api('XXXXXXXXXXXXXXXXXX')

    current_date = now_time.strftime('%Y%m%d')
    current_time = now_time.strftime('%H%M%S')

    is_open = pro.trade_cal(start_date=current_date, end_date=current_date)['is_open'].values[0]
    if is_open == 0 :
        return  0
    else:
        if 93000 < int(current_time) <113030:
            return  1
        elif 130000 < int(current_time) < 150030:
            return  1
        else:
            return 0


