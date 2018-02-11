from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from mavr.processing import get_ps

class PSCalculator(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.layout = QGridLayout()
        self.label = QLabel('PSCalculator')
        
        self.layout.addWidget(self.label, 0, 0)
        self.setLayout(self.layout)