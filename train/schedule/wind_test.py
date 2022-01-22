from WindPy import w
import time
import os

def start():
    start_data = w.start()
    print()
    if start_data.ErrorCode == 0:
      print("Wind API started successfully")
    else:
      print("Error message:")
      print(start_data)

    time.sleep(5)

    data = w.wss("600000.SH", "sec_name,bsharename,sec_englishname,exchange_cn,exch_eng")
    time.sleep(5)
    print()
    if data.ErrorCode == 0:
      print("WSS ran successfully")
      print("The data is:")
      print(data)
    else:
      print("WSS failed to run")
      print("Error message:")
      print(data)
    w.stop()
    os.system('PAUSE')


if __name__ == '__main__':
    start()
