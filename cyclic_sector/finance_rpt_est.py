import numpy as np
import pandas as pd
from helper.Loader import Loader

from helper.get_data import pivot_table_all

from src.helper.WSDLoader import WSDLoader

if __name__ == '__main__':
    database = 'market_research'
    table_name = 'finance_rpt_est'
    start_date = "2001-01-01"
    end_date = "2022-02-20"

    """
    """
    wind_codes = pd.read_csv('cyclic_sector/basic_material.txt',sep=' ', header=None,)
    wind_codes = wind_codes[0].to_list()
    # wind_codes = ["600519.SH"]
    options = "year=2021;westPeriod=180;Period=Q;Days=Alldays"
    field = "windcode,west_eps,west_maxeps,west_mineps,west_maxbps,west_minbps,west_medianbps"
    # options = "Period=Q;Currency=CNY;PriceAdj=F"
    loader = WSDLoader(start_date, end_date, database, table_name, field, options)
    loader.fetch_historical_data(wind_codes, UPLOAD_GITHUB=True)

    # df = loader.fetch_data(database, table_name, wind_codes, field)
    # df.head()
    # table = pivot_table_all(df, 'date', 'symbol', 'close')
    # print(table)
    #
    # df0 = table['000629.SZ']
    # df0 = df0.to_frame(name='000629.SZ')
    # df0['Time'] = np.arange(len(df0.index))

    # df0.head()

