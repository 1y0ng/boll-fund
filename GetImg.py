# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import requests
import re
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np 
from multiprocessing.dummy import Pool
def get_gsz(code):
    t = time.time()
    url='http://fundgz.1234567.com.cn/js/'+code+'.js?rt='+str(round(t * 1000))
    req=requests.get(str(url)).content.decode()
    if 'name' in req and 'gsz' in req:
        name=re.findall('name\":\"(.*?)\"',req)[0]
        gsz=re.findall('gsz\":\"(.*?)\"',req)
        return [float(gsz[0]),name]
def get_cur_month():
        # 获取当前日期
        return datetime.now().strftime("%Y-%m-%d")
def get_yesterday():
    return (datetime.now().date() - relativedelta(days=1)).strftime("%Y-%m-%d")
def get_date(n):
    # the_date = datetime(y,m,d)
    result_date = datetime.now().date() - relativedelta(days=n)
    d = result_date.strftime('%Y-%m-%d')
    week=datetime.strptime(d,"%Y-%m-%d").weekday() + 1
    return d,week

def get_last_month(d,number=3):# 获取前几个月
        month_date = datetime.strptime(d,"%Y-%m-%d") - relativedelta(months=number)
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

# def get_list(code,num):
#     dd=[]
#     series_list.append(get_gsz(code)[0])
#     date=get_cur_month()
#     x.append(date[5:])
#     url='http://hk.dayfund.cn/fundvalue/'+code+'.html?sdate='+get_last_month(date,(num+20)//20+2)+'&edate='+date
#     req=requests.get(url,headers=headers).content
#     soup = BeautifulSoup(req, "html.parser")
#     row1 = soup.select('tr.row1 > td')
#     row2 = soup.select('tr.row2 > td')
#     for i in range((num+22)//2):
#         dd.append(row1[i*9].get_text())
#         dd.append(row2[i*9].get_text())
#         # print(row1[i*9+3].get_text())
#         # print(row2[i*9+3].get_text())
#         series_list.append(float(row1[i*9+3].get_text()))
#         series_list.append(float(row2[i*9+3].get_text()))
#     for i in range(num-1):
#         x.append(dd[i][5:])
#     return series_list

def get_list(code,num,edate = get_cur_month()):
    try:
        if len(code)!=6:
            raise Exception("基金代码不是6位")

        if edate == get_cur_month() or edate == "":
            x = [get_cur_month()[5:]]
            series_list=[get_gsz(code)[0]]
            edate = get_yesterday()
        else:
            series_list = []
            x=[]

        sdate = get_last_month(edate,(num+20)//20+2)
        page = 1
        url = f"https://fundf10.eastmoney.com/F10DataApi.aspx?type=lsjz&code={code}&page={page}&per=49&sdate={sdate}&edate={edate}"
        print(url)
        req=requests.get(url).content.decode()
        pages = int(re.search(r"pages:(.*?),", req).group(1))
        series_list += [float(j) for j in re.findall(r"<td class='tor bold'>(.*?)</td><td class='tor bold'>", req)]
        x += [i[5:] for i in re.findall(r"<tr><td>(.*?)</td><td class='tor bold'>", req)]
        if pages > 1:
            for i in range(2, pages + 1):
                url = f"https://fundf10.eastmoney.com/F10DataApi.aspx?type=lsjz&code={code}&page={i}&per=49&sdate={sdate}&edate={edate}"

                req=requests.get(url).content.decode()
                series_list += [float(j) for j in re.findall(r"<td class='tor bold'>(.*?)</td><td class='tor bold'>", req)]
                x += [i[5:] for i in re.findall(r"<tr><td>(.*?)</td><td class='tor bold'>", req)]
        return series_list,x[:num]
    except Exception as e:

        print(f"基金代码{code}有误    "+str(e))
        return [],[]

def assignment(i):
    global series_list, h, l, x, mid, t, num
    list=series_list[i:i+20]
    # print(list)
    average=np.mean(list)#平均值
    std=np.std(list, ddof=1)#标准差
    high=average+1.5*std#高位线
    low=average-1.5*std#低位线
    t[num-i-1]=list[0]
    mid[num-i-1]=average
    h[num-i-1]=high
    l[num-i-1]=low

j=0
num=50
# code='010364'
t=[]#当日净值
mid=[]#20日均线
l=[]#低位线
h=[]#高位线
x=[]
series_list=[]
# print(x)
def run(code,n=100,T=""):
    global series_list,h,l,x,mid,t,num
    num=n if (n!=0 and n!=None) else 100
    series_list,x=get_list(code,num,T)
    x.reverse()
    t=[0]*num#当日净值
    mid=[0]*num#20日均线
    l=[0]*num#低位线
    h=[0]*num#高位线
    # for i in range(num):
    #     assignment(i,num)
    # pool=Pool(3)
    # ll=[o for o in range(num)]
    # pool.map(assignment,ll)

    for i in range(num):
        assignment(i)

    # plt.rcParams['font.sans-serif']= ['Microsoft YaHei', 'SimHei', 'SimSun']#中文输出
    plt.figure(figsize=(15, 4))#设置宽为1500px,高为400px
    plt.title(str(code))
    plt.plot(x, t, color='blue',marker='D', markersize=3, label='net worth')
    plt.plot(x, l, color='green', marker='D', markersize=3,label='Low order line')
    plt.plot(x, h, color='purple',marker='D', markersize=3, label='High water mark')
    plt.plot(x, mid, color='red', marker='D', markersize=3,label='20 day moving average')
    plt.xlabel('time')
    plt.ylabel('net worth')
    plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0)
    # for x1, y1 in zip(x, t):
    #     plt.text(x1, y1, str(y1), ha='center', va='bottom', fontsize=10)
    plt.show()
# print(get_list_2("012417",20))
# run("012417")
