from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox
)
from database.queries import insert_event, update_event

class EventEditor(QDialog):
    def __init__(self, event=None):
        super().__init__()
        self.setWindowTitle("Edit Event" if event else "Add Event")
        self.setFixedSize(350, 200)

        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.name_input = QLineEdit()
        self.date_input = QLineEdit()
        self.location_input = QLineEdit()
        self.organizer_input = QLineEdit()

        self.layout.addRow("Name:", self.name_input)
        self.layout.addRow("Date (YYYY-MM-DD):", self.date_input)
        self.layout.addRow("Location:", self.location_input)
        self.layout.addRow("Organizer ID:", self.organizer_input)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_event)
        self.layout.addRow(save_btn)

        self.event = event
        if event:
            self.name_input.setText(event[1])
            self.date_input.setText(event[2].strftime("%Y-%m-%d"))
            self.location_input.setText(event[3])
            self.organizer_input.setText(str(event[5]))

    def save_event(self):
        name = self.name_input.text()
        date = self.date_input.text()
        location = self.location_input.text()
        organizer_id = self.organizer_input.text()

        if not name or not date or not organizer_id:
            QMessageBox.warning(self, "Missing Fields", "Please fill in all required fields.")
            return

        try:
            organizer_id = int(organizer_id)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Organizer ID must be a number.")
            return

        success = False
        if self.event:
            success = update_event(self.event[0], name, date, location, organizer_id)
        else:
            success = insert_event(name, date, location, organizer_id)

        if success:
            QMessageBox.information(self, "Success", "Event saved.")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to save event.")