import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from PyQt5.QtTest import *

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self.login_event_loop = QEventLoop()

        self.detail_account_info_event_loop = QEventLoop()

        self.account_dict = {}

        self.total = 0 # 매수수량

        self.stock_list = ["000660", "003490", "005930", "034020", "016380",
                     "020560" , "204320"]

        self.portfolio = {}
        self.jango = {}
        self.done = []

        self.screen_my_info = "2000"
        self.screen_meme_stock = "6000"

        self.get_ocx_instance()
        print(2)
        self.event()
        self.get_chejan()
        self.commConnect()
        self.get_account_info()

        self.sonjul = -1.5 #손절률
        self.goal = 3 # 목표수익률

    #실시간 정보요청
    def send_rq(self):
        for code in self.port:
            fids = "20"
            self.dynamicCall("SetRealReg(QSt, QSt, QSt, QSt)", "5001", code, fids , "1")
        print("req is done!")

    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    ###실시간 이벤트 발생###
    def event(self):
        self.OnEventConnect.connect(self.login)
        self.OnReceiveTrData.connect(self.trdata)

    def get_chejan(self):
       self.OnReceiveChejanData.connect(self.chejan)

    def get_master_code_name(self, code):
        name = self.dynamicCall("GetMasterCodeName(QSt)", code)
        return name

    def get_login_info(self, x):
        r = self.dynamicCall("GetLoginInfo(QSt)", x)
        return r

    def commConnect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop.exec_()

    ###로그인완료신호###
    def done_login(self, err_code):
        if err_code == 0:
            print("connected!")
        self.login_event_loop.exit()

    ###계좌정보요청###
    def get_accInfo(self):
        account_list = self.dynamicCall("GetLoginInfo(QString)", "ACCNO")
        account_num = account_list.split(';')[0]
        self.account_num = account_num

    ###계좌평가잔고내역요청###
    def account_mystock(self, sPrevNext= "0"):
        self.dynamicCall("SetInputValue(QSt, QSt)", "계좌번호", self.account_num)
        self.dynamicCall("SetInputValue(QSt, QSt)", "비밀번호", "0000")
        self.dynamicCall("SetInputValue(QSt, QSt)", "비밀번호입력매체구분", "00")
        self.dynamicCall("SetInputValue(QSt, QSt)", "조회구분", "2")
        self.dynamicCall("CommRqData(QSt, QSt, int, QSt)", "계좌평가잔고내역요청", "opw00018", sPrevNext, "2000")

        self.detail_account_info_event_loop.exec_()

    ###계좌평가잔고내역###
    def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):

        if sRQName == "계좌평가잔고내역요청":

            total_buy = self.dynamicCall("GetCommData(QStirng, QStirng, int, QString)", sTrCode, sRQName, 0, "총매입금")
            self.total_buy = int(total_buy)
            total_loss_money = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "총평가손익금액")
            self.total_loss_money = int(total_loss_money)
            total_loss_rate = self.dynamicCall("GetCommData(Qs, Qs, int, Qs)", sTrCode, sRQName, 0, "총수익률(%)")
            self.total_profit_loss_rate = float(total_loss_rate)

            rows = self.dynamicCall("GetRepeatCnt(Qs, Qs)", sTrCode, sRQName)
            # print(rows)
            for i in range(rows):
                code = self.dynamicCall("GetCommData(Qs, Qs, int, Qs)", sTrCode, sRQName, i, "종목번호")
                code = code.strip()[1:]

                code_name = self.dynamicCall("GetCommData(Qs, Qs, int, Qs)", sTrCode, sRQName, i, "종목명")
                stock_quant= self.dynamicCall("GetCommData(Qs, Qs, int, Qs)", sTrCode, sRQName, i, "보유수량")
                buy_price = self.dynamicCall("GetCommData(Qs, Qs, int, Qs)", sTrCode, sRQName, i, "매입가")
                earn = self.dynamicCall("GetCommData(Qs, Qs, int, Qs)", sTrCode, sRQName, i, "수익률(%)")
                now = self.dynamicCall("GetCommData(Qs, Qs, int, Qs)", sTrCode, sRQName, i, "현재가")
                canToBuy = self.dynamicCall("GetCommData(Qs, Qs, int, Qs)", sTrCode, sRQName, i, "매매가능수량")

                if code not in self.account_dict:
                    self.account_dict[code] = {}

                else :
                    pass

                code_name = code_name.strip()
                stock_quant = int(stock_quant.strip())
                buy_price = int(buy_price.strip())
                earn = float(earn.strip())
                now = int(now.strip())
          #      total_chegual_price = int(total_chegual_price.strip())
                canToBuy = int(canToBuy.strip())

                self.account_stock_dict[code].update({"종목명": code_name})
                self.account_stock_dict[code].update({"보유수량": stock_quant})
                self.account_stock_dict[code].update({"매입가": buy_price})
                self.account_stock_dict[code].update({"수익률(%)": earn})
                self.account_stock_dict[code].update({"현재가": now})

                self.account_stock_dict[code].update({'매매가능수량' : canToBuy})
                self.how = rows

            if sPrevNext == "2":
                self.detail_account_mystock(sPrevNext="2")
            else:
                self.detail_account_info_event_loop.exit()

    ###매수매도 요청###
    def send_order(self, rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no):
        self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                        [rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no])

    #틱봉별 거래진행 함수
    def trader(self, code, sRealType, sRealData):

        if sRealType == "주식체결":

            now = self.dynamicCall("GetCommRealData(QString, int)", code,
                                 self.realType.REALTYPE[sRealType]['현재가'])
            now = abs(int(now))

            s_hoga = self.dynamicCall("GetCommRealData(QString, int)", code,
                                 self.realType.REALTYPE[sRealType]['(최우선)매도호가'])
            s_hoga = abs(int(s_hoga))

            d_hoga = self.dynamicCall("GetCommRealData(QString, int)", code,
                                 self.realType.REALTYPE[sRealType]['(최우선)매수호가'])
            d_hoga = abs(int(d_hoga))

            if code not in self.portfolio.keys():
                self.portfolio_stock_dict.update({code: {}})

            self.portfolio[code].update({"현재가": now})

            self.portfolio[code].update({"(최우선)매도호가": s_hoga})
            self.portfolio[code].update({"(최우선)매수호가": d_hoga})
            now = self.portfolio[code]["현재가"]

            if code not in self.jango.keys() and code not in self.done:

                if self.total is not 0:
                    self.send_order("mesoo", "0101",
                             self.account_num, 1, code, self.total, now, "00", "")

                    self.done.append(code)


            elif code in self.jango.keys():

              buy_price = int(self.jango[code]["매입단가"])
              print("in medo", code, buy_price)
              earn = 100*((buy_price - now) / buy_price)

              if self.jango[code]["주문가능수량"] > 0:
                  if earn >= self.goal * 0.95  or earn <= self.sonjul * 0.95:
                      self.send_order("medo", "0101",
                                             self.account_num, 2, code, self.jango_dict[code]["주문가능수량"], now, "00", "")

              not_list = list(self.not_account_dict)
              for ornum in not_list:
                     t_code = self.not_account_stock_dict[ornum]["종목코드"]
                     not_quant = self.not_account_stock_dict[ornum]["미체결수량"]
                     gubun = self.not_account_stock_dict[ornum]["주문구분"]
                     c_price = self.not_account_stock_dict[ornum]["체결가"]

                     if code is t_code and gubun is "매도" :

                       if c_price is not now:

                          if earn >= 3  or earn <= -2:
                              self.send_order("re_medo", "0101",
                                      self.account_num, 6, code, not_quant, now, "00", ornum)

                     elif not_quant is 0:
                            del self.not_account_stock_dict[ornum]

            not_list = list(self.not_account_stock_dict)
            for ornum in not_list:
                t_code = self.not_account_stock_dict[ornum]["종목코드"]
                not_quant = self.not_account_stock_dict[ornum]["미체결수량"]
                gubun = self.not_account_stock_dict[ornum]["주문구분"]
                c_price = self.not_account_stock_dict[ornum]["체결가"]

                if code is t_code and gubun is "매수" :
                    upDown = 100((c_price - now)/ c_price)
                    if upDown <= -1.5 :
                        self.send_order("re_medo", "0101",
                                        self.account_num, 3, code, not_quant, now, "00", ornum)

    #체결정보에 맞춰 잔고, 미체결종목에 대한 업데이트
    def chejan_slot(self, sGubun, nItemCnt, sFidList):

        if int(sGubun) == 0:

            sCode = self.dynamicCall("GetChejanData(int)", 9001)[1:]

            orig_ord_num = self.dynamicCall("GetChejanData(int)",904)

            ord_num = self.dynamicCall("GetChejanData(int)",9203)

            order_status = self.dynamicCall("GetChejanData(int)", 913)

            order_quant = self.dynamicCall("GetChejanData(int)", 900)
            order_quant = int(order_quant)

            not_quant = self.dynamicCall("GetChejanData(int)", 902)
            not_quant = int(not_quant)

            gubun = self.dynamicCall("GetChejanData(int)", 905)
            gubun = gubun.strip().lstrip('+').lstrip('-')

            cheg_price = self.dynamicCall("GetChejanData(int)", 910)
            if cheg_price == '':
                cheg_price = 0
            else:
                chegl_price = int(cheg_price)

            cheg_quant = self.dynamicCall("GetChejanData(int)", 911)
            if cheg_quant == '':
                cheg_quant = 0
            else:
                cheg_quant = int(cheg_quant)

            current_price = self.dynamicCall("GetChejanData(int)", 10)
            current_price = abs(int(current_price))

            if ord_num not in self.not_account_dict.keys():
                self.not_account_stock_dict.update({ord_num: {}})
            print("in not")
            self.not_account_dict[ord_num].update({"종목코드": sCode})
            self.not_account_dict[ord_num].update({"주문번호": ord_num})
            self.not_account_dict[ord_num].update({"주문상태": order_status})
            self.not_account_dict[ord_num].update({"미체결수량": not_quant})
            self.not_account_dict[ord_num].update({"원주문번호": orig_ord_num})
            self.not_account_dict[ord_num].update({"주문구분": gubun})
            self.not_account_dict[ord_num].update({"체결가": cheg_price})
            self.not_account_dict[ord_num].update({"체결량": cheg_quant})
            self.not_account_dict[ord_num].update({"현재가": current_price})

            if self.not_account_stock_dict[ord_num]["미체결수량"] is 0 :
                 del self.not_account_stock_dict[ord_num]

        elif int(sGubun) == 1:  # 잔고
            print("in jango")
            sCode = self.dynamicCall("GetChejanData(int)", 9001)[1:]

            current_price = self.dynamicCall("GetChejanData(int)", 10)
            current_price = abs(int(current_price))

            own_quant = self.dynamicCall("GetChejanData(int)", 930)
            own_quant = int(own_quant)

            can_quant = self.dynamicCall("GetChejanData(int)", 933)
            can_quant = int(can_quant)

            buy_price = self.dynamicCall("GetChejanData(int)", 931)
            buy_price = abs(int(buy_price))

            earn = self.dynamicCall("GetChejanData(int)", 8019)
            earn = float(earn)

            total_price = self.dynamicCall("GetChejanData(int)",932)  # 계좌에 있는 종목의 총매입가
            total_price = int(total_price)

            me_gubun = self.dynamicCall("GetChejanData(int)", 946)
            if me_gubun is "매도":
                me_gubun = "2"
            elif me_gubun is "매수" :
                 me_gubun = "1"

            if sCode not in self.jango_dict.keys():
                self.jango_dict.update({sCode: {}})

            self.jango[sCode].update({"현재가": current_price})
            self.jango[sCode].update({"종목코드": sCode})
            self.jango[sCode].update({"보유수량": own_quant})
            self.jango[sCode].update({"주문가능수량": can_quant})
            self.jango[sCode].update({"매입단가": buy_price})
            self.jango[sCode].update({"손익율": earn})
            self.jango[sCode].update({"총매입가": total_price})
            self.jango[sCode].update({"매도매수구분": me_gubun})

            if own_quant == 0:
                del self.jango[sCode]