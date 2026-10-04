import sys
import matplotlib.pyplot as plt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Reborts(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard Chart")
        self.setGeometry(100, 100, 500, 500)
        layout = QVBoxLayout()


        labels = ["Services", "Complaints", "Invoices", "Suggestions"]
        values = [150, 50, 75, 25]
        colors = ['#4285F4', '#FB8C00', '#34A853', '#9C27B0']

        fig = Figure(figsize=(2.5, 2.5))  # بدلاً من (4, 4)

        ax = fig.add_subplot(111)
        ax.pie(
            values,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            pctdistance=0.85,
            radius=0.7  # 👈 هذا هو المفتاح لتصغير حجم الدائرة
        )
        ax.add_artist(plt.Circle((0, 0), 0.4, color='white'))  # وسط فارغ

        ax.text(0, 0, f"{sum(values)}\nTotal", ha='center', va='center', fontsize=12)

        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        self.setLayout(layout)



        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Type", "Date", "Status", "Duration", "Amount ($)"])
        self.table.setFont(QFont("Arial", 12))
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)

        layout.addWidget(self.table)
        self.setLayout(layout)

        self.load_data()

    def load_data(self):
        data = [
            {"type": "Water Leak", "date": "01/05/2025", "status": "✅ Done", "duration": "2 days", "amount": 15},
            {"type": "Garbage", "date": "03/05/2025", "status": "❌ Pending", "duration": "-", "amount": 10},
            {"type": "Complaint", "date": "05/05/2025", "status": "🟢 Resolved", "duration": "1 day", "amount": "-"},
            {"type": "Invoice", "date": "06/05/2025", "status": "💰 Paid", "duration": "-", "amount": 25},
        ]

        self.table.setRowCount(len(data))

        for row, entry in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(entry["type"]))
            self.table.setItem(row, 1, QTableWidgetItem(entry["date"]))
            self.table.setItem(row, 2, QTableWidgetItem(entry["status"]))
            self.table.setItem(row, 3, QTableWidgetItem(entry["duration"]))
            self.table.setItem(row, 4, QTableWidgetItem(str(entry["amount"])))
