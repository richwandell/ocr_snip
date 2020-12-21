import os
import pickle
import urllib.request
from tkinter import Tk
from typing import List, Union

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QTabWidget, QWidget, QFormLayout, QHBoxLayout, \
    QGridLayout, QListWidget, QDesktopWidget, QVBoxLayout, QPushButton, QLabel
from iso639 import languages


class CustomListWidget(QWidget):

    def __init__(self, parent=None):
        super(CustomListWidget, self).__init__(parent)
        self.textQVBoxLayout = QVBoxLayout()
        self.textUpQLabel = QLabel()
        self.textDownQLabel = QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout = QHBoxLayout()
        self.iconQLabel = QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')
        self.textDownQLabel.setStyleSheet('''
            color: rgb(255, 0, 0);
        ''')

    def setTextUp (self, text):
        self.textUpQLabel.setText(text)

    def setTextDown (self, text):
        self.textDownQLabel.setText(text)

    def setIcon (self, imagePath):
        self.iconQLabel.setPixmap(QPixmap(imagePath))


class TabWidget(QTabWidget):

    lang_list: QListWidget
    selected_language: str
    right_layout: QGridLayout
    right_widget: QWidget
    main_layout: QGridLayout
    main_widget: QWidget
    languages: List[str]

    def __init__(self):
        super().__init__()
        self.langs = pickle.load(open(os.path.join(
            os.path.dirname(__file__),
            "..",
            "langs.pkl"
        ), "rb"))
        self.languages = list(self.get_languages())
        self.create_languages_tab()

    def install(self, item):
        try:
            lang = languages.get(name=self.selected_language)
            url = 'https://raw.githubusercontent.com/tesseract-ocr/tessdata/master/%s.traineddata' % lang.part3
            output = os.path.join(
                os.path.dirname(__file__),
                "..",
                "tesseract",
                "tessdata",
                "%s.traineddata" % lang.part3
            )
            urllib.request.urlretrieve(url, output)
            if os.path.exists(output):
                self.main_layout.removeWidget(self.right_widget)
                self.right_widget = QWidget()
                self.right_layout = QFormLayout()
                remove = QHBoxLayout()
                remove_button = QPushButton("Remove")
                remove_button.clicked.connect(self.remove)
                remove.addWidget(remove_button)
                self.right_layout.addRow(remove)
                self.right_widget.setLayout(self.right_layout)
                self.main_layout.addWidget(self.right_widget, 0, 1)
                self.languages.append(self.selected_language)
                self.color_lang_list()
        except KeyError as e:
            pass
        print(self.selected_language)

    def remove(self, item):
        print(self.selected_language)

    def lang_list_item_selected(self, item):
        self.selected_language = item.data()
        self.main_layout.removeWidget(self.right_widget)
        self.right_widget = QWidget()
        self.right_layout = QFormLayout()

        if self.selected_language in self.languages:
            remove = QHBoxLayout()
            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(self.remove)
            remove.addWidget(remove_button)
            self.right_layout.addRow(remove)
        else:
            install = QHBoxLayout()
            install_button = QPushButton("Install")
            install_button.clicked.connect(self.install)
            install.addWidget(install_button)
            self.right_layout.addRow(install)

        self.right_widget.setLayout(self.right_layout)
        self.main_layout.addWidget(self.right_widget, 0, 1)

    def get_languages(self):
        for file in os.listdir(os.path.join(
            os.path.dirname(__file__),
            "..",
            "tesseract",
            "tessdata"
        )):
            if file.endswith(".traineddata"):
                file = file.replace(".traineddata", "")
                try:
                    l = languages.get(bibliographic=file)
                    yield l.inverted
                except KeyError as e:
                    pass

    def color_lang_list(self):
        for i in self.languages:
            items = self.lang_list.findItems(i, Qt.MatchExactly)
            for item in items:
                item.setForeground(Qt.green)

    def create_languages_tab(self):
        self.main_widget = QWidget()
        self.main_layout = QGridLayout()
        self.main_widget.setLayout(self.main_layout)
        self.lang_list = QListWidget()
        for i, lang in enumerate(self.langs):
            try:
                l = languages.get(bibliographic=lang)
                self.lang_list.addItem(l.inverted)
            except KeyError as e:
                pass

        self.color_lang_list()

        self.lang_list.clicked.connect(self.lang_list_item_selected)
        self.main_layout.addWidget(self.lang_list, 0, 0)

        self.right_widget = QWidget()
        self.right_layout = QGridLayout()
        self.right_widget.setLayout(self.right_layout)
        self.main_layout.addWidget(self.right_widget, 0, 1)

        self.main_layout.setColumnStretch(0, 1)
        self.main_layout.setColumnStretch(1, 3)

        self.addTab(self.main_widget, "Languages")


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
        self.setWindowIcon(QIcon(os.path.join("images", "lasso.ico")))
