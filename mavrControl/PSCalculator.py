from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from mavr.processing import get_ps
from threading import Thread

class PSCalculator(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.layout = QGridLayout()
        
        self.b_Start = QPushButton('Start')
        self.b_Start.clicked.connect(self.c_Start)
        self.b_Input = QPushButton('Choose path')
        self.b_Input.clicked.connect(self.c_Input)
        self.b_Output = QPushButton('Choose path')
        self.b_Output.clicked.connect(self.c_Output)        
        
        self.l_Input = QLabel('Input path')
        self.v_Input = QLineEdit()

        self.l_Type = QLabel('Type')
        self.v_Type = QComboBox()
        self.v_Type.addItems(['Year', 'Set', 'Night', 'Star'])
        
        self.l_Output = QLabel('Output path: ')
        self.v_Outout = QLineEdit()
        
        self.layout.addWidget(self.l_Input, 0, 0)
        self.layout.addWidget(self.v_Input, 0, 1)
        self.layout.addWidget(self.b_Input, 0, 2)
        self.layout.addWidget(self.l_Type, 1, 0)
        self.layout.addWidget(self.v_Type, 1, 1)
        self.layout.addWidget(self.l_Output, 2, 0)
        self.layout.addWidget(self.v_Outout, 2, 1)
        self.layout.addWidget(self.b_Output, 2, 2)
        self.layout.addWidget(self.b_Start, 3, 0, 1, 3)
        self.setLayout(self.layout)
    
    def c_Start(self):
        self.th = Thread(target = get_ps, args=())

    def c_Input(self):
        pass

    def c_Output(self):
        pass