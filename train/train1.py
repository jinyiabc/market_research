# 本案例仅作参考，目的在于帮助WindPy的用户熟悉WindPy接口的使用方法。用户需根据实际需求自行编写、测试脚本
# 以下将演示如何下载沪深300成分股的历史数据并存入数据库
import time

import pandas as pd
from WindPy import w
from helper.mysql_dbconnection import mysql_dbconnection
import mysql.connector
from helper.configSQL import config

class WSDLoader:

    def __init__(self, start_date, end_date, db_engine):
        self._start_date = start_date
        self._end_date = end_date
        self._db_engine = db_engine

    @property
    def current_time(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    def __error_logger(self, wind_code, status, info=None):
        """
        Log the errors occuring when retriving or saving data
        :param wind_code: str, wind code of the present security
        :param status: status parameters, e.g. the ErrorCode returned by Wind API
        :return: None
        """
        error_log = pd.DataFrame(index=[wind_code])
        error_log.loc[wind_code, 'start_date'] = self._start_date
        error_log.loc[wind_code, 'end_date'] = self._end_date
        error_log.loc[wind_code, 'status'] = status
        error_log.loc[wind_code, 'table'] = 'stock_daily_data'
        error_log.loc[
            wind_code, 'args'] = 'Symbol: ' + wind_code + ' From ' + self._start_date + ' To ' + self._end_date
        error_log.loc[wind_code, 'error_info'] = info
        error_log.loc[wind_code, 'created_date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        error_log.to_sql('stock_error_log', self._db_engine, if_exists='append')

    def fetch_historical_data(self, wind_codes, sleep_time=5):
        """
        Retrieve the WSD data of specified windcodes
        :param wind_codes: List[str], the windcodes of specified securities
        :param sleep_time: number, the sleep time for the loop when an error occurs
        :return: None
        """
        print(self.current_time, ": Start to Download A-Share Stocks")
        start_date = self._start_date
        end_date = self._end_date
        db_engine = self._db_engine

        w.start()

        for wind_code in wind_codes:
            print(self.current_time, ": {0}".format(wind_code))
            # The code can be generated using Code Generator. To get data in format DataFrame, add usedf=True in the parameter list
            error_code, data = w.wsd(wind_code,
                                     "windcode,trade_code,open,high,low,close,pre_close,volume,amt",
                                     start_date,
                                     end_date,
                                     usedf=True)
            # Check if Wind API runs successfully. If error_code is not 0, it indicators an error occurs
            if error_code != 0:
                # Output log
                self.__error_logger(wind_code, '{0}'.format(int(error_code)))
                # Print error message
                print(self.current_time, ":data %s : ErrorCode :%s" % (wind_code, error_code))
                print(data)
                # Pause the loop for the specified time when an error occurs
                time.sleep(sleep_time)
                # Skip the present iteration
                continue

            try:
                # Save the data into the database
                data.to_sql('stock_daily_data', db_engine, if_exists='append')
            except Exception as e:
                self.__error_logger(wind_code, None)
                print(self.current_time, ": SQL Exception :%s" % e)

        print(self.current_time, ": Downloading A-Share Stock Finished .")

    def get_windcodes(self, trade_date=None):
        """
        Retrieve the windcodes of CSI300 (沪深300) constituents
        :param trade_date: the date to retrieve the windcodes of the constituents
        :return: Error code or a list of windcodes
        """
        w.start()
        if trade_date is None:
            trade_date = self._end_date
        # Retrieve the windcodes of CSI300 constituents.
        # Users can use Sector Constituents and Index Constituents of WSET to retrieve the constituents of a sector or an index
        stock_codes = w.wset("sectorconstituent", "date=" + trade_date + ";windcode=000300.SH;field=wind_code")
        if stock_codes.ErrorCode != 0:
            # Return the error code when an error occurs
            return stock_codes.ErrorCode
        else:
            # Return a list of windcodes if the data is achieved
            return stock_codes.Data[0]

    @staticmethod
    def fetchall_data(wind_code):
        """
        Fetch data from SQLite database
        :param str, wind_code:
        :return: None
        """
        db_engine = mysql_dbconnection(config['database'])
        query = ("SELECT * FROM stock_daily_data "
                 "WHERE WINDCODE ='" + wind_code + "'")

        data = pd.read_sql(query, db_engine)

        pd.set_option('display.expand_frame_repr', False)

        if len(data) > 0:
            print("Data found!")
        else:
            print("No data found!")
        db_engine.close()

        return data

    @staticmethod
    def fetchall_log():
        """
        Retrieve the error log
        :return: None
        """
        cnx = mysql.connector.connect(**config)
        c = cnx.cursor()
        c.execute("SELECT * FROM stock_error_log")
        for row in c.fetchall():
            # Print error log
            print(row)
        cnx.close()


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
    loader = WSDLoader(start_date, end_date, db_engine)

    wind_codes = loader.get_windcodes()

    if type(wind_codes) is not int:
        loader.fetch_historical_data(wind_codes)
    else:
        print('ErrorCode:', wind_codes)


if __name__ == '__main__':
    start = '20140101'
    end = '20151231'
    config['database'] = 'test1'
    main(start, end)

    # data = WSDLoader.fetchall_data('002500.SZ')
    # print(data)
    # WSDLoader.fetchall_log()