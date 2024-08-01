import requests
import re
import datetime
import time
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import numpy as np 
def get_gsz(code):
    t = time.time()
    url='http://fundgz.1234567.com.cn/js/'+code+'.js?rt='+str(round(t * 1000))
    req=requests.get(str(url)).content.decode()
    if 'name' in req and 'gsz' in req:
        name=re.findall('name\":\"(.*?)\"',req)[0]
        gsz=re.findall('gsz\":\"(.*?)\"',req)
        return [float(gsz[0]),name]

def get_cur_month():# 获取当前月
        return datetime.now().strftime("%Y-%m-%d")

def get_last_month( number=2):# 获取前几个月
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
def run(code):
    try:
        res=get_gsz(code)
        series_list=[res[0]]
        print("基金名为:",res[1])
        url='https://www.dayfund.cn/fundvalue/'+code+'.html?sdate='+get_last_month()+'&edate='+get_cur_month()
        url2='http://www.dayfund.cn/fundvalue/'+code+'.html?sdate='+get_last_month()+'&edate='+get_cur_month()
        req=requests.get(str(url),headers=headers).content.decode()
        soup = BeautifulSoup(req, "html.parser")
        row1 = soup.select('tr.row1 > td')
        row2 = soup.select('tr.row2 > td')
        for i in range(9):
            series_list.append(float(row1[i*9+3].get_text()))
            series_list.append(float(row2[i*9+3].get_text()))
        series_list.append(float(row1[9*9+3].get_text()))
        arr_mean = np.mean(series_list)
        arr_std = np.std(series_list, ddof=1)
        print('今日净值:',series_list[0])
        print('高位线:',arr_mean+1.5*arr_std)
        print('20日均线:',arr_mean)
        print('低位线:',arr_mean-1.5*arr_std)
        if series_list[0]<arr_mean-1.5*arr_std:
            print("推荐购买！！！")
        elif series_list[0]>arr_mean+1.5*arr_std:
            print('建议卖出')
    except:
        print("基金代码{}有误".format(code))

