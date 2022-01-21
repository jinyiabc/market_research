from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

dateparse  = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

df1 = pd.read_csv('../resource/300072-2.csv',
                  parse_dates=['Unnamed: 0'],
                  date_parser=dateparse,
                  # index_col=['Unnamed: 0'],
                  ).rename(columns={'Unnamed: 0': 'datetime'})
df1.fillna(method='ffill', inplace=True)
df2 = pd.read_csv('../resource/300144-2.csv',
                  parse_dates=['Unnamed: 0'],
                  date_parser=dateparse,
                  # index_col=['Unnamed: 0'],
                  ).rename(columns={'Unnamed: 0': 'datetime'})
df2.fillna(method='ffill', inplace=True)


from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt

host = host_subplot(111, axes_class=AA.Axes)
plt.subplots_adjust(right=0.75)

par1 = host.twinx()
par2 = host.twinx()

offset = 60
new_fixed_axis = par2.get_grid_helper().new_fixed_axis
par2.axis["right"] = new_fixed_axis(loc="right", axes=par2,
                                        offset=(offset, 0))

par2.axis["right"].toggle(all=True)

host.set_xlim(0, df1.shape[0])
host.set_ylim(0, df1['close'].max())

host.set_xlabel("datetime")
host.set_ylabel("300172")
par1.set_ylabel("300144")
# par2.set_ylabel("Velocity")

p1, = host.plot(np.arange(df1.shape[0]), df1['close'].values, label="300172")
p2, = par1.plot(np.arange(df1.shape[0]), df2['close'].values, label="300144")
# p3, = par2.plot(np.arange(df.shape[0]), [50, 30, 15], label="Velocity")

par1.set_ylim(0, df1['close'].max())
par2.set_ylim(1, df2['close'].max())

host.legend()

host.axis["left"].label.set_color(p1.get_color())
par1.axis["right"].label.set_color(p2.get_color())
# par2.axis["right"].label.set_color(p3.get_color())

plt.draw()
plt.show()