import os
import pickle
from tkinter import Tk

from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QTabWidget, QWidget, QFormLayout, QLineEdit, QHBoxLayout, \
    QRadioButton, QLabel, QCheckBox, QGridLayout, QListWidget, QDesktopWidget, QVBoxLayout, QPushButton


class TabWidget(QTabWidget):

    def __init__(self):
        super().__init__()
        self.langs = pickle.load(open(os.path.join(
            os.path.dirname(__file__),
            "..",
            "langs.p"
        ), "rb"))

        self.create_languages_tab()

        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.addTab(self.tab2, "Tab 2")
        self.addTab(self.tab3, "Tab 3")
        self.tab2UI()
        self.tab3UI()

    def lang_list_item_selected(self, item):
        print(item.data())

    def create_languages_tab(self):
        main_widget = QWidget()
        main_layout = QGridLayout()
        main_widget.setLayout(main_layout)
        lang_list = QListWidget()
        for i, lang in enumerate(self.langs):
            lang_list.addItem(lang)

        for i in ["eng"]:
            items = lang_list.findItems(i, Qt.MatchExactly)
            for item in items:
                item.setForeground(Qt.green)

        lang_list.clicked.connect(self.lang_list_item_selected)
        main_layout.addWidget(lang_list, 0, 0)

        right_widget = QWidget()
        right_layout = QGridLayout()
        right_widget.setLayout(right_layout)
        main_layout.addWidget(right_widget, 0, 1)

        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(1, 3)

        self.addTab(main_widget, "Languages")

    def tab2UI(self):
        layout = QFormLayout()
        sex = QHBoxLayout()
        sex.addWidget(QRadioButton("Male"))
        sex.addWidget(QRadioButton("Female"))
        layout.addRow(QLabel("Sex"), sex)
        layout.addRow("Date of Birth", QLineEdit())
        self.setTabText(1, "Personal Details")
        self.tab2.setLayout(layout)

    def tab3UI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("subjects"))
        layout.addWidget(QCheckBox("Physics"))
        layout.addWidget(QCheckBox("Maths"))
        self.setTabText(2, "Education Details")
        self.tab3.setLayout(layout)


class SettingsMainWindow(QMainWindow):

    def __init__(self, app: QApplication):
        super().__init__()
        self.app = app
        self.tk = Tk()
        self.screen_dim = (self.tk.winfo_screenwidth(), self.tk.winfo_screenheight())

        self.setWindowTitle("OCR Snip Settings")
        main_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(TabWidget())

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self.setGeometry(0, 0, self.screen_dim[0] / 2, self.screen_dim[1] / 2)
        center = QDesktopWidget().availableGeometry().center()
        rectangle = self.frameGeometry()
        rectangle.moveCenter(center)
        self.move(rectangle.topLeft())
        self.setWindowIcon(QIcon('lasso.ico'))
