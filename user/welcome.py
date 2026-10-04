import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QMessageBox

from user.Signup import SignUpWindow

from employee.log_employee import LogInWindow
from db_manager import create_tables, create_employee_table


class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome Page")
        self.setFixedSize(1244, 700)
        self.move(350, 200)
        self.setWindowIcon(QIcon("../images/icon.png"))

        self.signup_window = None
        self.login_window = None
        self.emp_login_window = None

        self.init_ui()

    def init_ui(self):
        # Background
        self.bg_label = QLabel(self)
        image_path = '../images/bg2.jpeg'
        pixmap = QPixmap(image_path).scaled(self.size())
        self.bg_label.setPixmap(pixmap)
        self.bg_label.setGeometry(0, 0, 1244, 700)

        # Welcome Label
        welcome_text = '''<b>WELCOME</b><i>to our App</i>'''
        self.welcome_label = QLabel(welcome_text, self)
        self.welcome_label.setGeometry(500, 200, 600, 60)
        self.welcome_label.setStyleSheet('color: #196297; font-size: 55px;')

        # Info Button
        self.info_button = QPushButton("Info", self)
        self.info_button.setGeometry(610, 290, 100, 50)
        self.info_button.setStyleSheet('color: white; background-color: #196297; font-size: 25px;')
        self.info_button.setToolTip('About the App')
        self.info_button.clicked.connect(self.show_info)

        # Log In Button
        self.login_button = QPushButton("Log In", self)
        self.login_button.setGeometry(720, 290, 100, 50)
        self.login_button.setStyleSheet('color: white; background-color: #196297; font-size: 25px;')
        self.login_button.setToolTip('Login to your account')
        self.login_button.clicked.connect(self.open_login)

        # Sign Up Button
        self.signup_button = QPushButton("Sign Up", self)
        self.signup_button.setGeometry(830, 290, 100, 50)
        self.signup_button.setStyleSheet('color: white; background-color: #196297; font-size: 25px;')
        self.signup_button.setToolTip('Create a new account')
        self.signup_button.clicked.connect(self.open_signup)

        # Employee Login Button
        self.emplog_button = QPushButton("EmpLog", self)
        self.emplog_button.setGeometry(650, 355, 100, 50)
        self.emplog_button.setStyleSheet('color: white; background-color: #196297; font-size: 25px;')
        self.emplog_button.setToolTip('Employee Login')
        self.emplog_button.clicked.connect(self.open_emplog)

        # Exit Button
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setGeometry(780, 355, 100, 50)
        self.exit_button.setStyleSheet('color: white; background-color: #196297; font-size: 25px;')
        self.exit_button.setToolTip('Exit the app')
        self.exit_button.clicked.connect(QtWidgets.qApp.quit)

    def show_info(self):
        information = '''
        <h2 style="color:#196297; text-align:center;">Municipal Services Tracking</h2>
        <p style="font-size:14px; color:#333333; text-align:justify;">
        This application is designed to help users monitor and manage municipal services in an organized and efficient way.
        </p>
        <p style="font-size:14px; color:#333333; text-align:justify;">
        It allows users to register, log in, and interact with various local government services such as 
        <b>waste collection</b>, <b>water supply</b>, <b>electricity maintenance</b>, and <b>public requests</b>.
        </p>
        <p style="font-size:14px; color:#333333; text-align:justify;">
        The system provides a graphical interface for easy interaction, a database for storing service records,
        and real-time tracking of service statuses. Its goal is to improve communication between citizens and municipal departments,
        making city management smarter and more responsive.
        </p>
        '''
        QMessageBox.about(self, "Municipal Services Tracking", information)

    def open_login(self):
        from user.Login import logIn  # 👈 ننقل الاستيراد هنا
        self.login_window = logIn()
        self.login_window.show()
        self.close()

    def open_signup(self):
        self.signup_window = SignUpWindow()
        self.signup_window.show()
        self.close()

    def open_emplog(self):
        self.emp_login_window = LogInWindow()
        self.emp_login_window.show()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    create_tables()
    create_employee_table()
    welcome = WelcomeWindow()
    welcome.show()
    sys.exit(app.exec_())
