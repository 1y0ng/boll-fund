import matplotlib.pyplot as plt
from GetImg import get_list
from decimal import Decimal

def get_rsi(series_list,num=100,N=14):
    series_list.reverse()
    series_list = series_list[len(series_list)-num-N:]
    pluses = []
    losses = []
    for i in range(len(series_list)-1):
        dif = Decimal(str(series_list[i+1]))-Decimal(str(series_list[i]))
        if dif > 0:
            pluses.append(dif)
            losses.append(0)
        else:
            losses.append(-dif)
            pluses.append(0)

    avplues = [sum(pluses[:N])/N]
    avlosses = [sum(losses[:N])/N]
    RSs = [avplues[-1]/abs(avlosses[-1])]
    RSIs = [100 - 100/(1+RSs[-1])]
    for i in range(1,num):
        avplues.append((avplues[-1]*(N-1)+pluses[N+i-1])/N)
        avlosses.append((avlosses[-1]*(N-1)+losses[N+i-1])/N)
        RSs.append(avplues[-1]/abs(avlosses[-1]))
        RSIs.append(100 - 100/(1+RSs[-1]))
    return RSIs


def show_pic(code,x,RSIs):
    plt.figure(figsize=(15, 4))  # 设置宽为1500px,高为400px
    plt.title(str(code))
    # plt.plot(x, RSIs, color='green', marker='D', markersize=3, label='RSI')
    plt.xlabel('day')
    plt.ylabel('RSI(14)')
    # 阈值
    threshold_high = 70
    threshold_low = 30

    # 绘制点
    for i in range(len(x)):
        if RSIs[i] < threshold_high and RSIs[i] > threshold_low:
            plt.plot(x[i], RSIs[i], color='green', marker='D', markersize=3)
        else:
            plt.plot(x[i], RSIs[i], color='red', marker='D', markersize=3)

    plt.plot(x, RSIs, color='gray', linestyle='--', linewidth=1)  # 连接点的线
    plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0)
    plt.show()

# code = "015210"
# num = 25
# series_list,x = get_list(code,num,"2024-05-20")
# RSI = get_rsi(series_list,num)
# x.reverse()
# show_pic(code,x,RSI)
