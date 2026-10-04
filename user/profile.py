import sys
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox,
    QGroupBox, QRadioButton, QDateEdit, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon
from db_manager import save_profile,  create_tables,get_user_id


class Profile(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        create_tables()

        self.setWindowIcon(QIcon("../images/icon.png"))
        self.setWindowTitle("Profile Form")
        self.setStyleSheet("background-color: #f1f2f6;")
        self.setGeometry(100, 100, 900, 600)

        # Title
        title = QLabel("Your personal profile info", self)
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setGeometry(250, 10, 400, 40)
        title.setAlignment(Qt.AlignCenter)

        # Labels
        self.create_label("First name:", 50, 100)
        self.create_label("Last name:", 50, 200)
        self.create_label("Username: (not your e-mail)", 50, 300)
        self.create_label("Your e-mail:", 50, 400)

        self.create_label("Personal phone number:", 320, 100)
        self.create_label("TC kimlik:", 320, 200)
        self.create_label("City:", 320, 300)
        self.create_label("Sex:", 320, 400)

        self.create_label("Old password: *", 600, 100)
        self.create_label("New password: *", 600, 200)
        self.create_label("Confirm new password: *", 600, 300)
        self.create_label("Birthday:", 600, 400)

        # Inputs
        self.input_firstname = QLineEdit(self)
        self.input_firstname.setGeometry(50, 150, 200, 30)

        self.input_lastname = QLineEdit(self)
        self.input_lastname.setGeometry(50, 250, 200, 30)

        self.input_username = QLineEdit(self)
        self.input_username.setGeometry(50, 350, 200, 30)

        self.input_email = QLineEdit(self)
        self.input_email.setGeometry(50, 450, 200, 30)

        self.input_phone = QLineEdit(self)
        self.input_phone.setGeometry(320, 150, 200, 30)
        self.input_phone.setPlaceholderText("5xxxxxxxxx")

        self.input_tc = QLineEdit(self)
        self.input_tc.setGeometry(320, 250, 200, 30)

        self.input_city = QComboBox(self)
        self.input_city.setGeometry(320, 350, 200, 30)
        self.input_city.addItems(["Ankara", "Istanbul", "Trabzon", "Aksaray", "Sabanca", "Bursa", "Adana", "Antalya"])

        # Sex (Radio Buttons)
        self.sex_group = QGroupBox(self)
        self.sex_group.setGeometry(320, 440, 200, 40)
        self.sex_male = QRadioButton("Male", self.sex_group)
        self.sex_female = QRadioButton("Female", self.sex_group)

        self.sex_male.move(0, 0)
        self.sex_female.move(70, 0)
        self.sex_male.setChecked(True)

        # Passwords
        self.input_oldpass = QLineEdit(self)
        self.input_oldpass.setGeometry(600, 150, 200, 30)
        self.input_oldpass.setEchoMode(QLineEdit.Password)

        self.input_newpass = QLineEdit(self)
        self.input_newpass.setGeometry(600, 250, 200, 30)
        self.input_newpass.setEchoMode(QLineEdit.Password)

        self.input_confirmpass = QLineEdit(self)
        self.input_confirmpass.setGeometry(600, 350, 200, 30)
        self.input_confirmpass.setEchoMode(QLineEdit.Password)

        # Birthday
        self.input_birthday = QDateEdit(self)
        self.input_birthday.setGeometry(600, 450, 200, 30)
        self.input_birthday.setCalendarPopup(True)
        self.input_birthday.setDisplayFormat("yyyy-MM-dd")
        self.input_birthday.setDate(QDate.currentDate())

        # Save Button
        save_btn = QPushButton("Correct. Save info", self)
        save_btn.setGeometry(600, 500, 200, 40)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        save_btn.clicked.connect(self.save_data)

    def create_label(self, text, x, y):
        label = QLabel(text, self)
        label.setFont(QFont("Segoe UI", 10))
        label.move(x, y)
        return label

    from PyQt5.QtWidgets import QMessageBox

    def save_data(self):
        try:
            sex = "Male" if self.sex_male.isChecked() else "Female"
            birthday = self.input_birthday.date().toString("yyyy-MM-dd")

            user_id = get_user_id(self.input_username.text())

            if user_id is None:
                QMessageBox.warning(self, "Error", "User not found.")
                return

            data = (
                user_id,
                self.input_firstname.text(),
                self.input_lastname.text(),
                self.input_email.text(),
                self.input_phone.text(),
                self.input_tc.text(),
                self.input_city.currentText(),
                sex,
                birthday
            )
            save_profile(data)

            QMessageBox.information(self, "Success", "Profile saved successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving:\n{e}")
