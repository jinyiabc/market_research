import pandas as pd

from helper.get_data import get_data_sql

def test_get_data_sql():
    file_path = 'resource/composition.xlsx'
    df0 = pd.read_excel(file_path,
                        converters={
                            "证券代码":str

                        }
                        ).rename(
                                columns={
                                    "证券代码": "ticker",
                                    "个股仓位%": "weights",
                                    "交易市场": "trader"
                                },
    )
    df0['wind_code'] = df0["ticker"] + df0["trader"].apply(lambda x: '.SZ' if x == '深市A股' else '.SH')
    df1 = df0[["wind_code", "weights"]]
    df1['weights'] = df1['weights']/df1['weights'].sum()
    # print(df1)
    # print(df1['percentage'].sum())
    wind_codes = df1['wind_code'].values.tolist()
    start_date = '2011-01-01'
    end_date = '2022-01-24'
    table_name = 'portfolio0124b'
    database = 'test1'
    field = "trade_code,close,windcode"
    options = "PriceAdj=B",

    # Add data to MySQL from wind api.
    # loader.fetch_historical_data(wind_codes,)

    data = get_data_sql(wind_codes, start_date, end_date, database, table_name, field, options)
    print(data)
