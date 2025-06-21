 # Entry point for the PyQt application

import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
import os

if __name__ == "__main__":
    app = QApplication(sys.argv)

    style_path = os.path.join(os.path.dirname(__file__), 'assests', 'style.qss')
    with open(style_path, 'r') as style_file:
        style = style_file.read()
        app.setStyleSheet(style)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())