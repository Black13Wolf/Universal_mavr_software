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

        self.l_Type = QLabel('Type: ')
        self.v_Type = QComboBox()
        self.v_Type.addItems(['Year', 'Set', 'Night', 'Star'])
        self.l_Type.setFixedWidth(150)
        self.v_Type.setFixedWidth(150)
        
        self.l_Diff = QLabel('Diff frames: ')
        self.v_Diff = QSpinBox()
        self.l_Diff.setFixedWidth(150)
        self.v_Diff.setFixedWidth(150)
        
        self.l_Acf = QLabel('ACF')
        self.v_Acf = QComboBox()
        self.v_Acf.addItems(['ON', 'OFF'])
        
        self.l_Save = QLabel('Save: ')
        self.v_Save = QComboBox()
        self.v_Save.addItems(['ON', 'OFF'])

        self.l_Shape = QLabel('Shape: ')
        self.v_Shape = QComboBox()
        self.v_Shape.addItems(['512x512', '1024x1024', '2048x2048', '4096x4096'])

        self.l_Rmbgr = QLabel('Removing BGR: ')
        self.v_Rmbgr = QComboBox()
        self.v_Rmbgr.addItems(['ON', 'OFF'])

        self.l_Output = QLabel('Output path: ')
        self.v_Output = QLineEdit()
    #def get_ps(path_to_dat, diff=0, acf=False, save=False, shape=(512,512), output=False, rmbgr_on=True)
        
        self.layout.addWidget(self.l_Input, 0, 0)
        self.layout.addWidget(self.v_Input, 0, 1)
        self.layout.addWidget(self.b_Input, 0, 2, 1, 2)
        self.layout.addWidget(self.l_Output, 1, 0)
        self.layout.addWidget(self.v_Output, 1, 1)
        self.layout.addWidget(self.b_Output, 1, 2, 1, 2)
        self.layout.addWidget(self.l_Type, 2, 0)
        self.layout.addWidget(self.v_Type, 2, 1)
        self.layout.addWidget(self.l_Diff, 2, 2)
        self.layout.addWidget(self.v_Diff, 2, 3)
        self.layout.addWidget(self.l_Acf, 3, 0)
        self.layout.addWidget(self.v_Acf, 3, 1)
        self.layout.addWidget(self.l_Save, 3, 2)
        self.layout.addWidget(self.v_Save, 3, 3)
        self.layout.addWidget(self.l_Shape, 4, 0)
        self.layout.addWidget(self.v_Shape, 4, 1)
        self.layout.addWidget(self.l_Rmbgr, 4, 2)
        self.layout.addWidget(self.v_Rmbgr, 4, 3)
        self.layout.addWidget(self.b_Start, 10, 1, 1, 2)
        self.setLayout(self.layout)
    

    def c_Start(self):
        self.th = Thread(target = get_ps, args=())

    def c_Input(self):
        pass

    def c_Output(self):
        pass