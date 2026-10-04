import sqlite3
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QMenu, QAction, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from db_manager import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data.db")


class UserSubscriptions(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"Subscriptions for {username}")
        self.resize(900, 500)

        layout = QVBoxLayout(self)
        self.label = QLabel(f"Subscriptions for user: {username}")
        layout.addWidget(self.label)

        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.pay_button = QPushButton("Pay Bills")
        self.pay_button.setStyleSheet("background-color: #196297; color: white; font-weight: bold;")
        layout.addWidget(self.pay_button)
        self.pay_button.clicked.connect(self.open_pay_panel)
        layout.addWidget(self.pay_button)

        self.setLayout(layout)
        self.load_data()

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def load_data(self):
        self.table.clearContents()
        data = fetch_user_subscriptions(self.username)

        if data:
            self.table.setRowCount(len(data))
            self.table.setColumnCount(len(data[0]))

            headers = ["Service"] + ["location"] + ["type"] + ["amount"]
            self.table.setHorizontalHeaderLabels(headers)

            for row_idx, row in enumerate(data):
                for col_idx, value in enumerate(row):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        else:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            self.label.setText("No subscriptions found.")

    def refresh(self):
        self.load_data()

    def show_context_menu(self, pos):
        context_menu = QMenu(self)

        refresh_action = QAction("🔁 Refresh Table", self)
        refresh_action.triggered.connect(self.refresh)
        context_menu.addAction(refresh_action)

        context_menu.exec_(self.mapToGlobal(pos))

    def open_pay_panel(self):
        self.pay_panel = PayBillsPanel(self.username)
        self.pay_panel.show()


from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout
)

from db_manager import fetch_unpaid_bills, mark_bill_as_paid  # تأكد من استيراد الدالة الجديدة


class PayBillsPanel(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Pay Bills")
        self.resize(700, 400)

        layout = QVBoxLayout()
        self.label = QLabel(f"Unpaid Bills for {username}")
        layout.addWidget(self.label)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_bills()

    def load_bills(self):
        self.table.clearContents()
        bills = fetch_unpaid_bills(self.username)

        if bills:
            self.table.setRowCount(len(bills))
            self.table.setColumnCount(6)
            self.table.setHorizontalHeaderLabels(["Service", "Month", "Consumption", "Amount", "Status", "Action"])

            for row_idx, bill in enumerate(bills):
                for col_idx in range(5):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(bill[col_idx])))

                pay_button = QPushButton("Pay")
                pay_button.clicked.connect(lambda _, b=bill: self.pay_bill(b))  # تمرير الفاتورة
                self.table.setCellWidget(row_idx, 5, pay_button)
        else:
            self.label.setText("No unpaid bills found.")
            self.table.setRowCount(0)
            self.table.setColumnCount(0)


    def pay_bill(self, bill):
        visa_info = get_user_visa(self.username)

        if not visa_info:
            QMessageBox.warning(self, "No Visa Found", "You must register a Visa card before paying.")
            return

        card_number, owner_name = visa_info
        # show massage for prove payment

        confirm = QMessageBox.question(
            self,
            "Confirm Payment",
            f"You will pay using:\n\nCard Number: {card_number}\nOwner Name: {owner_name}\n\nDo you want to continue?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            service = bill[0]
            month = bill[1]
            mark_bill_as_paid(self.username, service, month)
            QMessageBox.information(self, "Success", "Bill has been paid successfully.")
            self.load_bills()
