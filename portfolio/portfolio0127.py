import numpy as np
import pandas as pd
from helper.Loader import Loader
from helper.WSDLoader import WSDLoader
from WindPy import w
from helper.get_data import get_data_sql

if __name__ == '__main__':
    database = 'portfolio'
    table_name = 'portfolio0127'
    start_date = "2012-01-01"
    end_date = "2022-01-26"

    """
    GET INDEX300 AND BOND DATA
    """
    wind_codes = "010303.SH,000300.SH",
    field = "close"
    options = "PriceAdj=DP"
    loader = WSDLoader(start_date, end_date, database, table_name, field, options)
    loader.fetch_historical_data(wind_codes, UPLOAD_GITHUB=True)

