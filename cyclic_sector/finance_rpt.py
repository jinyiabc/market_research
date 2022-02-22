import numpy as np
import pandas as pd
from helper.Loader import Loader

from helper.get_data import pivot_table_all

from src.helper.WSDLoader import WSDLoader

if __name__ == '__main__':
    database = 'market_research'
    table_name = 'finance_rpt'
    start_date = "2000-01-01"
    end_date = "2022-02-20"

    """
    """
    wind_codes = pd.read_csv('cyclic_sector/beer.txt',sep=' ', header=None,)
    wind_codes = wind_codes[0].to_list()
    # wind_codes = ["600519.SH"]
    field_growth =  "windcode,yoyeps_basic,yoyeps_diluted,yoyocfps,yoy_tr,yoy_or,yoyop,yoyop2,yoyebt,yoyprofit,yoynetprofit,yoynetprofit_deducted,dp_yoy,yoyroe,yoyocf,maintenance,yoy_cash,yoy_fixedassets,fa_rdexp_yoy,yoy_equity,yoycf,yoydebt,yoy_assets"
    field_profit = "roe_avg,roe_basic,roe_diluted,roe_deducted,roe_exbasic,roe_exdiluted,roe_add,roa2,roa,roic,ROP,roe_yearly,roa2_yearly,roa_yearly,netprofitmargin,netprofitmargin_deducted,grossprofitmargin,cogstosales,nptocostexpense,expensetosales,optoebt,profittogr,optogr,ebittogr,gctogr,operateexpensetogr,adminexpensetogr,finaexpensetogr,impairtoOP,ebitdatosales"
    options = "rptType=1;Period=Q;Days=Alldays;Currency=CNY"
    field = field_growth + "," + field_profit
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

