from bottle import run,route,template,static_file,default_app,request,redirect
from stock_details import  *
import traceback
import datetime
import logging
import re






@route("/")
@route("/index")
def index():
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    hs300_data = get_stock_detail(get_hs300())
    my_stock_data = get_stock_detail(get_my_stock())
    market_index_data = get_market_index()

    return template('index',current_date = current_date,
                            current_time = current_time,
                            my_stock_data = my_stock_data,
                            hs300_data = hs300_data,
                            market_index_data=market_index_data,
                            top_banner_data = get_top_banner()
                    )


@route('/index', method = 'post')
def index():
    new_code = request.POST.get('code')
    add_my_stock(new_code)





@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static')



@route("/stock/<code>")
def stock_figure(code):


    if re.search(r'^\d{6}$',code):

        try:


            history_data = get_stock_history(code)

            minute_data = get_stock_minute(code)

            # print(minute_data[-1])
            single_stock_detail = get_stock_detail([code])[0]
            return template('figure',history_data = history_data,
                                           minute_data = {"data":minute_data,
                                                          "yestclose":single_stock_detail[6]},
                                           stock_info = single_stock_detail).replace('&#039;',"'")
        except:
            return template('error')
            logging.warning('获取股票编码失败')
            logging.warning('错误信息:' + traceback.format_exc())
    else:
        return  template('error')

@route("/error")
def error():
    return template('error')

#run(host = 'localhost', port = 8002, debug = True, reloader = True)
application = default_app()


