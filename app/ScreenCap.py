import sys

from PyQt5.QtWidgets import QApplication

from app import SnipWindow


class ScreenCap:

    def __init__(self):
        app = QApplication(sys.argv)
        window = SnipWindow(app)
        window.show()
        app.exec_()