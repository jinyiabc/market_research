from helper import mysql_dbconnection, config
from data_prep import WSDLoader


def main(start_date, end_date):
    """
    The main function
    :param start_date: str, set the start date, format: YYYYMMDD
    :param end_date: str，set the end date, format: YYYYMMDD
    :return: None
    """
    # The demonstration uses SQLite as an example. If you need to use another database, please refer to the documentation of sqlalchemy
    # db_engine = create_engine('sqlite:///example.db')
    db_engine = mysql_dbconnection(database=config['database'])
    loader = WSDLoader(start_date, end_date, db_engine,table_name)

    wind_codes = loader.get_windcodes()

    if type(wind_codes) is not int:
        loader.fetch_historical_data(wind_codes)
    else:
        print('ErrorCode:', wind_codes)


if __name__ == '__main__':
    start = '20140101'
    end = '20151231'
    config['database'] = 'test1'
    table_name = 'test_wsd'
    main(start, end)

    # data = WSDLoader.fetchall_data('002500.SZ')
    # print(data)
    # WSDLoader.fetchall_log()