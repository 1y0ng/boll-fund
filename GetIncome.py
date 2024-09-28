import os
import sys

import numpy as np

from GetImg import get_list

num = 300
series_list , day = get_list("005064",num,"2024-09-23")
series_list = series_list[0:num+19]
series_list.reverse()
day.reverse()
total = 0
holdings = 0
buy = 0
holds = []
sale = 0
sale_time = 0
buy_series = []
maney = 10
for i in range(num):
    twenty_list = series_list[i:i + 20]
    series = twenty_list[-1] # 当天净值
    # print(list)
    average = np.mean(twenty_list)  # 平均值
    std = np.std(twenty_list, ddof=1)  # 标准差
    high = average + 1.5 * std  # 高位线
    low = average - 1.5 * std  # 低位线
    #每次买10元
    if series<=low:
        holding = 10 / series
        print("%s买入10元，对应份额%f，当前净值%f"%(day[i],holding,series))
        total += 10
        buy += 10
        holdings += holding
        holds.append(holding)
        buy_series.append(series)
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
        while len(buy_series)>0 and series > buy_series[-1]:
            sale_time += 1
            holding += holds.pop()
            buy_series.pop()
        s = holding*series
        total = total-s if total-s>0 else 0
        sale += s
        holdings -= holding

        print("%s卖出%f元，对应份额%f，当前净值%f,剩余余额：%f"%(day[i],s,holding,series,total))

print(f"已买入{buy}元,已卖出{sale}元,对应本金{sale_time*10}")
if total<=0:
    print("已清仓")
    sys.exit()
Market_value_of_holdings = series_list[-1]*holdings

print('持有金额：%f  持有份额：%f   持仓市值：%f   基金净值：%f'%(total,holdings,Market_value_of_holdings,series_list[-1]))
print("持有收益：",Market_value_of_holdings-total)
print("持有收益率：%f%%"%((Market_value_of_holdings-total)/total*100))

