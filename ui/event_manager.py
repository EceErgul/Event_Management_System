from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox
)
from database.queries import fetch_all_events, delete_event
from ui.event_editor import EventEditor

class EventManager(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Event Manager")
        self.resize(700, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        btns = QHBoxLayout()
        self.add_btn = QPushButton("➕ Add Event")
        self.edit_btn = QPushButton("✏️ Edit Selected")
        self.delete_btn = QPushButton("🗑️ Delete Selected")

        for b in (self.add_btn, self.edit_btn, self.delete_btn):
            btns.addWidget(b)
        self.layout.addLayout(btns)

        self.add_btn.clicked.connect(self.add_event)
        self.edit_btn.clicked.connect(self.edit_event)
        self.delete_btn.clicked.connect(self.delete_event)

        self.load_data()

    def load_data(self):
        self.events = fetch_all_events()
        self.table.setRowCount(len(self.events))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Date", "Location", "Organizer"])
        for row, e in enumerate(self.events):
            self.table.setItem(row, 0, QTableWidgetItem(e[1]))
            self.table.setItem(row, 1, QTableWidgetItem(e[2].strftime("%Y-%m-%d")))
            self.table.setItem(row, 2, QTableWidgetItem(e[3]))
            self.table.setItem(row, 3, QTableWidgetItem(str(e[4])))
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def get_selected_event(self):
        row = self.table.currentRow()
        return self.events[row] if row >= 0 else None

    def add_event(self):
        editor = EventEditor(None)
        if editor.exec():
            self.load_data()

    def edit_event(self):
        selected = self.get_selected_event()
        if selected:
            editor = EventEditor(selected)
            if editor.exec():
                self.load_data()

    def delete_event(self):
        selected = self.get_selected_event()
        if not selected:
            QMessageBox.warning(self, "Select an Event", "Choose an event to delete.")
            return
        confirm = QMessageBox.question(
            self, "Confirm Deletion", f"Delete event: {selected[1]}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            if delete_event(selected[0]):
                self.load_data()
            else:
                QMessageBox.warning(self, "Error", "Could not delete event.")