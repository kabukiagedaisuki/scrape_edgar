import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# yoko
xtick= ["2016", "2017", "2018", "2019", "2020"]
# tate
ytick= ["DPS", "EPS", "CFPS", "SPS"]

dps  = [0.55, 0.6, 0.68, 0.75, 0.8]
eps  = [2.08, 2.3, 2.98, 2.97, 3.28]
cfps = [3.01, 3.06, 3.87, 3.73, 4.6]
sps  = [2.08, 10.91, 13.28, 13.99, 15.66]
data = [dps, eps, cfps, sps]

df = pd.DataFrame(data, index=ytick, columns=xtick)
print(df)
print("")

margin = 0.15
totoal_width = 1 - margin

x = np.array(list(range(1, len(xtick)+1)))
for i, h in enumerate(data):
    pos = x - totoal_width *( 1- (2*i+1)/len(data) )/2
    plt.bar(pos, h, width=totoal_width/len(data), label=h, zorder=10)

# グラフタイトル
plt.title("FB annual report")
# x軸の数値を置換
plt.xticks([])    #plt.xticks(x, xtick)
# 先頭棒グラフの余白、末尾棒グラフの余白
plt.xlim(0.5, 5.5)
# 補助線
plt.grid(axis='y', c='gainsboro', zorder=9)
# 凡例  ※labelが指定されていないと表示できない
plt.legend(ytick)

plt.table(cellText=data, colLabels=xtick, rowLabels=ytick, loc='bottom')

plt.savefig('3-3_c.png', bbox_inches='tight')

