from PyQt5.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QLabel, QFrame, QHBoxLayout, QLineEdit,
    QDialog, QVBoxLayout
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from functools import partial

from Show_Requests import ViewRequestsWindow
from kinan_manager import get_all_users, update_user, delete_user_by_id


class Requests(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Requests")
        self.setGeometry(0, 0, 1100, 840)
        self.setWindowIcon(QIcon("../images/icon.png"))

        self.photo = QLabel(self)
        self.photo.setGeometry(0, 0, self.width(), self.height())
        self.photo.setPixmap(
            QPixmap("../images/back2.jpg").scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        self.photo.lower()

        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["User Id", "Username", "Name", "Surname", "View"])
        self.table.setGeometry(50, 40, 1000, 400)

        # Content frame :
        self.set_content()
        # Starting some functions:
        self.load_users()
        self.show()

    def load_users(self):
        self.table.setRowCount(0)  # Clear table first
        users = get_all_users()
        self.table.setRowCount(len(users))

        for row_idx, user in enumerate(users):
            user_id, username, name, surname = user

            self.table.setItem(row_idx, 0, QTableWidgetItem(str(user_id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(username))
            self.table.setItem(row_idx, 2, QTableWidgetItem(name))
            self.table.setItem(row_idx, 3, QTableWidgetItem(surname))

            # View Button
            view_btn = QPushButton("View")
            view_btn.clicked.connect(self.make_view_handler(user_id))
            view_btn.setStyleSheet("background-color: #196297; padding: 8px; color: white;")

            self.table.setCellWidget(row_idx, 4, view_btn)

    def make_view_handler(self, user_id):
        return lambda: self.view_requests(user_id)

    def view_requests(self, user_id):
        users = get_all_users()
        self.table.setRowCount(len(users))

        for row_idx, user in enumerate(users):
            user_id, username, name, surname, _ =  user
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(user_id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(username))
            self.table.setItem(row_idx, 2, QTableWidgetItem(name))
            self.table.setItem(row_idx, 3, QTableWidgetItem(surname))

            view_button = QPushButton("View")
            view_button.clicked.connect(lambda _, uid=user_id: self.open_view_window(uid))
            self.table.setCellWidget(row_idx, 4, view_button)

    def open_view_window(self, user_id):
        self.view_window = ViewRequestsWindow(user_id)
        self.view_window.show()


    def search_user_by_id(self):
        user_id = self.User_textfield.text().strip()

        if not user_id.isdigit():
            return  # Optionally, show a message box for invalid input

        users = get_all_users()
        self.table.setRowCount(0)  # Clear existing table
        for user in users:
            if str(user[0]) == user_id:  # Match user ID
                row_idx = 0
                self.table.setRowCount(1)

                self.table.setItem(row_idx, 0, QTableWidgetItem(str(user[0])))
                self.table.setItem(row_idx, 1, QTableWidgetItem(user[1]))
                self.table.setItem(row_idx, 2, QTableWidgetItem(user[2]))
                self.table.setItem(row_idx, 3, QTableWidgetItem(user[3]))

                view_button = QPushButton("View")
                view_button.clicked.connect(lambda _, uid=user[0]: self.open_view_window(uid))
                self.table.setCellWidget(row_idx, 4, view_button)
                break



    def set_content(self):
        # Main container setup
        self.content = QFrame(self)
        self.content.setGeometry(50, 460, 1000, 200)  # Position/size first
        self.content.setStyleSheet("""
            border: 2px solid blue;
            background-color: white;  /* Optional: Add background */
        """)

        # Layout setup
        self.content_layout = QHBoxLayout(self.content)
        self.content_layout.setContentsMargins(10, 10, 10, 10)  # Add padding
        self.content_layout.setSpacing(15)  # Space between widgets

        # Buttons (aligned and styled)

        self.show_user_status = QPushButton("Show User")
        self.show_user_status.clicked.connect(self.search_user_by_id)
        self.show_user_status.setStyleSheet("""
                   
                       padding: 10px;
                       margin-left: 100px;
                       font-weight: bold;
                       min-width: 100px;
                       background-color: #196297;
                       color: white;
                                   
               """)

        # Text field
        self.User_textfield = QLineEdit()
        self.User_textfield.setPlaceholderText("Enter user ID...")
        self.User_textfield.resize(200, 40)

        self.User_textfield.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                margin-left: 100px;
                min-width: 120px;

            }
        """)

        # Add widgets to layout (logical order)

        self.content_layout.addWidget(self.User_textfield)
        self.content_layout.addWidget(self.show_user_status)

        # Optional: Add stretch to push buttons left or right
        self.content_layout.addStretch()  # Pushes all widgets to the left
        #####
        self.reset_button = QPushButton("Reset", self)
        self.reset_button.setGeometry(370, 10, 100, 30)
        self.reset_button.clicked.connect(self.load_users)
        self.content_layout.addWidget(self.reset_button)
        self.reset_button.setStyleSheet("""
                   
                       padding: 10px;
                       margin-left: 100px;
                       font-weight: bold;
                       min-width: 100px;
                       background-color: #196297;
                       color: white;
                                   
               """)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = Requests()
    sys.exit(app.exec_())
# Requests
