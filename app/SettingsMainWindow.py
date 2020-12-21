import os
import pickle
from tkinter import Tk
from iso639 import languages

from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QTabWidget, QWidget, QFormLayout, QLineEdit, QHBoxLayout, \
    QRadioButton, QLabel, QCheckBox, QGridLayout, QListWidget, QDesktopWidget, QVBoxLayout, QPushButton


class TabWidget(QTabWidget):

    right_layout: QGridLayout
    right_widget: QWidget
    main_layout: QGridLayout
    main_widget: QWidget

    def __init__(self):
        super().__init__()
        self.langs = pickle.load(open(os.path.join(
            os.path.dirname(__file__),
            "..",
            "langs.pkl"
        ), "rb"))

        self.create_languages_tab()

    def lang_list_item_selected(self, item):
        print(item.data())
        print(self.main_layout.removeWidget(self.right_widget))
        self.right_widget = QWidget()
        self.right_layout = QFormLayout()
        install = QHBoxLayout()
        install.addWidget(QPushButton("Install"))
        self.right_layout.addRow(install)
        self.right_widget.setLayout(self.right_layout)
        self.main_layout.addWidget(self.right_widget, 0, 1)

    def create_languages_tab(self):
        self.main_widget = QWidget()
        self.main_layout = QGridLayout()
        self.main_widget.setLayout(self.main_layout)
        lang_list = QListWidget()
        for i, lang in enumerate(self.langs):
            try:
                l = languages.get(bibliographic=lang)
                lang_list.addItem(l.inverted)
            except KeyError as e:
                pass

        for i in ["eng"]:
            items = lang_list.findItems(i, Qt.MatchExactly)
            for item in items:
                item.setForeground(Qt.green)

        lang_list.clicked.connect(self.lang_list_item_selected)
        self.main_layout.addWidget(lang_list, 0, 0)

        self.right_widget = QWidget()
        self.right_layout = QGridLayout()
        self.right_widget.setLayout(self.right_layout)
        self.main_layout.addWidget(self.right_widget, 0, 1)

        self.main_layout.setColumnStretch(0, 1)
        self.main_layout.setColumnStretch(1, 3)

        self.addTab(self.main_widget, "Languages")

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
