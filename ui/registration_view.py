from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QLineEdit, QFormLayout
)
from database.queries import (
    fetch_participants_by_event, insert_event_registration,
    update_event_registration, delete_event_registration
)

class ParticipantForm(QDialog):
    def __init__(self, participant=None):
        super().__init__()
        self.setWindowTitle("Participant Details")
        self.layout = QFormLayout(self)
        self.name_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.status_edit = QLineEdit()
        self.attendance_edit = QLineEdit()
        self.layout.addRow("Name:", self.name_edit)
        self.layout.addRow("Email:", self.email_edit)
        self.layout.addRow("Status:", self.status_edit)
        self.layout.addRow("Attendance (True/False):", self.attendance_edit)

        if participant:
            self.name_edit.setText(participant[1])
            self.email_edit.setText(participant[2])
            self.status_edit.setText(participant[3])
            self.attendance_edit.setText(str(participant[4]))

        buttons = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)
        self.layout.addRow(buttons)

        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

    def get_data(self):
        return (
            self.name_edit.text(),
            self.email_edit.text(),
            self.status_edit.text(),
            self.attendance_edit.text().lower() == "true"
        )

class RegistrationView(QDialog):
    def __init__(self, event_id):
        super().__init__()
        self.setWindowTitle("Event Participants")
        self.resize(700, 400)
        self.event_id = event_id

        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Email", "Status", "Attendance"])
        self.layout.addWidget(self.table)

        btns = QHBoxLayout()
        self.add_btn = QPushButton("➕ Add")
        self.edit_btn = QPushButton("✏️ Edit")
        self.delete_btn = QPushButton("🗑️ Delete")
        for b in (self.add_btn, self.edit_btn, self.delete_btn):
            btns.addWidget(b)
        self.layout.addLayout(btns)
        self.setLayout(self.layout)

        self.add_btn.clicked.connect(self.add_participant)
        self.edit_btn.clicked.connect(self.edit_participant)
        self.delete_btn.clicked.connect(self.delete_participant)

        self.load_participants()

    def load_participants(self):
        self.participants = fetch_participants_by_event(self.event_id)
        self.table.setRowCount(len(self.participants))
        for row, p in enumerate(self.participants):
            self.table.setItem(row, 0, QTableWidgetItem(p[1]))
            self.table.setItem(row, 1, QTableWidgetItem(p[2]))
            self.table.setItem(row, 2, QTableWidgetItem(p[3]))
            self.table.setItem(row, 3, QTableWidgetItem("✔️" if p[4] else "❌"))

    def get_selected(self):
        row = self.table.currentRow()
        return self.participants[row] if row >= 0 else None

    def add_participant(self):
        form = ParticipantForm()
        if form.exec():
            name, email, status, attendance = form.get_data()
            if insert_event_registration(self.event_id, name, email, status, attendance):
                self.load_participants()
            else:
                QMessageBox.warning(self, "Error", "Insert failed.")

    def edit_participant(self):
        selected = self.get_selected()
        if not selected:
            return
        form = ParticipantForm(selected)
        if form.exec():
            name, email, status, attendance = form.get_data()
            if update_event_registration(selected[0], name, email, status, attendance):
                self.load_participants()
            else:
                QMessageBox.warning(self, "Error", "Update failed.")

    def delete_participant(self):
        selected = self.get_selected()
        if not selected:
            return
        confirm = QMessageBox.question(self, "Confirm", f"Remove {selected[1]} from event?")
        if confirm == QMessageBox.StandardButton.Yes:
            if delete_event_registration(selected[0], self.event_id):
                self.load_participants()