import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QApplication
from PyQt5.QtGui import QFont
from db_manager import get_user_id, add_gas_bill, create_tables, get_all_userG


class GasBillPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Panel - Gas Bills")
        self.setGeometry(700, 250, 500, 600)
        self.setStyleSheet("background-color: #f1f2f6;")
        create_tables()
        self.setup_ui()

    def setup_ui(self):
        font = QFont("Segoe UI", 20)

        # Username
        self.user_label = QLabel("Username:", self)
        self.user_label.setGeometry(20, 20, 200, 50)
        self.user_label.setFont(font)

        self.user_input = QComboBox(self)
        self.user_input.setGeometry(190, 25, 250, 50)
        self.user_input.setFont(QFont("Segoe UI", 12))
        self.user_input.setStyleSheet("background-color: white;")
        self.user_input.addItems(get_all_userG())

        # Month
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

        # Consumption
        self.consumption_label = QLabel("Consumption (m³):", self)
        self.consumption_label.setGeometry(20, 160, 300, 50)
        self.consumption_label.setFont(font)

        self.consumption_input = QLineEdit(self)
        self.consumption_input.setGeometry(330, 160, 100, 50)
        self.consumption_input.setFont(QFont("Segoe UI", 12))
        self.consumption_input.setStyleSheet("background-color: white;")

        # First rate
        self.frate_label = QLabel("First 20 m³ rate:", self)
        self.frate_label.setGeometry(20, 230, 300, 50)
        self.frate_label.setFont(font)

        self.frate_input = QLineEdit(self)
        self.frate_input.setGeometry(330, 230, 100, 50)
        self.frate_input.setFont(QFont("Segoe UI", 12))
        self.frate_input.setStyleSheet("background-color: white;")

        # Above rate
        self.arate_label = QLabel("Above 20 m³ rate:", self)
        self.arate_label.setGeometry(20, 300, 300, 50)
        self.arate_label.setFont(font)

        self.arate_input = QLineEdit(self)
        self.arate_input.setGeometry(330, 300, 100, 50)
        self.arate_input.setFont(QFont("Segoe UI", 12))
        self.arate_input.setStyleSheet("background-color: white;")

        # Add button
        self.add_button = QPushButton("Add Bill", self)
        self.add_button.setGeometry(170, 500, 150, 50)
        self.add_button.setFont(QFont("Segoe UI", 14))
        self.add_button.setStyleSheet("background-color: #196297; color: white; font-weight: bold;")
        self.add_button.clicked.connect(self.add_bill)

    def calculate_gas_bill(self, consumption, frate, arate):
        if consumption <= 20:
            return consumption * frate
        else:
            return 20 * frate + (consumption - 20) * arate

    def add_bill(self):
        username = self.user_input.currentText()
        month = self.month_input.currentText()

        try:
            consumption = float(self.consumption_input.text())
            frate = float(self.frate_input.text())
            arate = float(self.arate_input.text())
            if consumption < 0 or frate < 0 or arate < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid positive numbers.")
            return

        user_id = get_user_id(username)
        if user_id is None:
            QMessageBox.warning(self, "User Not Found", f"User '{username}' does not exist.")
            return

        amount = self.calculate_gas_bill(consumption, frate, arate)
        add_gas_bill(user_id, username, month, consumption, amount, frate, arate)

        QMessageBox.information(self, "Success", f"Gas bill added successfully: {amount:.2f} ₺")
        self.consumption_input.clear()
        self.frate_input.clear()
        self.arate_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GasBillPanel()
    window.show()
    sys.exit(app.exec_())
