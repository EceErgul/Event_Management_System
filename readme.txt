# Directory Structure (Simplified)

Event_Management_System/
│
├── main.py                 # Entry point for the PyQt application
├── assets/
│   └── style.qss           # Global stylesheet for UI appearance
│
├── database/
│   ├── db_connection.py    # PostgreSQL connection setup
│   └── queries.py          # CRUD query functions
│
├── ui/
│   ├── main_window.py      # Central dashboard with event table
│   ├── event_manager.py    # Manage event list
│   ├── event_editor.py     # Form to add/edit individual events
│   └── registration_view.py # View & manage participants per event
│
├── utils/
    └── exporter.py         # CSV export functionality
