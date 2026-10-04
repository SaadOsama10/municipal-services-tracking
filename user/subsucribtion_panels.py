from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QTextEdit, QComboBox, QPushButton, QMessageBox, QCheckBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from db_manager import *
from my_sub import UserSubscriptions


class WaterSubscriptionForm(QFrame):
    def __init__(self, username):
        super().__init__()
        self.username = username

        self.setGeometry(120, 100, 650, 420)
        self.setStyleSheet("""
            QFrame { background-color:#f1f2f6; border-radius: 15px; }
            QLabel { font-size: 14px; }
            QLineEdit, QComboBox, QTextEdit {
                padding: 5px; border: 1px solid #aaa; border-radius: 5px; font-size: 13px;
            }
        """)
        self.setVisible(False)

        self.inputs = {}
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.inputs['address'] = QLineEdit()
        self.inputs['type'] = QComboBox()
        self.inputs['type'].addItems(["Residential", "Commercial", "Governmental", "Industrial", "Agricultural"])
        self.inputs['residents'] = QLineEdit()
        self.inputs['usage'] = QComboBox()
        self.inputs['usage'].addItems(["Drinking only", "Home use", "Agricultural", "Industrial", "Swimming Pool"])
        self.inputs['has_tank'] = QComboBox()
        self.inputs['has_tank'].addItems(["No", "Yes"])
        self.inputs['has_tank'].currentTextChanged.connect(self.toggle_tank_capacity)
        self.inputs['tank_capacity'] = QLineEdit()
        self.inputs['tank_capacity'].setEnabled(False)
        self.inputs['notes'] = QTextEdit()

        form_layout.addRow("Property Address :", self.inputs['address'])
        form_layout.addRow("Property Type :", self.inputs['type'])
        form_layout.addRow("Number of Residents :", self.inputs['residents'])
        form_layout.addRow("Water Usage :", self.inputs['usage'])
        form_layout.addRow("Has Water Tank ?", self.inputs['has_tank'])
        form_layout.addRow("Tank Capacity (L) :", self.inputs['tank_capacity'])
        form_layout.addRow("Notes :", self.inputs['notes'])

        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.btn_submit = QPushButton("Submit")
        self.btn_cancel = QPushButton("Cancel")
        self.btn_submit.setStyleSheet("background-color: #196297; color: white; padding: 8px; border-radius: 5px;")
        self.btn_cancel.setStyleSheet("background-color: #ccc; padding: 8px; border-radius: 5px;")
        self.btn_submit.clicked.connect(self.submit_form)
        self.btn_cancel.clicked.connect(self.hide)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_submit)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def toggle_tank_capacity(self, text):
        self.inputs['tank_capacity'].setEnabled(text == "Yes")

    def submit_form(self):
        data = {}
        for key, widget in self.inputs.items():
            if isinstance(widget, QTextEdit):
                value = widget.toPlainText().strip()
            elif isinstance(widget, QLineEdit):
                value = widget.text().strip()
            elif isinstance(widget, QComboBox):
                value = widget.currentText().strip()
            else:
                value = ""
            data[key] = value

        data["username"] = self.username

        missing = []
        for key, value in data.items():
            if key == 'tank_capacity' and data.get('has_tank') == "No":
                continue
            if not value and key != 'notes':
                missing.append(key)

        if missing:
            QMessageBox.warning(self, "Missing Data", "Please fill in all required fields.")
            return

        try:
            save_water_subscription(data)
            QMessageBox.information(self, "Success", "Subscription saved successfully.")
            self.hide()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save:\n{str(e)}")


class ElectricitySubscriptionForm(QFrame):
    def __init__(self, username):
        super().__init__()
        self.username = username

        self.setGeometry(120, 100, 650, 400)
        self.setStyleSheet("""
            QFrame { background-color:#f1f2f6; border-radius: 15px; }
            QLabel { font-size: 14px; }
            QLineEdit, QComboBox, QTextEdit {
                padding: 5px; border: 1px solid #aaa; border-radius: 5px; font-size: 13px;
            }
        """)
        self.setVisible(False)

        self.inputs = {}
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.inputs['address'] = QLineEdit()
        self.inputs['type'] = QComboBox()
        self.inputs['type'].addItems(["Residential", "Commercial", "Industrial", "Governmental"])
        self.inputs['phase'] = QComboBox()
        self.inputs['phase'].addItems(["Single Phase", "Three Phase"])
        self.inputs['usage'] = QLineEdit()
        self.inputs['generator'] = QComboBox()
        self.inputs['generator'].addItems(["No", "Yes"])
        self.inputs['notes'] = QTextEdit()

        form_layout.addRow("Property Address:", self.inputs['address'])
        form_layout.addRow("Property Type:", self.inputs['type'])
        form_layout.addRow("Electricity Phase:", self.inputs['phase'])
        form_layout.addRow("Estimated Usage (kWh):", self.inputs['usage'])
        form_layout.addRow("Need Generator?", self.inputs['generator'])
        form_layout.addRow("Notes:", self.inputs['notes'])

        layout.addLayout(form_layout)
        btn_layout = QHBoxLayout()
        self.btn_submit = QPushButton("Submit")
        self.btn_cancel = QPushButton("Cancel")
        self.btn_submit.setStyleSheet("background-color: #196297; color: white; padding: 8px; border-radius: 5px;")
        self.btn_cancel.setStyleSheet("background-color: #ccc; padding: 8px; border-radius: 5px;")
        self.btn_submit.clicked.connect(self.submit_form)

        self.btn_cancel.clicked.connect(self.hide)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_submit)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def submit_form(self):
        data = {}
        for key, widget in self.inputs.items():
            if isinstance(widget, QTextEdit):
                value = widget.toPlainText().strip()
            elif isinstance(widget, QLineEdit):
                value = widget.text().strip()
            elif isinstance(widget, QComboBox):
                value = widget.currentText().strip()
            else:
                value = ""
            data[key] = value

        data["username"] = self.username

        missing = []

        if missing:
            QMessageBox.warning(self, "Missing Data", "Please fill in all required fields.")
            return

        try:
            save_electricity_subscription(data)
            QMessageBox.information(self, "Success", "Electricity subscription submitted successfully.")
            self.hide()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save:\n{str(e)}")


