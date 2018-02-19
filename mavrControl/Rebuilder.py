from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from os.path import join
class Rebuilder(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.mainGui = parent        
        self.layout = QGridLayout()

        self.b_Input = QPushButton('Choose path')
        self.b_Input.clicked.connect(self.c_Input)
        self.b_Output = QPushButton('Choose path')
        self.b_Output.clicked.connect(self.c_Output)
        self.b_Rebuild = QPushButton('Пересобрать')
        self.b_Rebuild.clicked.connect(self.c_Rebuild)        
        
        self.l_Input = QLabel('Input path: ')
        self.v_Input = QLineEdit()
        self.v_Input.setFixedWidth(300)
        self.v_Input.textChanged.connect(self.s_Def_path)
        self.l_Output = QLabel('Output path: ')
        self.v_Output = QLineEdit()
        self.v_Output.setFixedWidth(300)

        self.layout.addWidget(self.l_Input, 0, 0)
        self.layout.addWidget(self.v_Input, 0, 1, 1, 2)
        self.layout.addWidget(self.b_Input, 0, 3)
        self.layout.addWidget(self.l_Output, 1, 0)
        self.layout.addWidget(self.v_Output, 1, 1, 1, 2)
        self.layout.addWidget(self.b_Output, 1, 3)
        self.layout.addWidget(self.b_Rebuild, 2, 1, 1, 2)
        self.setLayout(self.layout)

    def c_Input(self):
        self.v_Input.setText(QFileDialog.getExistingDirectory(self, "Select Input Directory", '.', QFileDialog.ShowDirsOnly))

    def c_Output(self):
        self.v_Output.setText(QFileDialog.getExistingDirectory(self, "Select Output Directory", '.', QFileDialog.ShowDirsOnly))

    def c_Rebuild(self):
        pass
    
    def s_Def_path(self):
        if self.v_Output.text() == '':
            self.v_Output.setText(join(self.v_Input.text(), 'rebuild'))