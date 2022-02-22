import numpy as np
import pandas as pd
from helper.Loader import Loader
from helper.WSDLoader import WSDLoader
from WindPy import w
from helper.get_data import get_data_sql, pivot_table_all

if __name__ == '__main__':
    database = 'bond'
    table_name = 'convertible_bond'
    start_date = "2022-01-04"
    end_date = "2022-01-26"

    """
    GET WIND CODES TO INVESTIGATE
    """
    # w.start()
    # wind_codes = w.wset("sectorconstituent","date=2022-01-26;sectorid=61efa6df695d4c9354451c77.U").Data[1]
    # wind_codes = ["110038.SH", "110043.SH"]
    # wind_codes = ["110038.SH"]
    """
    GET BOND DATA
    """
    # field = "windcode,underlyingcode,underlyingname,pct_chg,volume,turn,convpremiumratio,strbvalue,strbpremiumratio,convprice,convratio,convvalue,diluterate,outstandingbalance,conditionalcallprice,maturitycallprice,conditionalputprice,day,ptmyear,latestissurercreditrating2,rate_ratebond"
    # options =  "ratingAgency=101;type=1;PriceAdj=DP"
    # loader = WSDLoader(start_date, end_date, database, table_name, field, options)
    # loader.fetch_historical_data(wind_codes, UPLOAD_GITHUB=True)

    """
    GET STOCK DATA
    """

    # # GET UNDERLYING WINDCODES OF BOND.
    # loader = Loader(start_date, end_date, database, table_name, None, None)
    # field = "windcode, underlyingcode, pct_chg, convprice"
    # data = loader.fetchall_data(wind_codes, field)
    # underlyingcodes = data['UNDERLYINGCODE'].drop_duplicates().to_list()
    #
    # # GET DATA FROM WINDAPI
    # _stock_table_name = 'underlying_stock'
    # field = "windcode,sec_name,pre_close,open,high,low,close,volume,turn,adjfactor,exch_eng,trade_code,cbname,cbwindcode"
    # options = ""
    # loader = WSDLoader(start_date, end_date, database, _stock_table_name, field, options)
    # loader.fetch_historical_data(underlyingcodes, UPLOAD_GITHUB=True)

    """
    PREPARE DATA TO ANALYSIS
    """
    loader = Loader(start_date, end_date, database, None, None, None)
    field = "windcode, CONVVALUE, convpremiumratio"
    bond_data = loader.fetchall_data('convertible_bond', field)
    bond_data['CLOSE'] = bond_data["CONVVALUE"] * (1 + bond_data["CONVPREMIUMRATIO"] / 100)
    # bond_data.to_csv('resource/bond_data.csv')
    prices_bond = pivot_table_all(bond_data, ['index'], ['WINDCODE'], ['CLOSE'])

    field = "windcode,close"
    stock_data = loader.fetchall_data('underlying_stock', field)
    prices_stock = pivot_table_all(stock_data, ['index'], ['WINDCODE'], ['CLOSE'])

    """
    ANALYZE THROUGH PYPFOPT.
    """
    import pypfopt
    from pypfopt import risk_models, expected_returns
    from pypfopt import plotting

    mu = expected_returns.capm_return(prices_stock)
    S = risk_models.semicovariance(prices_stock)

    mu.plot.barh(figsize=(10, 5));