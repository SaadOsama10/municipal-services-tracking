from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QLabel
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from functools import partial

from db_manager import get_all_users, update_user, delete_user_by_id


class ManageUsers(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Users")
        self.setGeometry(100, 100, 1100, 840)
        self.setFixedSize(894, 700)
        self.setWindowIcon(QIcon("../images/icon.png"))


        self.photo = QLabel(self)
        self.photo.setGeometry(0, 0, self.width(), self.height())
        self.photo.setPixmap(QPixmap("../images/back2.jpg").scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        self.photo.lower()

        self.table = QTableWidget(self)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Username", "Name", "Surname", "New password (optional)", "Edit", "Delete"])
        self.table.setGeometry(50, 50, 750, 400)

        self.load_users()

        self.show()

    def load_users(self):
        self.table.setRowCount(0)  # Clear previous rows
        users = get_all_users()
        self.table.setRowCount(len(users))

        for row_idx, user in enumerate(users):
            user_id, username, name, surname = user

            # ID - read-only
            id_item = QTableWidgetItem(str(user_id))
            id_item.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(row_idx, 0, id_item)

            username_item = QTableWidgetItem(username)
            username_item.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(row_idx, 1, username_item)

            self.table.setItem(row_idx, 2, QTableWidgetItem(name))
            self.table.setItem(row_idx, 3, QTableWidgetItem(surname))
            # Passwords are stored hashed and never shown; type a new one here to reset it
            self.table.setItem(row_idx, 4, QTableWidgetItem(""))

            # Edit Button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(partial(self.edit_user, row_idx))
            self.table.setCellWidget(row_idx, 5, edit_btn)
            edit_btn.setStyleSheet("background-color: #196297; padding: 8px; color: white;")

            # Delete Button
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet("background-color: #196297; padding: 8px; color: white;")
            delete_btn.clicked.connect(partial(self.delete_user, user_id))
            self.table.setCellWidget(row_idx, 6, delete_btn)

    def edit_user(self, row):
        try:
            user_id = int(self.table.item(row, 0).text())
            name = self.table.item(row, 2).text()
            surname = self.table.item(row, 3).text()
            password = self.table.item(row, 4).text().strip()

            update_user(user_id, name, surname, password)
            self.table.item(row, 4).setText("")
            QMessageBox.information(self, "Success", "User updated successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def delete_user(self, user_id):
        reply = QMessageBox.question(self, 'Confirm', f"Are you sure to delete user ID {user_id}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            delete_user_by_id(user_id)
            QMessageBox.information(self, "Deleted", "User deleted.")
            self.load_users()
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = ManageUsers()
    sys.exit(app.exec_())