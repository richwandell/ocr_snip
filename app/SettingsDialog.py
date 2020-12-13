import sys

from PyQt5.QtWidgets import QApplication

from app.SettingsMainWindow import SettingsMainWindow


class SettingsDialog:

    def __init__(self):
        app = QApplication(sys.argv)
        window = SettingsMainWindow(app)
        window.show()
        app.exec_()
