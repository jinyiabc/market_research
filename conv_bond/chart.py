from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

dateparse  = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

df = pd.read_csv('../resource/300072-1.csv',
                 parse_dates=['Unnamed: 0'],
                 date_parser=dateparse,
                 # index_col=['Unnamed: 0'],
                 ).rename(columns={'Unnamed: 0': 'datetime'})
df.fillna(method='ffill', inplace=True)
print(df)
period1= 50
period2=100
period3=20

df["SMA1"] = df['close'].rolling(window=period1,min_periods=50).mean()
df["SMA2"] = df['close'].rolling(window=period2).mean()
df['ewma'] = df['close'].ewm(span=period3, min_periods=period3).mean()
df['middle_band'] = df['close'].rolling(window=period3).mean()
df['upper_band'] = df['close'].rolling(window=period3).mean() + df['close'].rolling(window=period3).std()*2
df['lower_band'] = df['close'].rolling(window=period3).mean() - df['close'].rolling(window=period3).std()*2

plt.figure(figsize=(30,10))
plt.plot(df['SMA1'], 'g--', label="SMA1-50min")
plt.plot(df['SMA2'], 'r--', label="SMA-100min")
plt.plot(df['ewma'], 'y--', label="ewma-20min")
plt.plot(df['close'], 'b--',label="close")
plt.axvline(x=240)
plt.text(230,8,'12/14',rotation=90)
plt.axvline(x=480)
plt.text(470,8,'12/15',rotation=90)
plt.axvline(x=720)
plt.text(710,8,'12/16',rotation=90)
plt.axvline(x=960)
plt.text(950,8,'12/17',rotation=90)
plt.axvline(x=1200)
plt.text(1190,8,'12/21',rotation=90)
plt.axvline(x=1440)
plt.text(1430,8,'12/22',rotation=90)
plt.title("Simple Moving Average and Exponential Moving Average 12/14/21 - 12/22/21")
# fig1, ax1 = plt.subplots()
# ax2 = ax1.twinx()
# N = df.shape[0]
# x = np.arange(N)
# y1 = df['close'].values
# # y2 = y1.copy()
# y2= df['volume'].values + 2000
# y2 = y2/(np.max(y2)-np.min(y2))
# ax1.plot(x, y1, label='Price', c='g')
# ax2.plot(x, df['volume'], label='Volume', c='r')
plt.legend()
plt.show()

plt.figure(figsize=(30,10))
plt.plot(df['upper_band'], 'g--', label="upper")
plt.plot(df['middle_band'], 'r--', label="middle")
plt.plot(df['lower_band'], 'y--', label="lower")
plt.plot(df['close'], label="close")
plt.axvline(x=240)
plt.text(230,8,'12/14',rotation=90)
plt.axvline(x=480)
plt.text(470,8,'12/15',rotation=90)
plt.axvline(x=720)
plt.text(710,8,'12/16',rotation=90)
plt.axvline(x=960)
plt.text(950,8,'12/17',rotation=90)
plt.axvline(x=1200)
plt.text(1190,8,'12/21',rotation=90)
plt.axvline(x=1440)
plt.text(1430,8,'12/22',rotation=90)
plt.title("Bollinger Bands 12/14/21 - 12/22/21")
plt.legend()
plt.show()

# from mpl_toolkits.axes_grid1 import host_subplot
# import mpl_toolkits.axisartist as AA
# import matplotlib.pyplot as plt

# host = host_subplot(111, axes_class=AA.Axes)
# plt.subplots_adjust(right=0.75)
#
# par1 = host.twinx()
# par2 = host.twinx()
#
# offset = 60
# new_fixed_axis = par2.get_grid_helper().new_fixed_axis
# par2.axis["right"] = new_fixed_axis(loc="right", axes=par2,
#                                         offset=(offset, 0))
#
# par2.axis["right"].toggle(all=True)
#
# host.set_xlim(0, 2)
# host.set_ylim(0, 2)
#
# host.set_xlabel("datetime")
# host.set_ylabel("price")
# par1.set_ylabel("volume")
# # par2.set_ylabel("Velocity")
#
# p1, = host.plot(np.arange(df.shape[0]), df['close'].values, label="price")
# p2, = par1.plot(np.arange(df.shape[0]), df['volume'].values, label="volume")
# # p3, = par2.plot(np.arange(df.shape[0]), [50, 30, 15], label="Velocity")
#
# par1.set_ylim(0, 4)
# par2.set_ylim(1, 65)
#
# host.legend()
#
# host.axis["left"].label.set_color(p1.get_color())
# par1.axis["right"].label.set_color(p2.get_color())
# # par2.axis["right"].label.set_color(p3.get_color())
#
# plt.draw()
# plt.show()