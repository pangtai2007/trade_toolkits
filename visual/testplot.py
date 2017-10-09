import pandas as pd
import matplotlib.pyplot as plt
import time

df = pd.read_csv('../data/kline_20170714.csv')
#print(df)
#print(df['open'][0])
#shijian
'''
timestamp=1462451334

time_local = time.localtime(timestamp)
dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
print(time_local)
print(dt)
c=1499956320000000000
d=c/1000000000
print(d)
'''
WIDTH1=0.01
WIDTH2=0.001
STARTX=0.1

fig = plt.figure()
plt.ylim((4890, 4985))
ax = fig.add_subplot(1,1,1)

for i in range(0,10):
    if(df['open'][i]<df['close'][i]):
        rect1 = plt.Rectangle((STARTX, df['open'][i]), WIDTH1, df['close'][i]-df['open'][i], color='r')
        flag=1
    else:
        rect1 = plt.Rectangle((STARTX, df['open'][i]), WIDTH1, df['open'][i]-df['close'][i], color='g')
        flag=0
    if(flag==1):
        rect2 = plt.Rectangle((STARTX+WIDTH1/2-WIDTH2/2, df['low'][i]), WIDTH2, df['high'][i] - df['low'][i], color='r')
    else:
        rect2 = plt.Rectangle((STARTX + WIDTH1 / 2 - WIDTH2 / 2, df['low'][i]), WIDTH2, df['high'][i] - df['low'][i],
                              color='g')
    STARTX +=0.1
    ax.add_patch(rect1)
    ax.add_patch(rect2)


plt.show()
