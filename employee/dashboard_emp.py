# dashboard_emp.py

import sys
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QMainWindow, QStackedWidget,
    QFrame, QApplication, QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize

from db_manager import create_tables
from employee.all_users import ManageUsers
from employee.ManageRequests import ManageRequests


class Main(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username

        from bills_admin.water import AdminPanel as WaterForm
        from bills_admin.electric import AdminPanel as ElectricForm
        from bills_admin.gas import GasBillPanel as GasForm
        from bills_admin.cleaning import CleaningBillPanel as CleaningForm


        self.water_form = WaterForm()
        self.electric_form = ElectricForm()
        self.gas_form = GasForm()
        self.clean_form = CleaningForm()

        self.subl = QLabel("Subscriptions", self)
        self.subl.setFont(QFont("Segoe UI", 25, QFont.Bold))
        self.subl.setAlignment(Qt.AlignCenter)
        self.subl.setGeometry(320, 45, 300, 60)
        self.subl.setStyleSheet("color: #1E2A38;")

        self.create_fun_card(90, 130, "../images/Su.jpeg", "Water Subscription", "Add Bill", self.show_water_form)
        self.create_fun_card(340, 130, "../images/elec.jpg", "Electricity Subscription", "Add Bill", self.show_electricity_form)
        self.create_fun_card(590, 130, "../images/clean.jpg", "Cleaning Subscription", "Add Bill", self.show_cleaning_form)
        self.create_fun_card(340, 420, "../images/gas.jpg", "Gas Subscription", "Add Bill", self.show_gas_form)

    def create_fun_card(self, x, y, image_path, title_text, button_text, button_action=None):
        card = QFrame(self)
        card.setGeometry(x, y, 220, 270)
        card.setStyleSheet("""
            QFrame {
                background-color: #fefefe;
                border-radius: 15px;
                border: 1px solid #ddd;
            }
        """)

        img = QLabel(card)
        img.setGeometry(10, 10, 200, 120)
        pixmap = QPixmap(image_path).scaled(200, 120, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        img.setPixmap(pixmap)
        img.setAlignment(Qt.AlignCenter)
        img.setStyleSheet("border-radius: 10px;")

        title = QLabel(title_text, card)
        title.setGeometry(10, 140, 200, 30)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 10, QFont.Bold))
        title.setStyleSheet("color: #333;")

        button = QPushButton(button_text, card)
        button.setGeometry(45, 200, 130, 40)
        button.setStyleSheet("""
            QPushButton {
                background-color: #ff5252;
                color: white;
                font-size: 20px;
                border: none;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #ff1744;
            }
        """)
        if button_action:
            button.clicked.connect(button_action)

    def show_water_form(self):
        self.water_form.show()

    def show_electricity_form(self):
        self.electric_form.show()

    def show_cleaning_form(self):
        self.clean_form.show()

    def show_gas_form(self):
        self.gas_form.show()


class Dashboard(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username

        self.setFixedSize(1244, 700)
        self.setWindowTitle("Dashboard")
        self.setWindowIcon(QIcon("../images/icon.png"))

        self.c = QFrame(self)
        self.setCentralWidget(self.c)
        self.setup_form()

    def setup_form(self):
        self.right_frame = QFrame(self.c)
        self.right_frame.setGeometry(350, 0, 894, 700)
        self.right_frame.setStyleSheet("background-color: #f1f2f6;")

        self.left_frame = QFrame(self.c)
        self.left_frame.setGeometry(0, 0, 350, 700)
        self.left_frame.setStyleSheet("background-color: #1E2A38;")

        self.label = QLabel(self.left_frame)
        pixmap = QPixmap("../images/icon2-Photoroom.png").scaled(220, 220, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)
        self.label.setGeometry(60, 5, pixmap.width(), pixmap.height())

        welcomL = QLabel(f"Hello {self.username}", self.left_frame)
        welcomL.setFont(QFont("Segoe UI", 18, QFont.Bold))
        welcomL.setAlignment(Qt.AlignCenter)
        welcomL.setGeometry(5, 190, 350, 60)
        welcomL.setStyleSheet("color: white;")

        button_style = """
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 25px;
                text-align: left;
                padding-left: 60px;
            }
            QPushButton:checked {
                background-color: rgba(255, 255, 255, 0.15);
                color: white;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.08);
            }
        """

        self.btn_main = QPushButton(" Main", self.left_frame)
        self.btn_main.setGeometry(0, 250, 350, 50)
        self.btn_main.setCheckable(True)
        self.btn_main.setStyleSheet(button_style)
        self.btn_main.setIcon(QIcon("../images/home.png"))
        self.btn_main.setIconSize(QSize(20, 20))

        self.btn_Subsc = QPushButton(" All Users", self.left_frame)
        self.btn_Subsc.setGeometry(0, 300, 350, 50)
        self.btn_Subsc.setCheckable(True)
        self.btn_Subsc.setStyleSheet(button_style)
        self.btn_Subsc.setIcon(QIcon("../images/pro.png"))
        self.btn_Subsc.setIconSize(QSize(22, 22))

        self.btn_service = QPushButton(" Users Activities", self.left_frame)
        self.btn_service.setGeometry(0, 350, 350, 50)
        self.btn_service.setCheckable(True)
        self.btn_service.setStyleSheet(button_style)
        self.btn_service.setIcon(QIcon("../images/m.png"))
        self.btn_service.setIconSize(QSize(22, 22))

        self.btn_signout = QPushButton(" Sign out", self.left_frame)
        self.btn_signout.setGeometry(0, 600, 350, 50)
        self.btn_signout.setCheckable(True)
        self.btn_signout.setStyleSheet(button_style)
        self.btn_signout.setIcon(QIcon("../images/out.png"))
        self.btn_signout.setIconSize(QSize(22, 22))

        def open_welcome():
            from user.welcome import WelcomeWindow
            self.welcome_window = WelcomeWindow()
            self.welcome_window.show()
            self.close()

        self.btn_signout.clicked.connect(open_welcome)

        self.stack = QStackedWidget(self.right_frame)
        self.stack.setGeometry(0, 0, 894, 700)

        self.page_main = Main(self.username)
        self.page_subs = ManageUsers()
        self.page_service = ManageRequests()

        self.stack.addWidget(self.page_main)
        self.stack.addWidget(self.page_subs)
        self.stack.addWidget(self.page_service)

        self.setup_button()

    def setup_button(self):
        self.btn_main.clicked.connect(lambda: self.switch_page(0, self.btn_main))
        self.btn_Subsc.clicked.connect(lambda: self.switch_page(1, self.btn_Subsc))
        self.btn_service.clicked.connect(lambda: self.switch_page(2, self.btn_service))
        self.switch_page(0, self.btn_main)

    def switch_page(self, index, active_button):
        self.stack.setCurrentIndex(index)
        for btn in [self.btn_main, self.btn_Subsc, self.btn_service]:
            btn.setChecked(btn == active_button)


if __name__ == "__main__":
    create_tables()
    app = QApplication(sys.argv)
    window = Dashboard("user")
    window.show()
    sys.exit(app.exec_())