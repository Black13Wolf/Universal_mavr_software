from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from os.path import join
from time import sleep
from threading import Thread, active_count

try:
    from . import p_Rebuild as rebuilder
except:
    import p_Rebuild as rebuilder

class Rebuilder(QWidget):
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
        
        self.layout.addWidget(self.l_Input, 0, 0)
        self.layout.addWidget(self.v_Input, 0, 1, 1, 2)
        self.layout.addWidget(self.b_Input, 0, 3)
        self.layout.addWidget(self.l_Output, 1, 0)
        self.layout.addWidget(self.v_Output, 1, 1, 1, 2)
        self.layout.addWidget(self.b_Output, 1, 3)
        self.layout.addWidget(self.l_Type, 2, 0)
        self.layout.addWidget(self.v_Type, 2, 1)
        self.layout.addWidget(self.b_Start, 2, 2, 1, 2)
        self.setLayout(self.layout)

    def c_Input(self):
        self.v_Input.setText(QFileDialog.getExistingDirectory(self, "Select Input Directory", '.', QFileDialog.ShowDirsOnly))

    def c_Output(self):
        self.v_Output.setText(QFileDialog.getExistingDirectory(self, "Select Output Directory", '.', QFileDialog.ShowDirsOnly))

    def c_Start(self):
        self.b_Start.setEnabled(False)
        params = {}
        params['type'] = self.v_Type.currentText().lower()
        params['input'] = {self.v_Type.currentText().lower() : self.v_Input.text()}
        params['output'] = {self.v_Type.currentText().lower() : self.v_Output.text()}

        if params['type'] == 'set':
            self.th = {
                '1' : Thread(target = rebuilder.rebuild_set, args=(params, self)),
                '2' : Thread(target = self.check_of_end)
            }
            
        elif params['type'] == 'night':
            self.th = {
                '1' : Thread(target = rebuilder.rebuild_night, args=(params, self)),
                '2' : Thread(target = self.check_of_end)
            }
            
        elif params['type'] == 'star':
            self.th = {
                '1' : Thread(target = rebuilder.rebuild_star, args=(params, self)),
                '2' : Thread(target = self.check_of_end)
            }
        self.th['1'].start()
        sleep(0.5)
        self.th['2'].start()
        self.mainGui.close()
                
    def s_Def_path(self):
        if self.v_Output.text() == '':
            self.v_Output.setText(join(self.v_Input.text(), 'rebuild'))
    
    def check_of_end(self):
        while True:
            sleep(0.5)
            if active_count() == 2:
                print('Завершено')
                break