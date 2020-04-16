from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

class Ui_MainWindow(object):
    def upload(self, r, newrow):
        total_cost = 0
        row = r-1
        self.table.insertRow(row)

        for col in range(6):
            self.table.setItem(row, col, QTableWidgetItem(str(newrow[col])))

        value = self.table.item(0, 1).text()

        for rows in range(1, r):
            value = int(value) + int(self.table.item(rows, 1).text())

        print(value)
        self.cost.setText(str(value))


    def search(self, barcode):
        cell = database.find(barcode)
        newrow = database.row_values(cell.row)
        billing.append_row(newrow)
        customer.append_row(newrow)
        rows = customer.get_all_records()
        r = len(rows)
        self.upload(r, newrow)

    def read_barcode(self):
        barcode = self.inpt.text()
        self.inpt.clear()
        self.search(barcode)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setMinimumSize(QtCore.QSize(660, 480))
        MainWindow.setWindowTitle("Product Details")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 10, 81, 31))
        self.label.setFont(QtGui.QFont("Franklin Gothic Medium", 16))
        self.label.setText("Barcode")
        self.inpt = QtWidgets.QLineEdit(self.centralwidget)
        self.inpt.setGeometry(QtCore.QRect(220, 9, 361, 31))
        self.inpt.setFont(QtGui.QFont("Franklin Gothic Medium", 11))
        self.inpt.setClearButtonEnabled(True)
        self.inpt.setPlaceholderText("Read Barcode")
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(20, 60, 621, 361))
        #self.table.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.table.setFont(QtGui.QFont("Franklin Gothic Medium", 10))
        self.table.setRowCount(0)
        self.table.setColumnCount(6)
        self.table.setObjectName("table")
        self.table.setHorizontalHeaderLabels(("Barcode", "Cost", "Product", "MFD", "EXP", "Quantity"))
        self.table.setColumnWidth(0, 140)
        self.table.setColumnWidth(2, 140)
        self.table.setColumnWidth(1, 60)
        self.table.setColumnWidth(5, 60)
        self.amount = QtWidgets.QLabel(self.centralwidget)
        self.amount.setGeometry(QtCore.QRect(80, 430, 120, 23))
        self.amount.setFont(QtGui.QFont("Franklin Gothic Medium", 13))
        self.amount.setText("Total Amount :")
        self.cost = QtWidgets.QLabel(self.centralwidget)
        self.cost.setGeometry((QtCore.QRect(225, 430, 100, 23)))
        self.cost.setFont(QtGui.QFont("Franklin Gothic Medium", 13))
        self.inpt.returnPressed.connect(self.read_barcode)
        MainWindow.setCentralWidget(self.centralwidget)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    database = client.open("database").sheet1
    customer = client.open("customer").sheet1
    billing = client.open("billing").sheet1
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
