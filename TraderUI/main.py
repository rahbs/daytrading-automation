import sys
from PyQt5 import uic
from kw.kiwoom import *
from PyQt5.QtWidgets import *
from PyQt5.QtTest import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets

form = uic.loadUiType('MainWindow.ui')[0]

class Main(QMainWindow, form):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.kiwoom = Kiwoom() #get open api

        ###사용자 계좌 설정###
        accounts_num = int(self.kiwoom.get_login_info("ACCOUNT_CNT"))
        accounts = self.kiwoom.get_login_info("ACCNO")
        accounts_list = accounts.split(';')[0:accounts_num]
        self.comboBox.addItems(accounts_list)

        ###이벤트 발생###
        self.pushButton_2.clicked.connect(self.mesoo)
        self.pushButton_3.clicked.connect(self.medo_setting)
        self.pushButton_4.clicked.connect(self.portfolio_setting_ins)
        self.pushButton_5.clicked.connect(self.portfolio_setting_del)

        ###종목리스트 구성###
        self.tableWidget.setRowCount(len(self.kiwoom.port))
        for i in range(len(self.kiwoom.port)):
          item = QTableWidgetItem(self.kiwoom.port[i])
          item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
          self.tableWidget.setItem(i, 0, item)

          name = QTableWidgetItem(self.kiwoom.get_master_code_name(self.kiwoom.port[i]))
          name.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
          self.tableWidget.setItem(i, 1, name)

    def stop(self):
        for code in self.kiwoom.port:
            self.dynamicCall("SetRealRemove(QString, QString)", self.kiwoom.portfolio[code]['스크린번호'], code)

        QTest.qWait(2000)

        for code in self.kiwoom.jango_dict.keys():
            iCode = code
            order_type = 1
            num = 2
            hoga = "03"
            price = 0
            self.kiwoom.send_order("mesoo", "0101",
                 self.kiwoom.account_num, 1, iCode, num, price, hoga, "")

    def portfolio_setting_ins(self):
        insert = self.lineEdit_5.text()
        if insert in self.kiwoom.stock_list:
            pass

        else :
         if insert not in self.kiwoom.stock_list :
            self.kiwoom.stock_list.append(insert)

         self.tableWidget.setRowCount(len(self.kiwoom.stock_list))
         for i in range(len(self.kiwoom.stock_list)) :
           item = QTableWidgetItem(self.kiwoom.stock_list[i])
           item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
           self.tableWidget.setItem(i, 0, item)

           name = QTableWidgetItem(self.kiwoom.get_master_code_name(self.kiwoom.stock_list[i]))
           name.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
           self.tableWidget.setItem(i, 1, name)

         self.tableWidget.resizeRowsToContents()


    def portfolio_setting_del(self):
        de = self.lineEdit_5.text()

        if de is None:
            pass

        else:

         if de in self.kiwoom.stock_list :
            self.kiwoom.stock_list.remove(de)

         self.tableWidget.setRowCount(len(self.kiwoom.stock_list))
         for i in range(len(self.kiwoom.stock_list)) :
           item = QTableWidgetItem(self.kiwoom.stock_list[i])
           item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
           self.tableWidget.setItem(i, 0, item)

           name = QTableWidgetItem(self.kiwoom.get_master_code_name(self.kiwoom.stock_list[i]))

           name.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)

           self.tableWidget.setItem(i, 1, name)

         self.tableWidget.resizeRowsToContents()


    def medo_setting(self):
        self.kiwoom.sonjul = -float(self.lineEdit_3.text())
        self.kiwoom.goal = float(self.lineEdit_4.text())


    def mesoo(self):
        self.kiwoom.send_rq()
        self.kiwoom.total = int(self.lineEdit_7.text())
        self.kiwoom.account_mystock()
        self.kiwoom.OnReceiveRealData.connect(self.kiwoom.trader)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    app.exec_()

