import pandas as pd
from WindPy import w

# 命令如何写可以用命令生成器来辅助完成
# 定义打印输出函数，用来展示数据使用
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
    print('\n\n' + '-----通过wsi来取日内分钟数据-----' + '\n')
    error_code, wsi_data = w.wsi("000665.SZ", "close,EXPMA", "2022-01-12 09:00:00", "2022-01-12 16:16:02", "EXPMA_N=20", usedf=True)
    # printpy(wsidata)

    if error_code == 0:
        # print(wsi_data)
        wsi_data.to_csv('sample.csv')
    else:
        print("Error Code:", error_code)
        print("Error Message:", wsi_data.iloc[0, 0])


    w.stop() # 当需要停止WindPy时，可以使用该命令
              # 注： w.start不重复启动，若需要改变参数，如超时时间，用户可以使用w.stop命令先停止后再启动。
              # 退出时，会自动执行w.stop()，一般用户并不需要执行w.stop
