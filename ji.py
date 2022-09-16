#!/usr/bin/python
# -*- coding: UTF-8 -*-
from enum import Flag
from ntpath import join
import requests
import re
from multiprocessing.dummy import Pool
import datetime
import calendar
import time
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import numpy as np 
import ways
def get_gsz(code):
    t = time.time()
    url='http://fundgz.1234567.com.cn/js/'+code+'.js?rt='+str(round(t * 1000))
    req=requests.get(str(url)).content.decode()
    name=re.findall('name\":\"(.*?)\"',req)[0]
    gsz=re.findall('gsz\":\"(.*?)\"',req)
    return [float(gsz[0]),name]
def get_cur_month():
        # 获取当前月
        return datetime.now().strftime("%Y-%m-%d")

def get_last_month( number=2):
        # 获取前几个月
        month_date = datetime.now().date() - relativedelta(months=number)
        return month_date.strftime("%Y-%m-%d")


headers={
    'Sec-Ch-Ua':'\"Microsoft Edge\";v=\"105\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"105\"',
    'Sec-Ch-Ua-Mobile':'?0',
    'Sec-Ch-Ua-Platform':'\"Windows\"',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site':'same-origin',
    'Sec-Fetch-Mode':'navigate',
    'Sec-Fetch-User':'?1',
    'Sec-Fetch-Dest':'document',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6'
}
buys=[]
sales=[]

def get_line(code):
    res=get_gsz(code)
    series_list=[res[0]]
    name=res[1]
    url='https://www.dayfund.cn/fundvalue/'+code+'.html?sdate='+get_last_month()+'&edate='+get_cur_month()
    url2='http://www.dayfund.cn/fundvalue/'+code+'.html?sdate='+get_last_month()+'&edate='+get_cur_month()
    req=requests.get(str(url),headers=headers).content.decode()
    soup = BeautifulSoup(req, "html.parser")
    row1 = soup.select('tr.row1 > td')
    row2 = soup.select('tr.row2 > td')
    for i in range(9):
        #     print(float(row1[i*9+3].get_text()))
        # print(float(row2[i*9+3].get_text()))
        series_list.append(float(row1[i*9+3].get_text()))
        series_list.append(float(row2[i*9+3].get_text()))
    series_list.append(float(row1[9*9+3].get_text()))
    arr_mean = np.mean(series_list)
    arr_std = np.std(series_list, ddof=1)*0.7
    # print(series_list)
    if series_list[0]>arr_mean+2*arr_std:
        sales.append(code+name)
        # print('sale it')
        # print('Net worth today:',series_list[0])
        # print('Hotline:',arr_mean+2*arr_std)
        # print('20 day EMA:',arr_mean)
        # print('Subcooling line:',arr_mean-2*arr_std)
    elif series_list[0]<arr_mean-2*arr_std:
        buys.append(code+name)
        # print('buy it')
        # print('Net worth today:',series_list[0])
        # print('Hotline:',arr_mean+2*arr_std)
        # print('20 day EMA:',arr_mean)
        # print('Subcooling line:',arr_mean-2*arr_std)        
    # else:
    #     print('keep it')
codes=ways.read_f('code.txt')

code2='008591'
# pool=Pool(5)
for code in codes:
    get_line(code)
# pool.map(get_line,codes)
data={
    "buy":{
        "value":'\n'+'\n'.join(buys),
        "color":"#173177"
    },
    "sale":{
        "value":'\n'+'\n'.join(sales),
        "color":"#173177"
    }
}
ways.send_msg('VkKpTCkHqCv2o_raY0d45VF2sPspXoio0F21ufS_zbs',data)
# print(':'.join(buys))
# print(sales)
