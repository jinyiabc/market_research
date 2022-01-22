from WindPy import w
from data_prep import WSETLoader
from helper import config, mysql_dbconnection

if __name__ == '__main__':
    w.start()
    w.isconnected()  # 判断WindPy是否已经登录成功
    sector = '000300.SH'
    start = '20220121'
    end = '20220121'
    config['database'] = 'test1'
    table_name = 'test_wset'

    db_engine = mysql_dbconnection(database=config['database'])
    loader = WSETLoader(start, end, db_engine, table_name, sector)
    # loader.fetch_historical_data(UPLOAD_GITHUB=True)

    loader.upload_csv()
    # data = loader.fetchall_data('601989.SH', table_name)
    # print(data)
    # w.stop()