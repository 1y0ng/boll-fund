# -*- coding: UTF-8 -*-
import requests
import re
import datetime
import time
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import numpy as np 
def read_f(file_name):#读取文本内容
    list_id=[]
    for line in open(file_name,encoding='utf-8'):
        list_id.append(line.rstrip('\n'))
    return list_id


def get_gsz(code):#根据编号获取基金当日净值和名字
    t = time.time()
    url='http://fundgz.1234567.com.cn/js/'+code+'.js?rt='+str(round(t * 1000))
    req=requests.get(str(url)).content.decode()
    if 'name' in req and 'gsz' in req:
        name=re.findall('name\":\"(.*?)\"',req)[0]
        gsz=re.findall('gsz\":\"(.*?)\"',req)
        return [float(gsz[0]),name]

def get_cur_month():# 获取当前日期
        return datetime.now().strftime("%Y-%m-%d")

def get_last_month(number=2):# 获取前number个月的日期
        month_date = datetime.now().date() - relativedelta(months=number)
        return month_date.strftime("%Y-%m-%d")

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
        res=get_gsz(code)
        series_list=[res[0]]
        name=res[1]
        url='https://www.dayfund.cn/fundvalue/'+code+'.html?sdate='+get_last_month()+'&edate='+get_cur_month()#爬取的url
        req=requests.get(str(url),headers=headers).content.decode()
        soup = BeautifulSoup(req, "html.parser")#利用bs4对提取净值
        row1 = soup.select('tr.row1 > td')
        row2 = soup.select('tr.row2 > td')
        for i in range(9):
            series_list.append(float(row1[i*9+3].get_text()))
            series_list.append(float(row2[i*9+3].get_text()))
        series_list.append(float(row1[9*9+3].get_text()))
        arr_mean = np.mean(series_list)#平均值
        arr_std = np.std(series_list, ddof=1)#标准差
        # print(series_list)
        if series_list[0]>arr_mean+1.5*arr_std:
            sales.append(code+name)
        elif series_list[0]<arr_mean-1.5*arr_std:
            buys.append(code+name)
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
run()