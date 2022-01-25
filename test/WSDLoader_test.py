import argparse
import sys

from helper.WSDLoader import WSDLoader



def main(start_date, end_date):
    """
    The main function
    :param start_date: str, set the start date, format: YYYYMMDD
    :param end_date: str，set the end date, format: YYYYMMDD
    :return: None
    """
    # The demonstration uses SQLite as an example. If you need to use another database, please refer to the documentation of sqlalchemy
    # db_engine = create_engine('sqlite:///example.db')
    # db_engine = mysql_dbconnection(database=database)
    loader = WSDLoader(start_date, end_date, database, table_name, field, options)

    # print(loader.current_time) # check for parent property

    wind_codes = loader.get_windcodes(sector=sector)
    if type(wind_codes) is not int:
        loader.fetch_historical_data(wind_codes)
    else:
        print('ErrorCode:', wind_codes)


if __name__ == '__main__':
    start = '20211231'
    end = '20211231'
    database = 'test1'
    table_name = 'test_wsd4'
    field = "trade_code,close,windcode"
    options = "PriceAdj=B"
    sector = '000300.SH'
    # main(start, end)

    loader = WSDLoader(start, end, database, table_name, field, options)
    data = loader.fetchall_data(wind_code='002460.SZ')
    print(data)
    # WSDLoader.fetchall_log()

    # command usage:
    # wsd -s "20211231" -e "20211231" -d test1 -t test_wsd3