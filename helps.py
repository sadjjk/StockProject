import logging
import time
import traceback


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

def add_code_sign(code):

    if code[:3] in ['000','002','300','001','003']:
        code = 'sz' + code
    elif code[:3] in ['600','601','603','688']:
        code = 'sh' + code

    return  code



