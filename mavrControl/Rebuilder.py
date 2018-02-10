from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

class Rebuilder(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.layout = QGridLayout()
        self.label = QLabel('Rebuilder')
        
        self.layout.addWidget(self.label, 0, 0)
        self.setLayout(self.layout)