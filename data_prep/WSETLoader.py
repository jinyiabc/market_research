import time

import mysql.connector
import pandas as pd
from WindPy import w

from helper.upload_github import upload_github
from helper.configSQL import config
from helper.mysql_dbconnection import mysql_dbconnection


class WSETLoader:

    def __init__(self, start_date, end_date, db_engine, table_name, sector=None):
        self._start_date = start_date
        self._end_date = end_date
        self._db_engine = db_engine
        self._table_name = table_name
        self._sector = sector

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
        table_name = self._table_name
        error_log = pd.DataFrame(index=[wind_code])
        error_log.loc[wind_code, 'start_date'] = self._start_date
        error_log.loc[wind_code, 'end_date'] = self._end_date
        error_log.loc[wind_code, 'status'] = status
        error_log.loc[wind_code, 'table'] = table_name
        error_log.loc[
            wind_code, 'args'] = 'Symbol: ' + wind_code + ' From ' + self._start_date + ' To ' + self._end_date
        error_log.loc[wind_code, 'error_info'] = info
        error_log.loc[wind_code, 'created_date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        error_log.to_sql('stock_error_log', self._db_engine, if_exists='append')

    def fetch_historical_data(self, wind_codes=None, sleep_time=5, UPLOAD_GITHUB=False):
        """
        Retrieve the WSET data of specified windcodes
        :param wind_codes: List[str], the windcodes of specified securities
        :param sleep_time: number, the sleep time for the loop when an error occurs
        :return: None
        """
        print(self.current_time, ": Start to Download Data")
        start_date = self._start_date
        end_date = self._end_date
        db_engine = self._db_engine
        table_name =  self._table_name
        sector = self._sector
        # if len(wind_codes) == 1:
        #     wind_code = wind_codes[0]
        w.start()
        w.isconnected()
        dti = pd.date_range(start_date, end_date)
        for rpt_date in dti:
            # for wind_code in wind_codes:
            print(self.current_time, ": {0}".format(sector))
            error_code, data = w.wset("IndexConstituent",
                                         f"date={rpt_date};windcode={sector}",
                                         usedf=True)
            # w.wset("indexconstituent", "date=2022-01-22;windcode=000300.SH")
            # Check if Wind API runs successfully. If error_code is not 0, it indicators an error occurs
            if error_code != 0:
                # Output log
                self.__error_logger(sector, '{0}'.format(int(error_code)))
                # Print error message
                print(self.current_time, ":data %s : ErrorCode :%s" % (sector, error_code))
                print(data)
                # Pause the loop for the specified time when an error occurs
                time.sleep(sleep_time)
                # Skip the present iteration
                continue
            # data.index.rename('wind_code', inplace=True)
            # data['rpt_date'] = rpt_date.date()
            # data.reset_index(inplace=True)

            try:
                # Save the data into the database
                data.to_sql(table_name, db_engine, if_exists='append', index=False)
            except Exception as e:
                self.__error_logger(sector, None)
                print(self.current_time, ": SQL Exception :%s" % e)

            if UPLOAD_GITHUB is True:
                data.to_csv(f'resource/{table_name}.csv', mode='a')
                print(self.current_time, f": Saved {table_name}.CSV.")
            print(self.current_time, ": Downloading Data Finished .")

    def get_windcodes(self, trade_date=None):
        """
        Retrieve the windcodes of CSI300 (沪深300) constituents
        :param trade_date: the date to retrieve the windcodes of the constituents
        :return: Error code or a list of windcodes
        """
        sector = self._sector
        w.start()
        if trade_date is None:
            trade_date = self._end_date
        # Retrieve the windcodes of CSI300 constituents.
        # Users can use Sector Constituents and Index Constituents of WSET to retrieve the constituents of a sector or an index
        stock_codes = w.wset("sectorconstituent", f"date={trade_date};windcode={sector};field=wind_code")
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