class CleaningSubscriptionForm(QFrame):
    def __init__(self, username):
        super().__init__()
        self.username = username

        self.setGeometry(120, 100, 650, 350)
        self.setStyleSheet("""
            QFrame { background-color:#f1f2f6; border-radius: 15px; }
            QLabel { font-size: 14px; }
            QLineEdit, QTextEdit, QComboBox {
                padding: 5px; border: 1px solid #aaa; border-radius: 5px; font-size: 13px;
            }
        """)
        self.setVisible(False)

        self.inputs = {}
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.inputs['address'] = QLineEdit()
        self.inputs['property_type'] = QComboBox()
        self.inputs['property_type'].addItems(["House", "Building", "Institution", "Other"])
        self.inputs['frequency'] = QComboBox()
        self.inputs['frequency'].addItems(["Daily", "Weekly", "Monthly"])
        self.inputs['notes'] = QTextEdit()

        form_layout.addRow("Address:", self.inputs['address'])
        form_layout.addRow("Property Type:", self.inputs['property_type'])
        form_layout.addRow("Cleaning Frequency:", self.inputs['frequency'])
        form_layout.addRow("Notes:", self.inputs['notes'])

        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.btn_submit = QPushButton("Submit")
        self.btn_cancel = QPushButton("Cancel")
        self.btn_submit.setStyleSheet("background-color: #196297; color: white; padding: 8px; border-radius: 5px;")
        self.btn_cancel.setStyleSheet("background-color: #ccc; padding: 8px; border-radius: 5px;")
        self.btn_submit.clicked.connect(self.submit_form)

        self.btn_cancel.clicked.connect(self.hide)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_submit)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def submit_form(self):
        data = {}
        for key, widget in self.inputs.items():
            if isinstance(widget, QTextEdit):
                value = widget.toPlainText().strip()
            elif isinstance(widget, QLineEdit):
                value = widget.text().strip()
            elif isinstance(widget, QComboBox):
                value = widget.currentText().strip()
            else:
                value = ""
            data[key] = value

        data['username'] = self.username

        missing = [key for key in data if key != 'notes' and not data[key]]
        if missing:
            QMessageBox.warning(self, "Missing Data", "Please fill in all required fields.")
            return

        try:
            save_cleaning_subscription(data)
            QMessageBox.information(self, "Success", "Cleaning subscription submitted successfully.")
            self.hide()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save:\n{str(e)}")


