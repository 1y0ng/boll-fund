import os
import sys

import numpy as np
import matplotlib.pyplot as plt
from GetImg import get_list
code = "010364"
num = 200
series_list , x = get_list(code,num,"2024-09-30")
series_list.reverse()

x.reverse()
N = 27
k = 50
d = 50
ks = [k]
ds = [d]
js = [3*k-2*d]
# print(x)
series_list = series_list[len(series_list)-num-N+1:]
# print(series_list)
for i in range(N,len(series_list)):
    # print(x[i-N+1],series_list[i])
    RABGE = series_list[i-N+1:i+1]
    low = min(RABGE)
    high = max(RABGE)
    RSV =  100*(series_list[i]-low)/(high-low)
    # print(RSV)
    k = 2/3*k+1/3*RSV
    d = 2/3*d+1/3*k
    j = 3*k-2*d
    j = 120 if j > 120 else j
    j = -20 if j < -20 else j
    ks.append(k)
    ds.append(d)
    js.append(j)
# print(ks)
# print(ds)
# print(js)
# series_list = series_list[N-1:]


plt.figure(figsize=(15, 4))  # 设置宽为1500px,高为400px
plt.title(str(code))
plt.plot(x, ks, color='green', marker='D', markersize=3, label='k')
plt.plot(x, ds, color='purple', marker='D', markersize=3, label='d')
plt.plot(x, js, color='red', marker='D', markersize=3, label='j')
plt.xlabel('time')
plt.ylabel('KDJ')
plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0)
plt.show()