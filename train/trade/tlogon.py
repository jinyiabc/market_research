from WindPy import *

from test.helper import config


class trade(object):
    def __init__(self,windAccount):
        # 登录股票模拟账号
        LogonID = w.tlogon("00000011","0",windAccount,config['windPassword'],"SHSZ")
        if LogonID.ErrorCode != 0:
            self.throwError(LogonID.ErrorCode)
        print("Successfully log on WIND account.")
        self.LogonID = LogonID.Data[0][0]

    # 抛出错误信息
    def throwError(self, Message):
        raise Exception(Message)

    def logout(self):
        Logout = w.tlogout(str(self.LogonID), options="")
        print("Successfully log out WIND account.")

if __name__ == "__main__":
    w.start()
    # Wind终端账号为W1191366008的用户终端WTTS模块创建了'W119136600801'股票模拟交易账号，'W119136600802'期货模拟交易账号, 则登录代码为同时登录两个账号
    windAccount = 'M5DDD653601'
    #   初始登入模拟账户
    _trade = trade(windAccount)
    _trade.logout()

