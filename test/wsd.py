import pandas as pd
from WindPy import w

# 命令如何写可以用命令生成器来辅助完成
# 定义打印输出函数，用来展示数据使用
from helper.mysql_dbconnection import mysql_dbconnection


def printpy(outdata):
    if outdata.ErrorCode!=0:
        print('error code:'+str(outdata.ErrorCode)+'\n')
        return()
    for i in range(0,len(outdata.Data[0])):
        strTemp=''
        if len(outdata.Times)>1:
            strTemp=str(outdata.Times[i])+' '
        for k in range(0, len(outdata.Fields)):
            strTemp=strTemp+str(outdata.Data[k][i])+' '
        print(strTemp)

if __name__ == '__main__':
    w.start()  # 默认命令超时时间为120秒，如需设置超时时间可以加入waitTime参数，例如waitTime=60,即设置命令超时时间为60秒

    w.isconnected()  # 判断WindPy是否已经登录成功
    # 通过wsi来取日内分钟数据，三年内数据
    print('\n\n' + '-----通过wsd来取获取数据-----' + '\n')

    """
        EXAMPLE: 
        error_code, wsi_data = w.wsi("000665.SZ", "close,EXPMA", "2022-01-11 14:00:00", "2022-01-12 15:30:00", "EXPMA_N=20", usedf=True)
        error_code, wsi_data = w.wsq("300072.SZ,300144.SZ", "rt_time,rt_last", usedf=True)
        error_code, wsi_data = w.wsd(
                    "600519.SH,000858.SZ,000568.SZ,600809.SH,002304.SZ,000799.SZ,600132.SH,000596.SZ,600600.SH,002568.SZ,688660.SH",
                    "val_mv_ARD", "2022-01-18", "2022-01-18", "", usedf=True)
        error_code, wsd_data = w.wsd(wind_code, "close,volume,amt,turn,val_mv_ARD,convpremiumratio", "2021-12-21", "2022-01-20", "unit=1", usedf=True)

    """


    wind_codes = [  '600959.SH',
                    '000156.SZ',
                    '300770.SZ',
                    '000665.SZ',
                    '600037.SH',
                    '601929.SH',
                    '000839.SZ',
                    '000917.SZ',
                    '600996.SH',
                    '002238.SZ',]

    # Create an empty dataframe.
    start = "2019-01-21"
    end = "2022-01-20"
    index = pd.date_range(start,end)
    data = pd.DataFrame(index=index, columns=['sector'])
    data = data.fillna(0)  # with 0s rather than NaNs
    for wind_code in wind_codes:
        error_code, wsd_data = w.wsd(wind_code, "close", start, end, "", usedf=True)
        wsd_data.rename(columns={"CLOSE":wind_code},  inplace=True)
        data = data.join(wsd_data)
        # wsd_data['wind_code'] = wind_code
    # Connect ot mysql.
    dbConnection = mysql_dbconnection(database='china_stock_wiki')
    tableName = '0122'.lower()
    # Write to Mysql
    try:

        frame = data.to_sql(tableName, dbConnection, if_exists='append');

    except Exception as ex:

        print(ex)

    else:

        print("Table %s created successfully." % tableName);

    dbConnection.close()


    w.stop() # 当需要停止WindPy时，可以使用该命令
              # 注： w.start不重复启动，若需要改变参数，如超时时间，用户可以使用w.stop命令先停止后再启动。
              # 退出时，会自动执行w.stop()，一般用户并不需要执行w.stop
