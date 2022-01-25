import time

import pandas as pd
from WindPy import w

from helper.WSETLoader import WSETLoader

if __name__ == '__main__':
    w.start()
    w.isconnected()  # 判断WindPy是否已经登录成功
    wind_code = '000300.SH'
    start_date = '20220121'
    end_date = '20220121'
    database = 'test1'
    table_name = 'test_wset4'
    wind_tableName = "IndexConstituent"
    options = "date={0};windcode={1}"
    # "Period=W;Currency=CNY;PriceAdj=B"     # for stock.
     # "Period=W;Fill=Previous;Currency=CNY;PriceAdj=DP")    # for bond
    #  "BarSize=5;PriceAdj=B")   for wsi
    wse_loader = WSETLoader(database, table_name, wind_tableName, options)

    date_range = pd.date_range(start_date, end_date)
    for rpt_date in date_range:
        rpt_date = str(rpt_date.date())   # coonvert to '2021-12-31'
        wse_loader.fetch_historical_data(rpt_date, wind_code)

    # loader.upload_csv()
    # data = loader.fetchall_data('601989.SH', table_name)
    # print(data)
    # w.stop()

    # wse -s "20220121" -e "20220121" -d test1 -t test_wset1 -se '000300.SH' --github