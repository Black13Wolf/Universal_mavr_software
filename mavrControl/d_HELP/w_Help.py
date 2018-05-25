from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from functools import partial
from os.path import join, dirname
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Help(QWidget):
    def __init__(self, parent = None):
        self.mainGui = parent
        QWidget.__init__(self, parent)
        self.main_layout = QGridLayout()

        self.browser = Browser(parent = self)
        self.main_layout.addWidget(self.browser, 0, 0)
        self.setLayout(self.main_layout)

class Browser(QWebEngineView):
    def __init__(self, parent = None):
        self.mainWidget = parent
        QWebEngineView.__init__(self, parent)
        self.setFixedSize(800,600)
        self.setUrl(QUrl.fromLocalFile(join(dirname(__file__), 'source', 'index.html')))
