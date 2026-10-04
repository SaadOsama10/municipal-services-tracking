import sys
from PyQt5.QtWidgets import (
    QApplication, QLabel, QLineEdit, QPushButton, QMainWindow, QMessageBox
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

from db_manager import create_employee_table, check_employee_credentials
from employee.dashboard_emp import Dashboard


class LogInWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log in as Employee")
        self.setFixedSize(1244, 700)
        self.move(350, 200)

        self.bg = QLabel(self)
        self.title = QLabel("Log In", self)
        self.title.setGeometry(280, 40, 830, 50)

        self.ln = QLabel("Username : ", self)
        self.lp = QLabel("Password : ", self)
        self.labels = [self.ln, self.lp]

        self.fusername = QLineEdit(self)
        self.fpassword = QLineEdit(self)
        self.fpassword.setEchoMode(QLineEdit.Password)

        self.textfields = [self.fusername, self.fpassword]

        self.register_btn = QPushButton("Log in", self)
        self.register_btn.clicked.connect(self.handle_login)

        self.setup_ui()

    def setup_ui(self):
        self.bg.setPixmap(QPixmap("../images/bg2.jpeg").scaled(self.size(), Qt.IgnoreAspectRatio))
        self.bg.setGeometry(0, 0, 1244, 700)

        self.title.setFont(QFont("Arial", 40, QFont.Bold))
        self.title.setStyleSheet("color: #196297; font-size: 40px; font-weight: bold;")
        self.title.move(680, 100)

        self.ln.move(500, 220)
        self.lp.move(500, 280)
        for label in self.labels:
            label.setFont(QFont("Arial", 16, QFont.Bold))
            label.setStyleSheet("color: #196297; font-size: 20px;")

        self.fusername.move(630, 220)
        self.fpassword.move(630, 280)
        for field in self.textfields:
            field.resize(300, 35)

        self.register_btn.setGeometry(630, 350, 300, 40)
        self.register_btn.setFont(QFont("Arial", 16, QFont.Bold))
        self.register_btn.setStyleSheet("color: #196297; font-size: 24px;")

    def handle_login(self):
        username = self.fusername.text()
        password = self.fpassword.text()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        if check_employee_credentials(username, password):
            QMessageBox.information(self, "Login Successful", f"Welcome, {username}!")

            self.dashboard = Dashboard(username)
            self.dashboard.show()
            self.close()

        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password.")

