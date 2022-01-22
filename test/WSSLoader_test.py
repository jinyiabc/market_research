from helper import mysql_dbconnection,config
from data_prep import WSSLoader


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
    loader = WSSLoader(start_date, end_date, db_engine, config['table_name'])

    # wind_codes = loader.get_windcodes()

    loader.fetch_historical_data(wind_codes)
    keyarg = {'table_name': config['table_name']}
    set_data_type = (
        "ALTER TABLE {table_name} MODIFY `wind_code` VARCHAR(10);"
    ).format(**keyarg)
    set_primary = (
        "ALTER TABLE {table_name} ADD PRIMARY KEY (`rpt_date`,`wind_code`);"
    ).format(**keyarg)
    with db_engine.connect() as con:
        con.execute(set_data_type)
        con.execute(set_primary)

if __name__ == '__main__':
    start = '20201231'
    end = '20201231'
    wind_codes = "000001.SZ,110034.SH,110055.SH,110071.SH,113565.SH,113584.SH,113605.SH,113620.SH,113634.SH,123056.SZ,123107.SZ,127015.SZ,127045.SZ,127046.SZ,127049.SZ,128017.SZ,128026.SZ,128030.SZ,128036.SZ,128106.SZ,128114.SZ,128119.SZ,128135.SZ,128142.SZ"
    wind_codes = wind_codes.split(sep=',')
    config['database'] = 'test1'
    config['table_name'] = 'wind_energy_cbond'
    main(start, end)

    # data = WSSLoader.fetchall_data('600000.SH')
    # print(data)