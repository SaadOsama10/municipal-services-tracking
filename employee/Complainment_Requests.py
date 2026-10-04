import sys

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QMainWindow, QVBoxLayout, QScrollArea, QFrame,
    QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


class Complainment_Requests(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Municipal Services")
        self.setFixedSize(1000, 700)

        # Title label
        self.title = QLabel("Complains", self)
        # Frame for horizantal bar details
        self.bar = QFrame(self)
        self.bar_layout = QHBoxLayout(self.bar)

        self.name = QLabel("Name", self)
        self.details = QLabel("details", self)
        self.status = QLabel("status", self)
        self.veiw = QLabel("veiw", self)
        self.all_titles_inBar = [self.name, self.details, self.status, self.veiw]

        self.GU_Utin()
        self.setup_complaints_view()

    def setup_complaints_view(self):
        self.scroll = QScrollArea(self)  # Parent it to the main window
        self.scroll.setGeometry(30, 180, 940, 500)

        self.content = QFrame()
        self.layout = QVBoxLayout(self.content)

        self.dummy_data = [
            {"user": "Ali", "type": "Water Leak", "status": "Pending"},
            {"user": "Sara", "type": "Street Light", "status": "Resolved"},
            {"user": "Omar", "type": "Garbage", "status": "In Progress"},
            {"user": "Omar", "type": "Garbage", "status": "In Progress"},
            {"user": "Omar", "type": "Garbage", "status": "In Progress"},
            {"user": "Omar", "type": "Garbage", "status": "In Progress"},
            {"user": "Omar", "type": "Garbage", "status": "In Progress"},
            {"user": "Omar", "type": "Garbage", "status": "In Progress"},
            {"user": "Omar", "type": "Garbage", "status": "In Progress"},
            {"user": "Omar", "type": "Garbage", "status": "In Progress"},
            {"user": "Omar", "type": "Garbage", "status": "In Progress"},
            {"user": "Omar", "type": "Garbage", "status": "In Progress"},
            {"user": "Omar", "type": "Garbage", "status": "In Progress"},
            {"user": "Omar", "type": "Garbage", "status": "In Progress"},
            {"user": "Omar", "type": "Garbage", "status": "In Progress"}]

        for complaint in self.dummy_data:
            row = QFrame()
            row.setStyleSheet("border: 1px solid #ccc;")
            row_layout = QHBoxLayout(row)

            name = QLabel(complaint["user"])
            complaint_type = QLabel(complaint["type"])
            status = QLabel(complaint["status"])
            btn = QPushButton("View")

            for widget in [name, complaint_type, status, btn]:
                widget.setFixedWidth(150)
                widget.setFixedHeight(40)
                widget.setStyleSheet("color: #196297;"
                                     "font: 17px Arial, sans-serif;"
                                     "border:none;")
                row_layout.addWidget(widget)

            self.layout.addWidget(row)

        self.scroll.setWidget(self.content)
        self.scroll.setWidgetResizable(True)

    def GU_Utin(self):
        self.title.setGeometry(400, 30, 400, 50)
        self.title.setStyleSheet("color: #196297;"
                            "font: 32px Arial, sans-serif;")


        self.bar.setStyleSheet("border: 1px solid #ccc;")
        self.bar.setGeometry(30,100, 940, 70)
        for widjet in self.all_titles_inBar:
            self.bar_layout.addWidget(widjet)
            widjet.setStyleSheet("color: #196297;"
                            "font: 20px Arial, sans-serif;"
                            "border:none;"
                            "margin-left:30px")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Complainment_Requests()
    window.show()
    sys.exit(app.exec_())