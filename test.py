import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

x = np.array([1,2,3,4,5])
# yoko
xtick= ["2016", "2017", "2018", "2019", "2020"]
# tate
ytick= ["DPS", "EPS", "CFPS", "SPS"]

dps  = [0.55, 0.6, 0.68, 0.75, 0.8]
eps  = [2.08, 2.3, 2.98, 2.97, 3.28]
cfps = [3.01, 3.06, 3.87, 3.73, 4.6]
sps  = [2.08, 10.91, 13.28, 13.99, 15.66]
data = [dps, eps, cfps, sps]

df = pd.DataFrame([dps,eps,cfps,sps], index=ytick, columns=xtick)
print(df)
print("")
print("tate: ", end='')
print(df.index)
print("yoko: ", end='')
print(df.columns)

margin = 0.15
totoal_width = 1 - margin

for i, h in enumerate(data):
    pos = x - totoal_width *( 1- (2*i+1)/len(data) )/2
    plt.bar(pos, h, width = totoal_width/len(data), label=h)

# グラフタイトル
plt.suptitle('FB')

# x軸の数値を置換
plt.xticks(x, xtick)

# labelが指定されていないと表示できない
plt.legend(ytick)

plt.savefig('3-3_c.png')

