import sys
from PyQt5 import QtCore,QtGui,uic,QtWidgets
from WindPy import w
w.start()

qtCreatorFile="sample.ui" # The name of the used UI file
Ui_MainWindow,QtBaseClass = uic.loadUiType(qtCreatorFile)

global accountNumber
accountNumber=0

class MyApp(QtWidgets.QMainWindow,Ui_MainWindow): 
    def __init__(self):
      
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        # Relate events with methods
        self.accountLogin.clicked.connect(self.login)        
        self.torder.clicked.connect(self.torderProcess)      
        self.quit.clicked.connect(self.logout)             

    # Log on with the entered accounts
    def login(self):
        
        global accountNumber
        msg = list()
        for k in range(2):
            accountlabelName="account_label"+str(k)
            print(self.account_label0.text())
            temtText = eval("self."+accountlabelName+".text()")
            if temtText!="":
                windLogin=w.tlogon('0000','0',str(temtText),'123456','SHSZ') 
                print(windLogin)
                if windLogin.ErrorCode == 0:
                    exec('self.LogonID_label'+str(k)+'.setText(str(windLogin.Data[0][0]))')

                # Save ErrorMsg
                if windLogin.ErrorCode == 0:
                    windLogin.Data[4][0] = 'Succeeded!'
                msg.append(windLogin.Data[4][0])
                
            accountNumber=k+1

        # Join saved ErrorMsgs to display
        msg = '\n'.join(msg)
        self.logon_msg_browser.setText(msg)          

    # Process order when the submit button is clicked
    def torderProcess(self):
        tmp=[]
        for j in range(5):
            tmp.append("")
            table_info = []
            for i in range(5):
                table_info.append(tmp)

        msg = list()

        for i in range(5):
            if(len(eval('self.label{0}_1.text()'.format(i)))!=0):
                logon_id = eval('self.label{0}_0.text()'.format(i))
                windcode = eval('self.label{0}_1.text()'.format(i))
                trade_side = eval('self.label{0}_2.text()'.format(i))
                price = eval('self.label{0}_3.text()'.format(i))
                amount = eval('self.label{0}_4.text()'.format(i))
                
                # Wind code, trading direction, order price, amount
                torderResult=w.torder(windcode,trade_side,price,amount,'OrderType=LMT;LogonID='+logon_id)
                # Save ErrorMsg
                msg.append(torderResult.Data[8][0])
        
        # Join saved ErrorMsgs to dispaly
        msg = '\n'.join(msg)
        self.order_msg_browser_2.setText(msg) 


    # Log out the accounts when the logout button is clicked
    def logout(self):
        global accountNumber
        if accountNumber!=0:
            for i in range(1,accountNumber):
                w.tlogout(i)
                print(i)
        self.close()       

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
