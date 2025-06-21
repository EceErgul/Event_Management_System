from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt
from database.queries import fetch_all_events, delete_event
from utils.exporter import export_events_to_csv
from ui.event_manager import EventManager
from ui.registration_view import RegistrationView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Campus Events Dashboard")
        self.setGeometry(100, 100, 800, 600)

        container = QWidget()
        self.layout = QVBoxLayout(container)

        self.header = QLabel("📅 Upcoming Events")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.header)

        self.event_table = QTableWidget()
        self.event_table.setColumnCount(4)
        self.event_table.setHorizontalHeaderLabels(["Name", "Date", "Location", "Organizer"])
        self.event_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.layout.addWidget(self.event_table)

        button_row = QHBoxLayout()
        self.manage_events_btn = QPushButton("🗂 Manage Events")
        self.export_btn = QPushButton("📤 Export Events")
        self.delete_btn = QPushButton("🗑️ Delete Selected")

        button_row.addWidget(self.manage_events_btn)
        button_row.addWidget(self.export_btn)
        button_row.addWidget(self.delete_btn)
        self.layout.addLayout(button_row)

        self.setCentralWidget(container)

        # Connect buttons
        self.manage_events_btn.clicked.connect(self.open_event_manager)
        self.export_btn.clicked.connect(self.export_data)
        self.delete_btn.clicked.connect(self.delete_selected_event)
        self.event_table.itemDoubleClicked.connect(self.show_event_participants)

        self.load_events()

    def load_events(self):
        self.events = fetch_all_events()
        self.event_table.setRowCount(len(self.events))
        for row, event in enumerate(self.events):
            self.event_table.setItem(row, 0, QTableWidgetItem(event[1]))
            self.event_table.setItem(row, 1, QTableWidgetItem(event[2].strftime("%Y-%m-%d")))
            self.event_table.setItem(row, 2, QTableWidgetItem(event[3]))
            self.event_table.setItem(row, 3, QTableWidgetItem(event[4]))

    def get_selected_event(self):
        row = self.event_table.currentRow()
        return self.events[row] if row >= 0 else None

    def delete_selected_event(self):
        selected = self.get_selected_event()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select an event to delete.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete:\n\n{selected[1]}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            if delete_event(selected[0]):
                QMessageBox.information(self, "Deleted", "Event deleted.")
                self.load_events()
            else:
                QMessageBox.warning(self, "Error", "Could not delete event.")

    def export_data(self):
        path = export_events_to_csv()
        QMessageBox.information(self, "Exported", f"Events exported to:\n{path}")

    def open_event_manager(self):
        dlg = EventManager()
        if dlg.exec():
            self.load_events()

    def show_event_participants(self):
        selected = self.get_selected_event()
        if selected:
            dlg = RegistrationView(event_id=selected[0])
            dlg.exec()