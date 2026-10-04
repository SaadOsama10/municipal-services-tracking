from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QTextEdit, QSpinBox,
    QFrame, QPushButton, QVBoxLayout, QMainWindow, QStackedWidget, QCheckBox, QApplication
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from user.complainment import Complainment
from suggestion import Suggestion
from user.service import Service
from profile import Profile
import sys
from db_manager import *
from subsucribtion_panels import *
from my_sub import UserSubscriptions
from welcome import WelcomeWindow


class Main(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username

        self.subl = QLabel("Subscriptions", self)
        self.subl.setFont(QFont("Segoe UI", 25, QFont.Bold))
        self.subl.setAlignment(Qt.AlignCenter)
        self.subl.setGeometry(320, 45, 300, 60)
        self.subl.setStyleSheet("color: #1E2A38;")

        self.water_form = WaterSubscriptionForm(self.username)
        self.electricity_form = ElectricitySubscriptionForm(self.username)
        self.cleaning_form = CleaningSubscriptionForm(self.username)
        self.gas_form = GasSubscriptionForm(self.username)
        self.visa_form = VisaDigitalForm(self.username)

        self.create_fun_card(90, 130, "../images/Su.jpeg", "Water Subscription", "Subscribe", self.show_water_form)
        self.create_fun_card(340, 130, "../images/elec.jpg", "Electricity Subscription", "Subscribe",
                             self.show_electricity_form)
        self.create_fun_card(590, 130, "../images/clean.jpg", "Cleaning Subscription", "Subscribe",
                             self.show_cleaning_form)
        self.create_fun_card(90, 420, "../images/gas.jpg", "Gas Subscription", "Subscribe", self.show_gas_form)
        self.create_fun_card(340, 420, "../images/visa.jpg", "Visa Digital", "Subscribe", self.show_visa_form)
        self.create_fun_card(590, 420, "../images/statf.jpeg", "Staff", "View", self.view)

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
        self.water_form.raise_()
        self.water_form.setVisible(True)

    def show_electricity_form(self):
        self.electricity_form.raise_()
        self.electricity_form.setVisible(True)

    def show_cleaning_form(self):
        self.cleaning_form.raise_()
        self.cleaning_form.setVisible(True)

    def show_gas_form(self):
        self.gas_form.raise_()
        self.gas_form.setVisible(True)

    def show_visa_form(self):
        self.visa_form.raise_()
        self.visa_form.setVisible(True)

    def view(self):
        information = '''
                <h2 style="color:#196297; text-align:center;">The Staff</h2>
                <p style="font-size:14px; color:#333333; text-align:justify;">
        The individuals who completed this project are Saed O. S. Radi, Abdulrahman Zeineddin, and Kinan Al-Imam. </p>'''

        QMessageBox.about(self, "Municipal Services Tracking", information)


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

        self.btn_Subsc = QPushButton(" My Subscriptions", self.left_frame)
        self.btn_Subsc.setGeometry(0, 300, 350, 50)
        self.btn_Subsc.setCheckable(True)
        self.btn_Subsc.setStyleSheet(button_style)
        self.btn_Subsc.setIcon(QIcon("../images/m.png"))
        self.btn_Subsc.setIconSize(QSize(22, 22))

        self.btn_service = QPushButton(" Service Request", self.left_frame)
        self.btn_service.setGeometry(0, 350, 350, 50)
        self.btn_service.setCheckable(True)
        self.btn_service.setStyleSheet(button_style)
        self.btn_service.setIcon(QIcon("../images/ser.png"))
        self.btn_service.setIconSize(QSize(22, 22))

        self.btn_complaint = QPushButton(" Complaint", self.left_frame)
        self.btn_complaint.setGeometry(0, 400, 350, 50)
        self.btn_complaint.setCheckable(True)
        self.btn_complaint.setStyleSheet(button_style)
        self.btn_complaint.setIcon(QIcon("../images/cons.png"))
        self.btn_complaint.setIconSize(QSize(22, 22))

        self.btn_suggestion = QPushButton(" Suggestion", self.left_frame)
        self.btn_suggestion.setGeometry(0, 450, 350, 50)
        self.btn_suggestion.setCheckable(True)
        self.btn_suggestion.setStyleSheet(button_style)
        self.btn_suggestion.setIcon(QIcon("../images/suggestion.png"))
        self.btn_suggestion.setIconSize(QSize(22, 22))

        self.btn_profile = QPushButton(" Profile", self.left_frame)
        self.btn_profile.setGeometry(0, 500, 350, 50)
        self.btn_profile.setCheckable(True)
        self.btn_profile.setStyleSheet(button_style)
        self.btn_profile.setIcon(QIcon("../images/pro.png"))
        self.btn_profile.setIconSize(QSize(22, 22))

        self.btn_signout = QPushButton(" Sign out", self.left_frame)
        self.btn_signout.setGeometry(0, 600, 350, 50)
        self.btn_signout.setCheckable(True)
        self.btn_signout.setStyleSheet(button_style)
        self.btn_signout.setIcon(QIcon("../images/out.png"))
        self.btn_signout.setIconSize(QSize(22, 22))

        self.btn_signout.clicked.connect(self.open_welcome)

        self.stack = QStackedWidget(self.right_frame)
        self.stack.setGeometry(0, 0, 894, 700)

        self.page_main = Main(self.username)
        self.page_subs = UserSubscriptions(self.username)
        self.page_subs.table.clear()

        self.page_subs.load_data()
        self.page_service = Service(self.username)
        self.page_complaint = Complainment(self.username)
        self.page_suggestion = Suggestion(self.username)
        self.page_profile = Profile(self.username)

        self.stack.addWidget(self.page_main)
        self.stack.addWidget(self.page_subs)
        self.stack.addWidget(self.page_service)
        self.stack.addWidget(self.page_complaint)
        self.stack.addWidget(self.page_suggestion)
        self.stack.addWidget(self.page_profile)

        self.setup_button()

    def setup_button(self):
        self.btn_main.clicked.connect(lambda: self.switch_page(0, self.btn_main))
        self.btn_Subsc.clicked.connect(lambda: self.switch_page(1, self.btn_Subsc))
        self.btn_service.clicked.connect(lambda: self.switch_page(2, self.btn_service))
        self.btn_complaint.clicked.connect(lambda: self.switch_page(3, self.btn_complaint))
        self.btn_suggestion.clicked.connect(lambda: self.switch_page(4, self.btn_suggestion))
        self.btn_profile.clicked.connect(lambda: self.switch_page(5, self.btn_profile))

        self.switch_page(0, self.btn_main)

    def switch_page(self, index, active_button):
        self.stack.setCurrentIndex(index)
        for btn in [
            self.btn_main, self.btn_Subsc, self.btn_service,
            self.btn_complaint, self.btn_suggestion, self.btn_profile,
        ]:
            btn.setChecked(btn == active_button)

    def open_welcome(self):
        self.welcome_window = WelcomeWindow()
        self.welcome_window.show()
        self.close()

#
# if __name__ == "__main__":
#     create_tables()
#     app = QApplication(sys.argv)
#     window = Dashboard(self.username)
#     window.show()
#     sys.exit(app.exec_())
