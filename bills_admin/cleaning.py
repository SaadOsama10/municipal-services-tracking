import sys

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QApplication
from PyQt5.QtGui import QFont
from db_manager import get_user_id, add_cleaning_bill, create_tables, get_all_userC


class CleaningBillPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Panel - Cleaning Bills")
        self.setGeometry(700, 250, 500, 400)
        self.setStyleSheet("background-color: #f1f2f6;")
        create_tables()
        self.setup_ui()

    def setup_ui(self):
        font = QFont("Segoe UI", 20)

        self.user_label = QLabel("Username:", self)
        self.user_label.setGeometry(20, 20, 200, 50)
        self.user_label.setFont(font)

        self.user_input = QComboBox(self)
        self.user_input.setGeometry(190, 25, 250, 50)
        self.user_input.setFont(QFont("Segoe UI", 12))
        self.user_input.addItems(get_all_userC())
        self.user_input.setStyleSheet("background-color: white;")

        self.month_label = QLabel("Month:", self)
        self.month_label.setGeometry(20, 90, 200, 50)
        self.month_label.setFont(font)

        self.month_input = QComboBox(self)
        self.month_input.setGeometry(190, 95, 250, 40)
        self.month_input.setFont(QFont("Segoe UI", 12))
        self.month_input.setStyleSheet("background-color: white;")
        self.month_input.addItems([
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ])

        self.amount_label = QLabel("Fixed Amount (₺):", self)
        self.amount_label.setGeometry(20, 160, 300, 50)
        self.amount_label.setFont(font)

        self.amount_input = QLineEdit(self)
        self.amount_input.setGeometry(290, 160, 100, 50)
        self.amount_input.setFont(QFont("Segoe UI", 12))
        self.amount_input.setStyleSheet("background-color: white;")

        self.add_button = QPushButton("Add Bill", self)
        self.add_button.setGeometry(170, 300, 150, 50)
        self.add_button.setFont(QFont("Segoe UI", 14))
        self.add_button.setStyleSheet("background-color: #2980b9; color: white; font-weight: bold;")
        self.add_button.clicked.connect(self.add_bill)

    def add_bill(self):
        username = self.user_input.currentText()
        month = self.month_input.currentText()

        try:
            amount = float(self.amount_input.text())
            if amount < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid amount.")
            return

        user_id = get_user_id(username)
        if user_id is None:
            QMessageBox.warning(self, "User Not Found", "No user found with that username.")
            return

        add_cleaning_bill(user_id, username, month, amount)
        QMessageBox.information(self, "Success", f"Cleaning bill added: {amount:.2f} ₺")
        self.amount_input.clear()


if __name__ == "_main_":
    app = QApplication(sys.argv)
    window = CleaningBillPanel()
    window.show()
    sys.exit(app.exec_())