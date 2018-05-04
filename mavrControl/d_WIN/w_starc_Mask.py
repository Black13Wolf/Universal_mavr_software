from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from threading import Thread, active_count
from ast import literal_eval
from time import sleep
from subprocess import call
from threading import Thread
    
class starc_MASK(QWidget):
    def __init__(self, parent = None):
        self.mainGui = parent
        QWidget.__init__(self, parent)
        self.layout = QGridLayout()
        
        self.l_Starc = QLabel('STARC path: ')
        self.v_Starc = QLineEdit()
        self.v_Starc.setFixedWidth(300)
        self.b_Starc = QPushButton('Choose path')

        self.l_Input = QLabel('Input path: ')
        self.v_Input = QLineEdit()
        self.b_Input = QPushButton('Choose path')

        self.l_Output = QLabel('Output path: ')
        self.v_Output = QLineEdit()
        self.b_Output = QPushButton('Choose path')

        self.l_Params = QLabel('Console parameters: ')
        self.v_Params = QLineEdit()

        
        self.layout.addWidget(self.l_Starc, 0, 0)
        self.layout.addWidget(self.v_Starc, 0, 1)
        self.layout.addWidget(self.b_Starc, 0, 2)
        self.layout.addWidget(self.l_Input, 1, 0)
        self.layout.addWidget(self.v_Input, 1, 1)
        self.layout.addWidget(self.b_Input, 1, 2)
        self.layout.addWidget(self.l_Output, 2, 0)
        self.layout.addWidget(self.v_Output, 2, 1)
        self.layout.addWidget(self.b_Output, 2, 2)
        self.layout.addWidget(self.l_Params, 3, 0)
        self.layout.addWidget(self.v_Params, 3, 1, 1, 2)

        self.setLayout(self.layout)