# -*- coding:utf-8 -*-
# Author:OpenAPISupport@wind.com.cn
# Editdate:2017-11-08

from WindPy import *
import random
import time

w.start()

class wupf_weight(object):

    def __init__(self,PortfoName,windAccount,beginDate,endDate):

        reloadResult=self.reloadPortfo(PortfoName,windAccount)
        if reloadResult.ErrorCode!=0:
            self.throwError(reloadResult.Data[0][0])

        self.strategy(PortfoName,windAccount,beginDate,endDate)

    #执行回测策略
    def strategy(self,PortfoName,windAccount,beginDate,endDate):

        #每周最后一个交易日调仓, 获取调仓日期序列
        adjPositionDate=w.tdays(beginDate, endDate, "Period=M")

        for i in range(len(adjPositionDate.Data[0])):

            #周末调仓日前推1个交易日
            adjPositionDateBefore1=w.tdaysoffset(-1, adjPositionDate.Data[0][i].strftime("%Y-%m-%d"), "")

            #调仓日创业板成分及涨跌停状态
            sector=w.wset("sectorconstituent","date="+adjPositionDate.Data[0][i].strftime("%Y-%m-%d")+";sectorid=a001010r00000000;field=wind_code")
            tradeStatus=w.wss(sector.Data[0], "maxupordown", "tradeDate="+adjPositionDateBefore1.Data[0][0].strftime("%Y-%m-%d"))

            #提取涨停品种及振幅
            limitUpCode=[tradeStatus.Codes[j] for j in range(len(tradeStatus.Data[0])) if tradeStatus.Data[0][j]==1]

            if len(limitUpCode)>0:

                limitUpCodeSwing=w.wss(limitUpCode, "swing","tradeDate="+adjPositionDate.Data[0][i].strftime("%Y-%m-%d")+";cycle=D")

                #提取权重调仓品种
                buyableCode=[limitUpCode[j] for j in range(len(limitUpCode)) if limitUpCodeSwing.Data[0][j]>1]
                adjPositionCode=random.sample(buyableCode,min(5,len(buyableCode)))

                #执行权重调仓
                if(len(adjPositionCode)>0):

                    adjPositionClose=w.wss(adjPositionCode, "close","tradeDate="+adjPositionDate.Data[0][i].strftime("%Y-%m-%d")+";priceAdj=U;cycle=D")

                    windCodes=",".join(adjPositionCode)
                    price=",".join([str(k) for k in adjPositionClose.Data[0]])
                    weight=",".join([str(0.6/len(adjPositionCode))]*len(adjPositionCode))

                    w.wupf(PortfoName, adjPositionDate.Data[0][i].strftime("%Y%m%d"), windCodes, weight, price,"Direction=Long;CreditTrading=No;Owner="+windAccount+";type=weight")
                    print (adjPositionDate.Data[0][i].strftime("%Y%m%d"))
                    time.sleep(0.5)

    #重置回测组合
    def reloadPortfo(self,PortfoName,windAccount):
        result=w.wupf(PortfoName, "", "", "", "","Owner="+windAccount+";reset=true")
        time.sleep(0.5)
        return result

    #抛出错误信息
    def throwError(self,Message):
        raise Exception(Message)

if __name__=="__main__":

    wupf_weight("PMStest1", "W1191366008","2016-01-01","2017-11-09")
