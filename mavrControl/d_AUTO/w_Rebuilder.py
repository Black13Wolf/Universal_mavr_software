from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from os.path import join, abspath, dirname, pardir
from time import sleep
from threading import Thread, active_count

from . import p_Rebuild as rebuilder
from ..d_LOG.logging import test_msg

class Rebuilder(QWidget):
    sign_set_progress = pyqtSignal(int, int)
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.mainGui = parent        
        self.layout = QGridLayout()

        self.b_Input = QPushButton('Choose path')
        self.b_Input.clicked.connect(self.c_Input)
        self.b_Output = QPushButton('Choose path')
        self.b_Output.clicked.connect(self.c_Output)
        self.b_Start = QPushButton('Пересобрать')
        self.b_Start.clicked.connect(self.c_Start)        
        
        self.l_Input = QLabel('Input path: ')
        self.v_Input = QLineEdit()
        self.v_Input.setFixedWidth(300)
        self.v_Input.textChanged.connect(self.s_Def_path)
        self.l_Output = QLabel('Output path: ')
        self.v_Output = QLineEdit()
        self.v_Output.setFixedWidth(300)

        self.l_Type = QLabel('Type: ')
        self.v_Type = QComboBox()
        self.v_Type.addItems(['Set', 'Night', 'Star'])
        
        self.progressbar = QProgressBar()
        self.sign_set_progress.connect(self.slot_set_progress)
        self.progressbar.hide()

        self.layout.addWidget(self.l_Input, 0, 0)
        self.layout.addWidget(self.v_Input, 0, 1, 1, 2)
        self.layout.addWidget(self.b_Input, 0, 3)
        self.layout.addWidget(self.l_Output, 1, 0)
        self.layout.addWidget(self.v_Output, 1, 1, 1, 2)
        self.layout.addWidget(self.b_Output, 1, 3)
        self.layout.addWidget(self.l_Type, 2, 0)
        self.layout.addWidget(self.v_Type, 2, 1)
        self.layout.addWidget(self.b_Start, 2, 2, 1, 2)
        self.layout.addWidget(self.progressbar, 3, 0, 1, 4)
        self.setLayout(self.layout)

    def c_Input(self):
        self.v_Input.setText(QFileDialog.getExistingDirectory(self, "Select Input Directory", '.', QFileDialog.ShowDirsOnly))

    def c_Output(self):
        self.v_Output.setText(QFileDialog.getExistingDirectory(self, "Select Output Directory", '.', QFileDialog.ShowDirsOnly))

    def c_Start(self):
        self.b_Start.setEnabled(False)
        self.b_Input.setEnabled(False)
        self.b_Output.setEnabled(False)
        self.progressbar.show()

        params = {}
        params['type'] = self.v_Type.currentText().lower()
        params['input'] = {self.v_Type.currentText().lower() : self.v_Input.text()}
        params['output'] = {self.v_Type.currentText().lower() : self.v_Output.text()}
        self.th = Thread(target = rebuilder.rebuild_start, args=(params, self))
        self.th.start()
                
    def s_Def_path(self):
        if self.v_Output.text() == '' and self.v_Type.currentText().lower() == 'star':
            self.v_Output.setText(join(self.v_Input.text()))
        elif self.v_Output.text() == '' and (self.v_Type.currentText().lower() == 'night' or self.v_Type.currentText().lower() == 'set'):
            self.v_Output.setText(join(self.v_Input.text(), 'rebuild'))
        
    def slot_set_progress(self, v, maxv):
        self.progressbar.setRange(0, maxv)
        self.progressbar.setValue(v)
        if v == maxv:
            self.b_Start.setEnabled(True)
            self.b_Input.setEnabled(True)
            self.b_Output.setEnabled(True)