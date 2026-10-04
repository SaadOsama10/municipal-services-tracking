import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QMainWindow
)
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt
from db_manager import register_user  # هذا يمكن تركه لأنه لا يستورد شيء من welcome أو login


class SignUpWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.main_window = None

        self.bg = QLabel(self)

        self.title = QLabel("Sign Up", self)

        self.lu = QLabel("Username : ", self)
        self.ln = QLabel("Name : ", self)
        self.ls = QLabel("Surname : ", self)
        self.lp = QLabel("Password : ", self)
        self.lpc = QLabel("Confirm Pass : ", self)
        self.labels = [self.lu, self.ln, self.ls, self.lp, self.lpc]

        self.fu = QLineEdit(self)
        self.fn = QLineEdit(self)
        self.fs = QLineEdit(self)
        self.fp = QLineEdit(self)
        self.fpc = QLineEdit(self)

        self.fp.setEchoMode(QLineEdit.Password)
        self.fpc.setEchoMode(QLineEdit.Password)
        self.textfields = [self.fu, self.fn, self.fs, self.fp, self.fpc]

        self.register_btn = QPushButton("Register", self)

        self.haveaccount = QLabel("Have an account?", self)
        self.login_btn = QPushButton("Log in", self)

        self.GUI_init()

    def GUI_init(self):
        self.setWindowTitle("Sign Up - Municipal Services")
        self.setFixedSize(1244, 700)
        self.move(350, 200)
        self.setWindowIcon(QIcon("../images/icon.png"))

        self.bg.setPixmap(QPixmap("../images/bg2.jpeg").scaled(self.size(), Qt.IgnoreAspectRatio))
        self.bg.setGeometry(0, 0, 1244, 700)

        self.title.setFont(QFont("Arial", 40, QFont.Bold))
        self.title.setStyleSheet("color: #196297; font-size: 40px; font-weight: bold;")
        self.title.move(680, 100)
        self.title.adjustSize()

        y = 200
        for label, field in zip(self.labels, self.textfields):
            label.move(500, y)
            label.setFont(QFont("Arial", 16, QFont.Bold))
            label.setStyleSheet("color: #196297; font-size: 20px;")
            field.move(630, y)
            field.resize(300, 35)
            label.adjustSize()
            y += 60

        self.register_btn.setGeometry(630, 500, 300, 40)
        self.register_btn.setFont(QFont("Arial", 16, QFont.Bold))
        self.register_btn.setStyleSheet("color: #196297; font-size: 24px;")
        self.register_btn.clicked.connect(self.register_btn_clicked)

        self.login_btn.setFont(QFont("Arial", 16, QFont.Bold))
        self.login_btn.setStyleSheet("color: #196297; font-size: 24px;")
        self.login_btn.setGeometry(630, 550, 300, 40)
        self.haveaccount.move(500, 560)
        self.haveaccount.setFont(QFont("Arial", 9, QFont.Bold))
        self.haveaccount.adjustSize()
        self.login_btn.clicked.connect(self.login_btn_clicked)

    def register_btn_clicked(self):
        username = self.fu.text()
        name = self.fn.text()
        surname = self.fs.text()
        password = self.fp.text()
        confirm = self.fpc.text()

        elements = [username, name, surname, password, confirm]
        for x in elements:
            if x.strip() == "":
                QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
                return

        msg = register_user(username, name, surname, password, confirm)
        if "success" in msg.lower():
            QMessageBox.information(self, "Success", msg)
            self.login_btn_clicked()
        else:
            QMessageBox.warning(self, "Registration Error", msg)

    def login_btn_clicked(self):
        from Login import logIn
        self.main_window = logIn()
        self.main_window.show()
        self.close()

