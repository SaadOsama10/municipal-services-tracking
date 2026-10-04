from PyQt5.QtWidgets import (
    QFrame, QLabel, QComboBox, QPlainTextEdit, QLineEdit,
    QPushButton, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import os

from db_manager import insert_service_request, get_user_id, create_tables


class Service(QFrame):
    def __init__(self, username):
        super().__init__()
        self.setStyleSheet("background-color: white;")
        self.setGeometry(0, 0, 894, 700)

        self.username = username
        self.user_id = get_user_id(username)
        self.selected_image_path = ""
        self.setup_ui()
        create_tables()

    def setup_ui(self):
        self.setup_title()
        self.setup_form()
        self.setup_image_section()
        self.setup_submit_button()

    def setup_title(self):
        self.title_label = QLabel("Make a Service", self)
        self.title_label.setFont(QFont("Arial", 25))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setGeometry(300, 20, 310, 100)
        self.title_label.setStyleSheet("color: #196297;background-color: transparent;")

    def setup_form(self):
        self.photo = QLabel(self)
        self.photo.setGeometry(0, 0, self.width(), self.height())
        self.photo.setPixmap(
            QPixmap("../images/back2.jpg").scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        self.photo.lower()

        label_font = QFont("Arial", 15)

        self.typel = QLabel("Service Type :", self)
        self.typel.setFont(label_font)
        self.typel.setGeometry(20, 130, 200, 50)
        self.typel.setStyleSheet("color: #196297;background-color: transparent;")

        self.type_combo = QComboBox(self)
        self.type_combo.setGeometry(250, 130, 300, 50)
        self.type_combo.setStyleSheet("""
            background-color: #196297;
            font-size: 20px;
            color: white;
        """)
        self.type_combo.addItems([
            "Garbage Collection", "Street Light Repair", "Water Leak",
            "Pothole Repair", "Tree Trimming", "Road Line Painting"
        ])

        self.descriptionl = QLabel("Description :", self)
        self.descriptionl.setFont(label_font)
        self.descriptionl.setGeometry(20, 200, 200, 50)
        self.descriptionl.setStyleSheet("color: #196297;background-color: transparent;")

        self.description = QPlainTextEdit(self)
        self.description.setPlaceholderText("Explain the problem here")
        self.description.setGeometry(250, 200, 300, 150)
        self.description.setStyleSheet("color: #196297;background-color: transparent;")

        self.addressl = QLabel("Address :", self)
        self.addressl.setFont(label_font)
        self.addressl.setGeometry(20, 380, 200, 50)
        self.addressl.setStyleSheet("color: #196297;background-color: transparent;")

        self.address = QLineEdit(self)
        self.address.setPlaceholderText("Your address")
        self.address.setGeometry(250, 380, 300, 50)
        self.address.setStyleSheet("font-size: 20px;")

    def setup_image_section(self):
        label_font = QFont("Arial", 15)

        self.image_label = QLabel("Image for\nyour problem :", self)
        self.image_label.setFont(label_font)
        self.image_label.setGeometry(20, 520, 200, 100)
        self.image_label.setStyleSheet("color: #196297;background-color: transparent;")

        self.photo_label = QLabel(self)
        default_image = "../images/pro.jpg"
        if os.path.exists(default_image):
            pixmap = QPixmap(default_image)
            self.photo_label.setPixmap(pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.photo_label.setText("No Image")
        self.photo_label.setGeometry(250, 500, 200, 150)
        self.photo_label.setAlignment(Qt.AlignCenter)

        self.browse_button = QPushButton("Browse", self)
        self.browse_button.setGeometry(500, 580, 100, 50)
        self.browse_button.setStyleSheet("""
            background-color: #196297;
            font-size: 20px;
            color: white;
            border-radius: 20px;
        """)
        self.browse_button.clicked.connect(self.open_image)

    def setup_submit_button(self):
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.setGeometry(740, 550, 140, 140)
        self.submit_button.setStyleSheet("""
            background-color: #196297;
            font-size: 25px;
            color: white;
            border-radius: 70px;
        """)
        self.submit_button.clicked.connect(self.handle_submit)

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_name:
            self.selected_image_path = file_name
            pixmap = QPixmap(file_name)
            self.photo_label.setPixmap(
                pixmap.scaled(self.photo_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.photo_label.setAlignment(Qt.AlignCenter)

    def handle_submit(self):
        service_type = self.type_combo.currentText()
        description = self.description.toPlainText()
        address = self.address.text()
        image_path = self.selected_image_path if hasattr(self, 'selected_image_path') else ""

        if not description.strip() or not address.strip():
            QMessageBox.warning(self, "Input Error", "Please fill all fields.")
            return

        insert_service_request(self.user_id, service_type, description, address, image_path)
        QMessageBox.information(self, "Success", "Service request submitted successfully.")
        self.clear_form()

    def clear_form(self):
        self.description.clear()
        self.address.clear()
        self.type_combo.setCurrentIndex(0)
        self.photo_label.clear()
        self.photo_label.setText("No Image")
        self.selected_image_path = ""
