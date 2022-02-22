import numpy as np
import pandas as pd
from helper.Loader import Loader

from helper.get_data import pivot_table_all

if __name__ == '__main__':
    database = 'market_research'
    table_name = 'ohlc'
    start_date = "2012-01-01"
    end_date = "2022-01-26"

    """
    """
    wind_codes = pd.read_csv('cyclic_sector/basic_material.txt',sep=' ', header=None,)
    wind_codes = wind_codes[0].to_list()
    field = "symbol,date,close"
    # options = "PriceAdj=DP"
    loader = Loader(start_date, end_date, database, table_name, field, None)
    df = loader.fetch_data(database, table_name, wind_codes, field)
    df.head()
    table = pivot_table_all(df, 'date', 'symbol', 'close')
    print(table)

    df0 = table['000629.SZ']
    df0 = df0.to_frame(name='000629.SZ')
    df0['Time'] = np.arange(len(df0.index))

    df0.head()

    import matplotlib.pyplot as plt
    import seaborn as sns

    plt.style.use("seaborn-whitegrid")
    plt.rc(
        "figure",
        autolayout=True,
        figsize=(11, 4),
        titlesize=18,
        titleweight='bold',
    )
    plt.rc(
        "axes",
        labelweight="bold",
        labelsize="large",
        titleweight="bold",
        titlesize=16,
        titlepad=10,
    )

    fig, ax = plt.subplots()
    ax.plot('Time', '000629.SZ', data=df0, color='0.75')
    ax = sns.regplot(x='Time', y='000629.SZ', data=df0, ci=None, scatter_kws=dict(color='0.25'))
    ax.set_title('Time Plot of Hardcover Sales');
