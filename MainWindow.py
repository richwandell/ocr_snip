from tkinter import Tk

import cv2
import numpy as np
import pyperclip
import pytesseract
from PIL import ImageGrab
from PyQt5.QtCore import Qt, QObject, QPointF, QPoint
from PyQt5.QtGui import QPixmap, QKeyEvent, QPainter, QPen, QMouseEvent, QRegion, QPolygon
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QWidget


class MainWindow(QMainWindow):

    mouse_start = (0, 0)
    mouse_pos = (0, 0)
    screen_dim = (0, 0)
    box_dim = (0, 0)

    def __init__(self, app: QApplication):
        super().__init__()
        self.app = app
        self.tk = Tk()
        self.screen_dim = (self.tk.winfo_screenwidth(), self.tk.winfo_screenheight())

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setCursor(Qt.BlankCursor)
        self.label = QLabel()
        canvas = QPixmap(*self.screen_dim)
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
        self.mouse_pos = (e.x(), e.y())

        if self.mouse_start != (0, 0):
            self.box_dim = (self.mouse_pos[0] - self.mouse_start[0], self.mouse_pos[1] - self.mouse_start[1])

        painter.setPen(QPen(Qt.green, 5, Qt.DashLine))
        painter.drawEllipse(QPointF(*self.mouse_pos), 20, 20)
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
        s = pytesseract.image_to_string(screen)
        pyperclip.copy(s)

    def get_mouse_coords(self):
        if self.box_dim[1] > 0:
            box_top = self.mouse_start[1]
            box_bottom = self.mouse_start[1] + self.box_dim[1]
        else:
            box_top = self.mouse_start[1] + self.box_dim[1]
            box_bottom = self.mouse_start[1]
        if self.box_dim[0] > 0:
            box_left = self.mouse_start[0]
            box_right = self.mouse_start[0] + self.box_dim[0]
        else:
            box_left = self.mouse_start[0] + self.box_dim[0]
            box_right = self.mouse_start[0]
        return box_left, box_right, box_top, box_bottom

    def paintEvent(self, event=None):
        painter = QPainter(self)
        if self.box_dim != (0, 0):
            l, r, t, b = self.get_mouse_coords()
            painter.setClipRegion(QRegion(QPolygon([
                QPoint(0, 0),
                QPoint(self.screen_dim[0], 0),
                QPoint(self.screen_dim[0], t),
                QPoint(l, t),
                QPoint(l, b),
                QPoint(r, b),
                QPoint(r, t),
                QPoint(self.screen_dim[0], t),
                QPoint(self.screen_dim[0], self.screen_dim[1]),
                QPoint(0, self.screen_dim[1]),
                QPoint(0, 0)
            ]), Qt.OddEvenFill))
        painter.setOpacity(0.4)
        painter.setBrush(Qt.black)
        painter.setPen(QPen(Qt.black))
        painter.drawRect(self.rect())
