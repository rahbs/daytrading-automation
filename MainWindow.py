from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_UI(object):
    def setupUi(self, UI):
        UI.setObjectName("UI")
        UI.resize(809, 632)
        UI.setAcceptDrops(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        UI.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(UI)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 300, 221, 241))
        self.groupBox.setObjectName("groupBox")
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(80, 40, 131, 21))
        self.comboBox.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.comboBox.setObjectName("comboBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 40, 61, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 100, 81, 20))
        self.label_2.setObjectName("label_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(120, 160, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_7.setGeometry(QtCore.QRect(80, 100, 131, 21))
        self.lineEdit_7.setText("")
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(250, 90, 521, 451))
        self.groupBox_3.setObjectName("groupBox_3")
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox_3)
        self.tableWidget.setGeometry(QtCore.QRect(10, 20, 271, 271))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_4.setGeometry(QtCore.QRect(290, 20, 211, 271))
        self.groupBox_4.setObjectName("groupBox_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_5.setGeometry(QtCore.QRect(80, 80, 113, 21))
        self.lineEdit_5.setText("")
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 210, 93, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_5.setGeometry(QtCore.QRect(110, 210, 93, 28))
        self.pushButton_5.setObjectName("pushButton_5")
        self.label_3 = QtWidgets.QLabel(self.groupBox_4)
        self.label_3.setGeometry(QtCore.QRect(10, 80, 61, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_4)
        self.label_4.setGeometry(QtCore.QRect(10, 100, 61, 21))
        self.label_4.setObjectName("label_4")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 90, 221, 201))
        self.groupBox_2.setObjectName("groupBox_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_3.setGeometry(QtCore.QRect(70, 40, 113, 21))
        self.lineEdit_3.setText("")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_4.setGeometry(QtCore.QRect(70, 70, 113, 21))
        self.lineEdit_4.setText("")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_3.setGeometry(QtCore.QRect(110, 140, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(10, 40, 61, 20))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(10, 70, 61, 20))
        self.label_7.setObjectName("label_7")
        UI.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(UI)
        self.statusbar.setObjectName("statusbar")
        UI.setStatusBar(self.statusbar)

        self.retranslateUi(UI)
        QtCore.QMetaObject.connectSlotsByName(UI)

    def retranslateUi(self, UI):
        _translate = QtCore.QCoreApplication.translate
        UI.setWindowTitle(_translate("UI", "Welcom JooLin!"))
        self.groupBox.setTitle(_translate("UI", "주문"))
        self.label.setText(_translate("UI", "주문계좌"))
        self.label_2.setText(_translate("UI", "매수량"))
        self.pushButton_2.setText(_translate("UI", "거래 시작"))
        self.groupBox_3.setTitle(_translate("UI", "추천 종목 및 변경"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("UI", "종목코드"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("UI", "종목이름"))
        self.groupBox_4.setTitle(_translate("UI", "종목 추가/제거"))
        self.pushButton_4.setText(_translate("UI", "추가"))
        self.pushButton_5.setText(_translate("UI", "제거"))
        self.label_3.setText(_translate("UI", "종목입력"))
        self.label_4.setText(_translate("UI", "(코드)"))
        self.groupBox_2.setTitle(_translate("UI", "매도 설정"))
        self.pushButton_3.setText(_translate("UI", "저장"))
        self.label_6.setText(_translate("UI", "목표(%)"))
        self.label_7.setText(_translate("UI", "손절(%)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    UI = QtWidgets.QMainWindow()
    ui = Ui_UI()
    ui.setupUi(UI)
    UI.show()
    sys.exit(app.exec_())

