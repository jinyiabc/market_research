import pandas as pd

# 命令如何写可以用命令生成器来辅助完成
# 定义打印输出函数，用来展示数据使用
from matplotlib import pyplot as plt

from helper.mysql_dbconnection import mysql_dbconnection


def compare_bond_stock(dataframe, bond=None, stock=None, price=None, start=None, end=None):
    """
    bond: 可转债代码
    stock: 正股代码
    price: 转股价格
    1. 转股价值
    转股价值 = 100 / 转股价 x 正股现价
    2. 溢价率
    溢价率 =（转债现价 - 转股价值）/ 转股价值
    3. 标准券折算率
    标准券折算率=中登公布的标准券折算率/转债现价
    """
    df_bond = dataframe[dataframe["windcode"] == bond]
    df_stock = dataframe[dataframe["windcode"] == stock]
    # 计算股票溢价率
    # df127007 = df127007.join(df000665['close']* (100 / 5.58), rsuffix='_other')
    df_bond = df_bond.set_index('index').join(df_stock.set_index('index')['close'] * (100 / price),
                                              rsuffix='_other').rename(columns={'close_other': 'bond_stock_value'})
    df_bond['BSRatio'] = df_bond['close'] / df_bond['bond_stock_value'] - 1

    print(df_bond['2022-01-17':'2022-01-20'])
    if start is not None and end is not None:
        return df_bond[start:end]
    return df_bond


if __name__ == '__main__':
    # 1st method

    # Get data from mysql,
    dbConnection = mysql_dbconnection('china_stock_wiki')
    dataframe = pd.read_sql("select * from `0120`", dbConnection);
    pd.set_option('display.expand_frame_repr', False)
    # print(frame)

    dbConnection.close()

    """
    127007.SZ = 湖广转债
    000665.SZ = 湖北广电
    113017.SH  = 吉视转债  
    601929.SH  = 吉视传媒                
    """
    keyargment = {'bond':"127007.SZ", 'stock':"000665.SZ", 'price':5.58}
    # keyargment = {'bond':"113017.SH", 'stock':"601929.SH", 'price':2.23}
    # start = '2022-01-17'
    # end = '2022-01-20'
    # df_bond = compare_bond_stock(df,start=None, end=None, **keyargment)
    dataframe.set_index('index',inplace=True)
    df_bond = dataframe[dataframe["wind_code"] == keyargment['bond']]
    df_stock = dataframe[dataframe["wind_code"] == keyargment['stock']]
    # print(df_bond)
    # print(df_stock)

    # Plot AMT
    plt.figure(figsize=(15,10))
    plt.plot(df_bond['AMT'], 'b--',label="Bond Amount")
    plt.plot(df_stock['AMT'], 'r--', label="Stock Amount")
    plt.title("Bond VS Stock trade amount")
    plt.axhline(y=0,)
    plt.legend()
    plt.show()

    # Plot Turn rate
    plt.figure(figsize=(15,10))
    plt.plot(df_bond['TURN'], 'b--',label="Bond TURN")
    plt.plot(df_stock['TURN'], 'r--', label="Stock TURN")
    plt.title("Bond VS Stock Turn percentage 1214-0120")
    # plt.axhline(y=130,)
    plt.legend()
    plt.show()

    # # Convertible value = bond - bond_stock_value
    # plt.figure(figsize=(30,10))
    # plt.plot(df_bond['close']-df_bond['bond_stock_value'], 'y--', label="Convertible value")
    # plt.title("Convertible value 1214-0120")
    # plt.axhline(y=0,)
    # plt.legend()
    # plt.show()
