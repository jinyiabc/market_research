from WindPy import *
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pylab as plt

w.start()

errorcode, df = w.wsd("002739.SZ",
                      "close",
                      "2016-05-17", "2020-05-18",
                      "TradingCalendar=SZSE;Fill=Previous",
                      usedf=True)

plt.figure(figsize=(10, 7))
df['CLOSE'].plot()
plt.ylabel('Price', fontsize=14)
plt.xlabel('Date', fontsize=14)
plt.show()
