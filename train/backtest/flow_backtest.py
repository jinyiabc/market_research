# -*- coding:utf-8 -*-
# Author:OpenAPISupport@wind.com.cn
# Editdate:2017-11-08

from WindPy import *
import time

w.start()


class wupf_flow(object):

    def __init__(self, PortfoName, windAccount, windCode, originalCaptial, beginDate, endDate):

        reloadResult = self.reloadPortfo(PortfoName, windAccount)
        if reloadResult.ErrorCode != 0:
            self.throwError(reloadResult.Data[0][0])

        self.strategy(windCode, beginDate, endDate, originalCaptial, PortfoName, windAccount)

    # 执行回测策略
    def strategy(self, windCode, beginDate, endDate, originalCaptial, PortfoName, windAccount):

        # 接口获取回测数据
        closePrice = w.wsd(windCode, "close", beginDate, endDate, "Fill=Previous")  # [beginDate,endDate]收盘价
        ma10 = w.wsd(windCode, "MA", beginDate, endDate, "MA_N=10", "PriceAdj=F")  # [beginDate,endDate]5日均线
        ma30 = w.wsd(windCode, "MA", beginDate, endDate, "MA_N=30", "PriceAdj=F")  # [beginDate,endDate]10日均线
        tradeStatus = w.wsd(windCode, "trade_status", beginDate, endDate, "")  # [beginDate,endDate]交易状态

        # 设置期初组合现金
        wupfCash = w.wupf(PortfoName, beginDate, "CNY", originalCaptial, "1",
                          "Direction=Short;Method=BuySell;CreditTrading=No;Owner=" + windAccount + ";type=flow")
        if wupfCash.ErrorCode != 0:
            self.throwError(wupfCash.Data[0][0])
        time.sleep(0.5)

        buyFlag = 1
        for i in range(len(ma10.Data[0])):

            # 10日均线与30日均线黄金交叉且30日均线向上运行, 买入
            if i > 0 and buyFlag == 1 and (
                    ma10.Data[0][i - 1] < ma30.Data[0][i - 1] and ma10.Data[0][i] > ma30.Data[0][i] and ma30.Data[0][
                i - 1] < ma30.Data[0][i]) and tradeStatus.Data[0][i] == u"交易":

                buyFlag = 0

                wupfSecurity = w.wupf("PMStest1", closePrice.Times[i].strftime("%Y%m%d"), windCode, "100",
                                      str(closePrice.Data[0][i]),
                                      "Direction=Long;Method=BuySell;CreditTrading=No;Owner=" + windAccount + ";type=flow")
                time.sleep(0.5)

                if wupfSecurity.ErrorCode != 0:
                    self.throwError(wupfSecurity.Data[0][0])

                print (closePrice.Times[i].strftime("%Y%m%d") + "_buy")

            # 10日均线与30日均线死亡交叉, 卖出
            elif i > 0 and buyFlag == 0 and (ma10.Data[0][i - 1] > ma30.Data[0][i - 1] and ma10.Data[0][i] < ma30.Data[0][i]) and tradeStatus.Data[0][i] == u"交易":

                buyFlag = 1

                wpfPosition = w.wpf("PMStest1", "Position", "view=PMS;date=" + closePrice.Times[i].strftime(
                    "%Y%m%d") + ";sectorcode=101;displaymode=1")
                time.sleep(0.5)

                if wpfPosition.ErrorCode != 0:
                    self.throwError(wpfPosition.Data[0][0])

                wupfSecurity = w.wupf("PMStest1", closePrice.Times[i].strftime("%Y%m%d"), windCode,
                                      "-" + str(wpfPosition.Data[3][0]), str(closePrice.Data[0][i]),
                                      "Direction=Long;Method=BuySell;CreditTrading=No;Owner=" + windAccount + ";type=flow")
                time.sleep(0.5)

                if wupfSecurity.ErrorCode != 0:
                    self.throwError(wupfSecurity.Data[0][0])

                print(closePrice.Times[i].strftime("%Y%m%d") + "_sell")

    # 重置回测组合
    def reloadPortfo(self, PortfoName, windAccount):
        # result = w.wupf(PortfoName, "", "", "", "", "Owner=" + windAccount + ";reset=true")
        result = w.wupf(PortfoName, "", "", "", "","Owner=W1191366008;reset=true")
        time.sleep(0.5)
        return result

    # 抛出错误信息
    def throwError(self, Message):
        raise Exception(Message)


if __name__ == "__main__":
    wupf_flow("PMStest1", "W1191366008", "300008.SZ", "10000", "20150101", "20171031")


