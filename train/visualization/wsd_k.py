from WindPy import *
import numpy as np
import pandas as pd
import talib as ta
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import datetime
from matplotlib.dates import date2num

def mkt_plot(quotes, field, sec): # quotes:行情数据-Dateframe类型 sec：标题

    fig = plt.figure(figsize=(11,5))

    ax1 = fig.add_axes([0, 1, 1, 1])
    ax1.set_title(sec, fontsize=15)

    ax1.grid(True, axis='y')
    ax1.set_xlim(-1, len(quotes)+1)

    for i in range(len(quotes)):
        close_price,open_price = quotes['CLOSE'].iloc[i], quotes['OPEN'].iloc[i]
        high_price, low_price = quotes['HIGH'].iloc[i], quotes['LOW'].iloc[i]
        trade_date = quotes.index[i]
        if close_price > open_price:#画阳线
            ax1.add_patch(patches.Rectangle((i-0.2, open_price), 0.4, close_price-open_price, fill=False, color='r'))
            ax1.plot([i, i], [low_price, open_price], 'r')
            ax1.plot([i, i], [close_price, high_price], 'r')
        else:#画阴线
            ax1.add_patch(patches.Rectangle((i-0.2, open_price), 0.4, close_price-open_price, color='g'))
            ax1.plot([i, i], [low_price, high_price], color='g')
    ax1.set_ylabel("Price", fontsize=15)
    ax1.set_xlabel("Date", fontsize=15)
    #设置x轴标签
    ax1.set_xticks(range(0,len(quotes),5))#位置
    ax1.set_xticklabels([(quotes.index[i]).strftime('%Y-%m-%d') for i in ax1.get_xticks()] , rotation=20)#标签内容

    ax2 = ax1.twinx()
    ax2.plot(range(len(quotes)), quotes[field.upper()])
    ax2.set_ylabel(field.capitalize(), fontsize=15)

    return fig

w.start()
errorcode, data = w.wsd(
    "600028.SH",
    "open,high,low,close,volume","ED-1M" ,
    (datetime.date.today()-datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
    "Fill=Previous",
    usedf=True
)
print(data)
# mkt_plot(data, 'volume', '600028')
# plt.show()