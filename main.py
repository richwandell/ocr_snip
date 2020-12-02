import numpy as np
from PIL import ImageGrab
import cv2
from PyQt5.QtCore import Qt, QEvent, QObject, QPointF
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen, QKeyEvent, QMouseEvent
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel

from tkinter import *

from PyQt5.uic.properties import QtWidgets, QtGui

try:
    # if on windows we need this app to be dpi aware so screenshots understand scaling
    from ctypes import windll
    user32 = windll.user32
    user32.SetProcessDPIAware()
except:
    pass


class MainWindow(QMainWindow):

    mouse_start = (0, 0)

    def __init__(self, app: QApplication):
        super().__init__()
        self.app = app
        root = Tk()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setCursor(Qt.BlankCursor)
        self.label = QLabel()
        canvas = QPixmap(width, height)
        canvas.fill(Qt.transparent)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.move(0, 0)
        self.showFullScreen()
        self.setMouseTracking(True)

    def setMouseTracking(self, flag):
        def recursive_set(parent):
            for child in parent.findChildren(QObject):
                try:
                    child.setMouseTracking(flag)
                except:
                    pass
                recursive_set(child)
        QWidget.setMouseTracking(self, flag)
        recursive_set(self)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.nativeVirtualKey() == 27:
            self.destroy()
            self.app.quit()

    def mouseMoveEvent(self, e):
        self.label.pixmap().fill(Qt.transparent)
        painter = QPainter(self.label.pixmap())
        x, y = e.x(), e.y()

        painter.setPen(QPen(Qt.green,  5, Qt.DashLine))
        if self.mouse_start != (0, 0):
            width = x - self.mouse_start[0]
            height = y - self.mouse_start[1]
            painter.drawRect(*self.mouse_start, width, height)

        painter.drawEllipse(QPointF(x, y), 20, 20)
        painter.end()
        self.update()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.mouse_start = e.x(), e.y()

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        self.destroy()
        self.app.quit()
        d = ImageGrab.grab(bbox=(*self.mouse_start, e.x(), e.y()))
        screen = np.array(d)
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

        while True:
            cv2.imshow('Python Window', screen)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setOpacity(0.1)
        painter.setBrush(Qt.white)
        painter.setPen(QPen(Qt.white))
        painter.drawRect(self.rect())


class ScreenCap:

    def __init__(self):
        app = QApplication(sys.argv)
        window = MainWindow(app)
        window.show()
        app.exec_()


if __name__ == "__main__":
    sc = ScreenCap()


