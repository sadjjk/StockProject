from bottle import default_app, request, route, static_file, template,run,error
from stock_details import *
import datetime
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
                            top_banner_data = get_top_banner(),
                            footer_string = random.choice(FOOTER_STRING)
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
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.datetime.now().strftime('%H:%M:%S')

    if re.search(r'^(sh|sz)?\d{6}$',code):
        try:

            single_stock_detail = get_stock_detail([code])[0]
        except:
            # return  str({"code":500,"msg":"该股票代码:%s不存在！" % code}).encode('utf-8')
            return  template('error',current_date = current_date,
                            current_time = current_time,
                            footer_string=random.choice(FOOTER_STRING),
                            msg = "该股票代码:%s不存在！" % code
                            )

        history_data = get_stock_history(code)
        minute_data = get_stock_minute(code)
        return template('figure',history_data = history_data,
                                       minute_data = {"data":minute_data,
                                                      "yestclose":single_stock_detail[6]},
                                       stock_info = single_stock_detail).replace('&#039;',"'")

    else:
        # return  str({"code":500,"msg":"请输入6位股票代！" }).encode('utf-8')
        return template('error', current_date=current_date,
                        current_time=current_time,
                        footer_string=random.choice(FOOTER_STRING),
                        msg="请输入6位股票代码！"
                        )

@error(404)
def miss(error):
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.datetime.now().strftime('%H:%M:%S')

    return template('error',current_date = current_date,
                            current_time = current_time,
                            footer_string=random.choice(FOOTER_STRING),
                            msg = ''
                            )

# run(host = 'localhost', port = 8002, debug = True, reloader = True)
application = default_app()