class GasSubscriptionForm(QFrame):
    def __init__(self, username):
        super().__init__()
        self.username = username

        self.setGeometry(120, 100, 650, 400)
        self.setStyleSheet("""
            QFrame { background-color:#f1f2f6; border-radius: 15px; }
            QLabel { font-size: 14px; }
            QLineEdit, QComboBox, QTextEdit {
                padding: 5px; border: 1px solid #aaa; border-radius: 5px; font-size: 13px;
            }
        """)
        self.setVisible(False)

        self.inputs = {}
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.inputs['address'] = QLineEdit()
        self.inputs['property_type'] = QComboBox()
        self.inputs['property_type'].addItems(["Residential", "Commercial", "Industrial"])
        self.inputs['stove_type'] = QComboBox()
        self.inputs['stove_type'].addItems(["1-burner", "2-burner", "Built-in"])
        self.inputs['cylinder_size'] = QComboBox()
        self.inputs['cylinder_size'].addItems(["Small", "Medium", "Large"])
        self.inputs['usage'] = QLineEdit()
        self.inputs['notes'] = QTextEdit()

        form_layout.addRow("Property Address:", self.inputs['address'])
        form_layout.addRow("Property Type:", self.inputs['property_type'])
        form_layout.addRow("Stove Type:", self.inputs['stove_type'])
        form_layout.addRow("Cylinder Size:", self.inputs['cylinder_size'])
        form_layout.addRow("Usage:", self.inputs['usage'])
        form_layout.addRow("Notes:", self.inputs['notes'])

        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.btn_submit = QPushButton("Submit")
        self.btn_cancel = QPushButton("Cancel")
        self.btn_submit.setStyleSheet("background-color: #196297; color: white; padding: 8px; border-radius: 5px;")
        self.btn_cancel.setStyleSheet("background-color: #ccc; padding: 8px; border-radius: 5px;")
        self.btn_submit.clicked.connect(self.submit_form)

        self.btn_cancel.clicked.connect(self.hide)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_submit)
        btn_layout.addWidget(self.btn_cancel)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def submit_form(self):
        data = {}
        for key, widget in self.inputs.items():
            if isinstance(widget, QTextEdit):
                value = widget.toPlainText().strip()
            elif isinstance(widget, QLineEdit):
                value = widget.text().strip()
            elif isinstance(widget, QComboBox):
                value = widget.currentText().strip()
            else:
                value = ""
            data[key] = value

        data["username"] = self.username

        missing = [key for key in data if key != 'notes' and not data[key]]
        if missing:
            msg = "Please fill in all required fields."
            QMessageBox.warning(self, "Missing Data", msg)
            return

        try:
            save_gas_subscription(data)
            QMessageBox.information(self, "Success", "Gas subscription submitted successfully.")
            self.hide()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save:\n{str(e)}")


class VisaDigitalForm(QFrame):
    def __init__(self, username):
        super().__init__()
        self.username = username

        self.setGeometry(120, 100, 650, 400)
        self.setStyleSheet("""
            QFrame {
                background-color:#f1f2f6;
                border-radius: 15px;
            }
            QLabel {
                font-size: 13px;
            }
            QLineEdit {
                padding: 4px;
                border: 1px solid #aaa;
                border-radius: 4px;
                font-size: 13px;
            }
        """)
        self.setVisible(False)

        self.inputs = {}
        layout = QVBoxLayout()

        title = QLabel("Payment Information")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: black;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        form_layout = QFormLayout()
        self.inputs['card_number'] = QLineEdit()
        self.inputs['balance'] = QLineEdit("₺0,00")
        self.inputs['balance'].setReadOnly(True)
        self.inputs['topup'] = QLineEdit()
        form_layout.addRow("Transportation Card Number:", self.inputs['card_number'])
        form_layout.addRow("Current Balance:", self.inputs['balance'])
        form_layout.addRow("Balance to be loaded:", self.inputs['topup'])

        credit_title = QLabel("Credit/Debit Card Information")
        credit_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        credit_title.setStyleSheet("color: black;")
        credit_title.setAlignment(Qt.AlignCenter)

        credit_form = QFormLayout()
        self.inputs['owner'] = QLineEdit()
        self.inputs['credit_card'] = QLineEdit()
        credit_form.addRow("Cardholder Name Surname:", self.inputs['owner'])
        credit_form.addRow("Card No:", self.inputs['credit_card'])

        date_row = QHBoxLayout()
        self.inputs['month'] = QLineEdit()
        self.inputs['year'] = QLineEdit()
        self.inputs['cvv'] = QLineEdit()
        self.inputs['month'].setPlaceholderText("month")
        self.inputs['year'].setPlaceholderText("year")
        self.inputs['cvv'].setPlaceholderText("CVV code")
        date_row.addWidget(self.inputs['month'])
        date_row.addWidget(self.inputs['year'])
        date_row.addWidget(self.inputs['cvv'])

        self.checkbox = QCheckBox("I have read and accept the distance sales contract.")

        btn_layout = QHBoxLayout()
        submit_btn = QPushButton("Pay Now")
        submit_btn.setStyleSheet("background-color: #196297; color: white; padding: 6px; border-radius: 5px;")
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("padding: 6px;")
        submit_btn.clicked.connect(self.submit_form)

        cancel_btn.clicked.connect(self.hide)
        btn_layout.addStretch()
        btn_layout.addWidget(submit_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(form_layout)
        layout.addWidget(credit_title)
        layout.addLayout(credit_form)
        layout.addLayout(date_row)
        layout.addWidget(self.checkbox)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def submit_form(self):
        data = {}
        for key, field in self.inputs.items():
            data[key] = field.text().strip()

        data['username'] = self.username

        if not all(data.values()) or not self.checkbox.isChecked():
            QMessageBox.warning(self, "Missing Information", "Please fill in all fields and accept the agreement.")
            return

        try:
            save_visa_subscription(data)
            QMessageBox.information(self, "Successful", "Payment completed successfully.")
            self.hide()

        except ValueError as e:
            QMessageBox.warning(self, "Invalid Card", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Database error:\n{str(e)}")
