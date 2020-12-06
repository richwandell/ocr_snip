import os
import sys

import pytesseract
from PyQt5.QtWidgets import QApplication

try:
    # if on windows we need this app to be dpi aware so screenshots understand scaling
    from ctypes import windll
    user32 = windll.user32
    user32.SetProcessDPIAware()
except:
    pass

f = os.path.dirname(os.path.realpath(__file__)) + "\\tesseract\\tesseract.exe"
if os.path.exists(f):
    pytesseract.pytesseract.tesseract_cmd = f

from MainWindow import MainWindow


class ScreenCap:

    def __init__(self):
        app = QApplication(sys.argv)
        window = MainWindow(app)
        window.show()
        app.exec_()


if __name__ == "__main__":
    sc = ScreenCap()

