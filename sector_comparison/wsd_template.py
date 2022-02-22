
from helper.get_data import get_data_sql

if __name__ == '__main__':

    wind_codes = ['600959.SH',
                '000156.SZ',
                '300770.SZ',
                '000665.SZ',
                '600037.SH',
                '601929.SH',
                '000839.SZ',
                '000917.SZ',
                '600996.SH',
                '002238.SZ',]

    # 1. Parameter Preparation.
    start = "2019-01-21"
    end = "2022-01-20"
    field = "trade_code,close,windcode"
    options = "PriceAdj=B"
    database = 'test1'
    table_name = 'test_wsd5'

    # 2. Download tikcer data from WIND.
    # print('\n\n' + '-----通过wsd来取获取数据-----' + '\n')
    # loader = WSDLoader(start, end, database, table_name, field, options)
    # loader.fetch_historical_data(wind_codes)

    # 3. Get data with ticker columned by close price.
    data = get_data_sql(wind_codes, start, end, database, table_name, field, options)
    print(data)
