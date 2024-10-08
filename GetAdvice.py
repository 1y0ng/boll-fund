from GetImg import get_list, get_gsz
import numpy as np

from GetRSI import get_rsi


def read_f(file_name):#读取文本内容
    list_id=[]
    for line in open(file_name,encoding='utf-8'):
        list_id.append(line.rstrip('\n'))
    return list_id


def print_out(buys,sales):#汇总输出
    if len(buys):
        print("今日推荐购买的基金有：")
        for obj in buys:
            print("   ",obj)
    else:
        print("今日无基金购买建议")
    if len(sales): 
        print("今日推荐卖出的基金有：")
        for obj in sales:
            print("   ",obj)
    else:
        print("今日无基金卖出建议")

def get_line(code):#对相关基金历史净值进行爬取
    try:
        name=get_gsz(code)[1]
        series_list , _ = get_list(code,25)
        RSI = get_rsi(series_list, 25)[-1]
        series_list = series_list[-20:]
        arr_mean = np.mean(series_list)#平均值
        arr_std = np.std(series_list, ddof=1)#标准差
        x = ""
        if RSI>70 or RSI<30:
            x = "***"
        elif RSI>65 or RSI<35:
            x = "**"
        elif RSI>60 or RSI<40:
            x = "*"
        if series_list[-1]>arr_mean+1.5*arr_std:
            sales.append(code+name+x)
        elif series_list[-1]<arr_mean-1.5*arr_std:
            buys.append(code+name+x)
    except Exception as e:
        print("基金代码{}有误".format(code),e)


headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
}
buys=[]
sales=[]
# print(datetime.now().strftime("%Y-%m-%d"))
def run():
    codes=read_f('ku.txt')
    for code in codes:
        if len(code)==6:
            get_line(code)
    print_out(buys,sales)
