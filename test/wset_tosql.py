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
    print('\n\n' + '-----获取申万一级行业的成分股-----' + '\n')
    # 获取申万一级行业的成分股
    print('\n\n' + '-----通过wset来取数据集数据,获取沪深300指数权重-----' + '\n')
    sector = '000300.SH'
    # date = '2021-12-22'
    # ErrorCode, wsetdata = w.wset("IndexConstituent", f"date={date};windcode={sector};field=date,wind_code,i_weight",usedf = True)
    ErrCode, wsetdata = w.wset("indexhistory","startdate=2010-12-15;enddate=2022-01-15;windcode=000300.SH", usedf = True)
    print(wsetdata['tradedate'])
    datelist = wsetdata['tradedate'].drop_duplicates().to_list()

    dbConnection = mysql_dbconnection(database='china_stock_wiki')
    tableName = '000300_SH'.lower()
    for i, value in enumerate(datelist):
        ErrorCode, wsetdata = w.wset("IndexConstituent", f"date={str(value.date())};windcode={sector};field=date,wind_code,i_weight",
                                     usedf=True)

        '''
        How to behave if the table already exists.
            fail: Raise a ValueError.
            replace: Drop the table before inserting new values.
            append: Insert new values to the existing table.
        '''
        wsetdata.set_index('wind_code', inplace=True)
        try:

            frame = wsetdata.to_sql(tableName, dbConnection, if_exists='append');

        except Exception as ex:

            print(ex)

        else:

            print("Table %s created successfully." % tableName);

        finally:

            dbConnection.close()
        pass


    w.stop() # 当需要停止WindPy时，可以使用该命令
              # 注： w.start不重复启动，若需要改变参数，如超时时间，用户可以使用w.stop命令先停止后再启动。
              # 退出时，会自动执行w.stop()，一般用户并不需要执行w.stop
