# -*- coding:utf-8 -*-
# Author:OpenAPISupport@wind.com.cn
# Editdate:2017-11-08

from WindPy import *
import time

w.start()


class wupf_position(object):

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

        # 设置期初组合现金
        wupfCash = w.wupf(PortfoName, beginDate, "CNY", originalCaptial, "1",
                          "Direction=Short;Method=BuySell;CreditTrading=No;Owner=" + windAccount + ";type=flow")

        if wupfCash.ErrorCode != 0:
            self.throwError(wupfCash.Data[0][0])
        time.sleep(0.5)

        holdFlag = 1

        for i in range(len(ma10.Data[0])):

            # 10日均线与30日均线黄金交叉且30日均线向上运行, 持有
            if i > 0 and holdFlag == 1 and (
                    ma10.Data[0][i - 1] < ma30.Data[0][i - 1] and ma10.Data[0][i] > ma30.Data[0][i] and ma30.Data[0][
                i - 1] < ma30.Data[0][i]):

                holdFlag = 0

                selectCash = w.wpd(PortfoName, "Cash", closePrice.Times[i].strftime("%Y%m%d"),
                                   closePrice.Times[i].strftime("%Y%m%d"), "view=PMS")
                time.sleep(0.5)

                if selectCash.ErrorCode != 0:
                    self.throwError(selectCash.Data[0][0])

                currentCaptial = selectCash.Data[0][0] - 100 * closePrice.Data[0][i]

                wupfHolding = w.wupf(PortfoName, closePrice.Times[i].strftime("%Y%m%d"), windCode + ",CNY",
                                     "100," + str(currentCaptial), str(closePrice.Data[0][i]) + ",1",
                                     "Owner=" + windAccount + ";Direction=Long,Long;CreditTrading=No,No;HedgeType=Spec,Spec;")
                time.sleep(0.5)

                if wupfHolding.ErrorCode != 0:
                    self.throwError(wupfHolding.Data[0][0])

                print(closePrice.Times[i].strftime("%Y%m%d") + "_holdSecurity")
            elif i > 0 and holdFlag == 0 and (
                    ma10.Data[0][i - 1] > ma30.Data[0][i - 1] and ma10.Data[0][i] < ma30.Data[0][i]):

                holdFlag = 1

                selectCash = w.wpd(PortfoName, "Cash", closePrice.Times[i].strftime("%Y%m%d"),
                                   closePrice.Times[i].strftime("%Y%m%d"), "view=PMS")
                time.sleep(0.5)
                if selectCash.ErrorCode != 0:
                    self.throwError(selectCash.Data[0][0])

                currentCaptial = selectCash.Data[0][0] + 100 * closePrice.Data[0][i]

                wupfHolding = w.wupf(PortfoName, closePrice.Times[i].strftime("%Y%m%d"), "CNY", str(currentCaptial),
                                     "1", "Owner=" + windAccount + ";Direction=Long;CreditTrading=No;HedgeType=Spec;")
                time.sleep(0.5)

                if wupfHolding.ErrorCode != 0:
                    self.throwError(wupfHolding.Data[0][0])

                print(closePrice.Times[i].strftime("%Y%m%d") + "_holdCNY")

    # 重置回测组合
    def reloadPortfo(self, PortfoName, windAccount):
        result = w.wupf(PortfoName, "", "", "", "", "Owner=" + windAccount + ";reset=true")
        time.sleep(0.5)
        return result

    # 抛出错误信息
    def throwError(self, Message):
        raise Exception(Message)


if __name__ == "__main__":
    wupf_position("PMStest1", "W1191366008", "300008.SZ", "10000", "20150101", "20171031")