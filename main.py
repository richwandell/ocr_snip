import os

import pytesseract

from app import *

is_windows = False
try:
    # if on windows we need this app to be dpi aware so screenshots understand scaling
    from ctypes import windll
    user32 = windll.user32
    user32.SetProcessDPIAware()
    is_windows = True
except:
    pass

# install with build script windows
f = os.path.dirname(os.path.realpath(__file__)) + "\\tesseract\\tesseract.exe"
if os.path.exists(f):
    pytesseract.pytesseract.tesseract_cmd = f

if __name__ == "__main__":
    if is_windows:
        WinSysTray()


