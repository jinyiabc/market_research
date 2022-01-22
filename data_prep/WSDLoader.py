import time

import mysql.connector
import pandas as pd
from WindPy import w
from helper import config, mysql_dbconnection, upload_github

class WSDLoader:

    def __init__(self, start_date, end_date, db_engine, table_name):
        self._start_date = start_date
        self._end_date = end_date
        self._db_engine = db_engine
        self._table_name = table_name

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
        table_name = self._table_name

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
                data.to_sql(table_name, db_engine, if_exists='append')
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
    def fetchall_data(wind_code, table_name):
        """
        Fetch data from SQLite database
        :param str, wind_code:
        :return: None
        """
        db_engine = mysql_dbconnection(config['database'])
        query = ("SELECT * FROM " + table_name + " "
                 "WHERE wind_code ='" + wind_code + "'")

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

    def upload_csv(self):
        table_name = self._table_name
        file_path = f'resource/{table_name}.csv'
        upload_github(file_path)
