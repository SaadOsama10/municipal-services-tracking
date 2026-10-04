from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox
from PyQt5.QtCore import Qt
from functools import partial
from db_manager import get_all_user_requests_info, update_request_status


class ManageRequests(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(894, 700)
        self.setWindowTitle("Manage Requests")

        self.table = QTableWidget(self)
        self.table.setGeometry(20, 20, 850, 650)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Username", "Complaint", "Request", "Suggestion", "Status"])

        self.load_data()

    def load_data(self):
        data = get_all_user_requests_info()
        self.table.setRowCount(0)

        for row_idx, (username, complaint, request, suggestion, request_id, status) in enumerate(data):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(username))
            self.table.setItem(row_idx, 1, QTableWidgetItem(complaint))
            self.table.setItem(row_idx, 2, QTableWidgetItem(request))
            self.table.setItem(row_idx, 3, QTableWidgetItem(suggestion))

            combo = QComboBox()
            combo.addItems(["Pending", "Approved", "Rejected", "In Progress", "Closed"])
            combo.setCurrentText(status)

            if request_id:
                combo.currentTextChanged.connect(partial(self.update_status, request_id))
            else:
                combo.setEnabled(False)

            self.table.setCellWidget(row_idx, 4, combo)

    def update_status(self, request_id, new_status):
        try:
            update_request_status(request_id, new_status)
            QMessageBox.information(self, "Status Updated", f"Request ID {request_id} updated to '{new_status}'.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
