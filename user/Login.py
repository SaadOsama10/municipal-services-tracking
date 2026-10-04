import sys
from PyQt5.QtWidgets import (
    QApplication, QLabel, QLineEdit, QPushButton, QMessageBox, QMainWindow
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from db_manager import check_credentials
from dashboard import Dashboard


class logIn(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log in as User")
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
        self.haveaccount = QLabel("You haven't an account ?", self)
        self.login_btn = QPushButton("Sign up now !", self)

        self.GU_Utin()

    def GU_Utin(self):
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
        self.register_btn.clicked.connect(self.login_btn_clicked)

        self.login_btn.setFont(QFont("Arial", 16, QFont.Bold))
        self.login_btn.setStyleSheet("color: #196297; font-size: 24px;")
        self.login_btn.setGeometry(630, 400, 300, 40)
        self.haveaccount.move(420, 410)
        self.haveaccount.setFont(QFont("Arial", 10, QFont.Bold))
        self.haveaccount.adjustSize()
        self.login_btn.clicked.connect(self.sign_up_clicked)

    def login_btn_clicked(self):
        username = self.fusername.text()
        password = self.fpassword.text()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        if check_credentials(username, password):
            QMessageBox.information(self, "Login", f"Welcome, {username}!")
            self.open_dashboard(username)
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password.")

    def sign_up_clicked(self):
        from Signup import SignUpWindow
        self.main_window = SignUpWindow()
        self.main_window.show()
        self.close()

    def open_dashboard(self, fusername):
        self.dashboard_window = Dashboard(fusername)
        self.dashboard_window.show()
        self.close()
