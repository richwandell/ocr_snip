from app import ScreenCap


class WinSysTray:

    def __init__(self):
        from infi.systray import SysTrayIcon

        def say_hello(systray):
            ScreenCap()

        menu_options = (("Say Hello", None, say_hello),)
        systray = SysTrayIcon("lasso.ico", "OCR Snip", menu_options)
        systray.start()

