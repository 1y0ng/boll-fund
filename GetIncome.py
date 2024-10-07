import os
import sys

import numpy as np
from GetRSI import get_rsi
from GetImg import get_list

num = 100
code = "501012"
d = "2024-09-23"
series_list , day = get_list(code,num,d)
Rsis = get_rsi(series_list[:],num)
series_list = series_list[0:num+19]
series_list.reverse()
day.reverse()
total = 0
holdings = 0
buy = 0
holds = []
sale = 0
buy_moneys = []
sale_moneys = []
buy_series = []
index_money = 10
for i in range(num):
    maney = index_money if Rsis[i]>30 else index_money*2
    twenty_list = series_list[i:i + 20]
    series = twenty_list[-1] # 当天净值
    # print(list)
    average = np.mean(twenty_list)  # 平均值
    std = np.std(twenty_list, ddof=1)  # 标准差
    high = average + 1.5 * std  # 高位线
    low = average - 1.5 * std  # 低位线
    #每次买10元
    if series<=low:

        holding = maney / series
        print("%s买入%d元，对应份额%f，当前净值%f"%(day[i],maney,holding,series))
        total += maney
        buy += maney
        holdings += holding
        holds.append(holding)
        buy_series.append(series)
        buy_moneys.append(maney)
    # if series <= low:
    #     holding = maney / series
    #     print("%s买入%f元，对应份额%f，当前净值%f" % (day[i],maney ,holding, series))
    #     total += maney
    #     buy += maney
    #     holdings += holding
    #     holds.append(holding)
    #     buy_series.append(series)
    #     maney += 5
    # 仅卖出10元
    # if series>=high and total>0:
    #     sale_time += 1
    #     holding = holds.pop()
    #     s = holding*series
    #     total -= s
    #     sale += s
    #     holdings -= holding
    #     print("%s卖出%f元，对应份额%f，当前净值%f,剩余余额：%f"%(day[i],s,holding,series,total))
    if series>=high and total>0:

        holding = 0
        if Rsis[i]>65:
            while len(buy_series)>0 and series > buy_series[-1] and len(buy_moneys)>0:
                sale_moneys.append(buy_moneys.pop())
                holding += holds.pop()
                buy_series.pop()
        else:
            holding = holds.pop()
            sale_moneys.append(buy_moneys.pop())
        s = holding*series
        total = total-s if total-s>0 else 0
        sale += s
        holdings -= holding

        print("%s卖出%f元，对应份额%f，当前净值%f,剩余余额：%f"%(day[i],s,holding,series,total))

print(f"已买入{buy}元,已卖出{sale}元,对应本金{sum(sale_moneys)}")
if total<=0:
    print("已清仓")
    sys.exit()
Market_value_of_holdings = series_list[-1]*holdings

print('持有金额：%f  持有份额：%f   持仓市值：%f   基金净值：%f'%(total,holdings,Market_value_of_holdings,series_list[-1]))
print("持有收益：",Market_value_of_holdings-total)
print("持有收益率：%f%%"%((Market_value_of_holdings-total)/total*100))

