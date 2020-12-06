import sys

from PyQt5.QtWidgets import QApplication

from app import MainWindow


class ScreenCap:

    def __init__(self):
        app = QApplication(sys.argv)
        window = MainWindow(app)
        window.show()
        app.exec_()