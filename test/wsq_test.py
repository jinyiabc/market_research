from WindPy import w
import os


def myCallback(indata: w.WindData):
    """Callback function for WSQ

    params
    ------
    indata: WindData, accepts the received market quotation data. WindData has the following fields:
              .ErrorCode: error code, if it is 0, the code runs successfully
              .StateCode: state code. No need to process it.
              .RequestID: save the request ID of WSQ request
              .Codes: wind code of the securities
              .Fields: fields for the received data
              .Times: local time rather than the corresponding time for the recieved data
              .Data: market quotation data
    """
    print(indata)
    if indata.ErrorCode!=0:
        print('error code:'+str(indata.ErrorCode)+'\n')
        return()

    global begintime
    lastvalue =""
    for k in range(0,len(indata.Fields)):
        if(indata.Fields[k] == "RT_TIME"):
            begintime = indata.Data[k][0]
        if(indata.Fields[k] == "RT_LAST"):
            lastvalue = str(indata.Data[k][0])

    string = str(begintime) + " " + lastvalue +"\n"
    pf.writelines(string)
    print(string)
    pf.flush()


if __name__ == '__main__':

    start_ret = w.start()


    if start_ret.ErrorCode != 0:
        print("Start failed")
        print("Error Code:", start_ret.ErrorCode)
        print("Error Message:", start_ret.Data[0])
    else:
        # Open a file to write.
        pf = open('../resource/pywsqdataif.data', 'w')
        # Subscribe market quotation data
        wsq_ret = w.wsq("CN.SG","rt_time,rt_last",func=myCallback)

        if wsq_ret.ErrorCode != 0:
            print("Error Code:", wsq_ret.ErrorCode)

        ext = ''
        while ext != 'q':
          ext = input('Enter "q" to exit')

        w.cancelRequest(0)
        pf.close()