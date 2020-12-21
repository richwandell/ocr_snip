import ctypes
import multiprocessing
import os
import threading
from ctypes import wintypes
from functools import reduce
from infi.systray import SysTrayIcon

import win32con

from app import ScreenCap
from app.SettingsDialog import SettingsDialog


class Hotkey(multiprocessing.Process):

    def run(self) -> None:

        vk, modifiers = (79, (win32con.MOD_WIN, win32con.MOD_SHIFT))
        if ctypes.windll.user32.RegisterHotKey(None, 0, reduce(lambda x, y: x | y, modifiers), vk):
            try:
                msg = wintypes.MSG()
                while ctypes.windll.user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                    if msg.message == win32con.WM_HOTKEY:
                        ScreenCap()
                    ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
                    ctypes.windll.user32.DispatchMessageA(ctypes.byref(msg))
            finally:
                ctypes.windll.user32.UnregisterHotKey(None, 0)


class WinSysTray:

    def __init__(self):
        hkt = Hotkey()
        hkt.start()

        def settings(systray):
            nonlocal hkt
            SettingsDialog()
            hkt.terminate()
            hkt = Hotkey()
            hkt.start()

        menu_options = (("Settings", None, settings),)
        systray = SysTrayIcon(os.path.join("images", "lasso.ico"), "OCR Snip", menu_options)
        systray.start()


