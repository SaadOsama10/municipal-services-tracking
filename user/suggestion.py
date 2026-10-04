from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QComboBox, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt

from db_manager import insert_suggestion, get_user_id


class Suggestion(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.user_id = get_user_id(username)

        self.resize(910, 840)
        self.setWindowTitle("Suggestions")
        self.setWindowIcon(QIcon("../images/icon.png"))

        self.welcomL = QLabel("Share your Suggestion", self)
        self.label1 = QLabel("Suggestion :", self)
        self.label2 = QLabel("Categories : ", self)
        self.label3 = QLabel("Proposed Solution :", self)
        self.label4 = QLabel("PlaceHolder : ", self)

        self.field1 = QLineEdit(self)
        self.field2 = QLineEdit(self)
        self.field3 = QLineEdit(self)

        self.combo_box = QComboBox(self)
        self.send_button = QPushButton("Send", self)

        self.all_labels = [self.label1, self.label2, self.label3, self.label4]
        self.all_fields = [self.field1, self.field2, self.field3]

        self.GU_Utin()

    def GU_Utin(self):
        self.photo = QLabel(self)
        self.photo.setGeometry(0, 0, self.width(), self.height())
        self.photo.setPixmap(QPixmap("../images/back2.jpg").scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        self.photo.lower()

        self.welcomL.setFont(QFont("Arial", 24))
        self.welcomL.setAlignment(Qt.AlignCenter)
        self.welcomL.setGeometry(280, 20, 400, 100)
        self.welcomL.setStyleSheet("color: #196297;background-color: transparent;")

        self.label1.setGeometry(200, 240, 150, 20)
        self.label2.setGeometry(200, 300, 150, 20)
        self.label3.setGeometry(200, 360, 150, 20)
        self.label4.setGeometry(200, 420, 150, 20)

        field_width = 270
        self.field1.setGeometry(450, 240, field_width, 35)
        self.combo_box.setGeometry(450, 300, field_width, 35)
        self.field2.setGeometry(450, 360, field_width, 35)
        self.field3.setGeometry(450, 420, field_width, 35)

        for i in self.all_labels:
            i.setFont(QFont("Arial", 16))
            i.setStyleSheet("color: #196297;")

        for j in self.all_fields:
            j.setStyleSheet("""
                color: #196297;
                border: 2px solid #196297;
                padding: 10px;
                border-radius: 5px;
            """)

        self.combo_box.setStyleSheet("""
            background-color: #196297;
            font-size: 16px;
            color: white;
        """)
        self.combo_box.addItems([
            "UI Improvment", "Service Enhancement", "New Feature Proposal", "Recurring Issues", "Other"
        ])

        self.send_button.setGeometry(200, 520, 540, 50)
        self.send_button.setStyleSheet("""
            background-color: #196297;
            border: 2px solid white;
            padding: 10px;
            border-radius: 3px;
            color: white;
            font-size: 2rem;
        """)
        self.send_button.clicked.connect(self.Sendbutton)

    def Sendbutton(self):
        suggestion = self.field1.text().strip()
        category = self.combo_box.currentText()
        proposed_solution = self.field2.text().strip()
        placeholder = self.field3.text().strip()

        if not suggestion or not proposed_solution or not placeholder:
            QMessageBox.warning(self, "Input Error", "Please fill in all the fields.")
            return

        insert_suggestion(self.user_id, suggestion, category, proposed_solution, placeholder)
        QMessageBox.information(self, "Success", "Suggestion submitted successfully.")

        self.field1.clear()
        self.field2.clear()
        self.field3.clear()
        self.combo_box.setCurrentIndex(0)
