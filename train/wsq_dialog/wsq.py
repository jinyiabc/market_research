# -*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSignal as Signal
from WindPy import w

import globaldef

w.start()


class feeder(QThread):

    update_data = Signal(object)

    def run(self):
        w.start()
        secstring = ",".join(globaldef.secID)
        indstring = ",".join(globaldef.indID)
        w.wsq(secstring, indstring, func=self.myCallback)

    def finished(self):
        w.cancelRequest(0)

    def myCallback(self, indata):
        if indata.ErrorCode != 0:
            print('error code:' + str(indata.ErrorCode) + '\n')
            return ()

        for j in range(0, len(indata.Fields)):
            indindex = globaldef.indID.index(indata.Fields[j])
            for k in range(0, len(indata.Codes)):
                if indata.Codes[k] == globaldef.secID[0]:
                    globaldef.gdata[0][indindex] = indata.Data[j][k]
                if indata.Codes[k] == globaldef.secID[1]:
                    globaldef.gdata[1][indindex] = indata.Data[j][k]
                # If many SecIDs are subscribed , use the folloing way to retrieve data:
                # codeindex = globaldef.secID.index(indata.Codes[k])
                # globaldef.gdata[codeindex][indindex] = indata.Data[j][k]
        globaldef.spreadBid = globaldef.gdata[0][2] - globaldef.gdata[1][1]
        globaldef.spreadAsk = globaldef.gdata[0][1] - globaldef.gdata[1][2]
        globaldef.spreadLast = globaldef.gdata[0][5] - globaldef.gdata[1][5]

        if len(globaldef.plotTime) > 100:
            # Save at most 100 recent data to display on the UI
            del globaldef.plotTime[0]
            del globaldef.plotLast[0]
            del globaldef.plotBid[0]
            del globaldef.plotAsk[0]

        globaldef.plotLast.append(globaldef.spreadLast)
        globaldef.plotBid.append(globaldef.spreadBid)
        globaldef.plotAsk.append(globaldef.spreadAsk)
        if len(globaldef.plotTime) == 0:
            globaldef.plotTime.append(0)
        else:
            globaldef.plotTime.append(globaldef.plotTime[-1] + 1)

        self.update_data.emit(globaldef.gdata)

        print("-----------------------------------")
        print(indata)
