import matplotlib.pyplot as plt
import mplcursors

# 示例数据
x = [1, 2, 3, 4, 5]
ks = [10, 20, 30, 40, 50]
ds = [15, 25, 35, 45, 55]
js = [20, 30, 40, 50, 60]

code = "股票代码"

plt.figure(figsize=(15, 4))  # 设置宽为1500px,高为400px
plt.title(str(code))

# 绘制 k 线
line_k, = plt.plot(x, ks, color='green', marker='D', markersize=3, label='k')

# 绘制 d 线
line_d, = plt.plot(x, ds, color='purple', marker='D', markersize=3, label='d')

# 绘制 j 线
line_j, = plt.plot(x, js, color='red', marker='D', markersize=3, label='j')

plt.xlabel('time')
plt.ylabel('KDJ')
plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0)

# 添加数据光标
cursor_k = mplcursors.cursor(line_k, hover=True)
@cursor_k.connect("add")
def on_add_k(sel):
   x_val = sel.target[0]
   k_val = sel.target[1]
   d_val = ds[x.index(x_val)]
   j_val = js[x.index(x_val)]
   sel.annotation.set_text(f"x={x_val:.2f}\nk={k_val:.2f}\nd={d_val:.2f}\nj={j_val:.2f}")
   sel.annotation.set_position((0.95, 0.05), coords="axes fraction")

cursor_d = mplcursors.cursor(line_d, hover=True)
@cursor_d.connect("add")
def on_add_d(sel):
   x_val = sel.target[0]
   d_val = sel.target[1]
   k_val = ks[x.index(x_val)]
   j_val = js[x.index(x_val)]
   sel.annotation.set_text(f"x={x_val:.2f}\nk={k_val:.2f}\nd={d_val:.2f}\nj={j_val:.2f}")
   sel.annotation.set_position((0.95, 0.05), coords="axes fraction")

cursor_j = mplcursors.cursor(line_j, hover=True)
@cursor_j.connect("add")
def on_add_j(sel):
   x_val = sel.target[0]
   j_val = sel.target[1]
   k_val = ks[x.index(x_val)]
   d_val = ds[x.index(x_val)]
   sel.annotation.set_text(f"x={x_val:.2f}\nk={k_val:.2f}\nd={d_val:.2f}\nj={j_val:.2f}")
   sel.annotation.set_position((0.95, 0.05), coords="axes fraction")

plt.show()
