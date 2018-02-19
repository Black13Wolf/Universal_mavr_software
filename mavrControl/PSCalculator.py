from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from mavr.processing import get_ps
from threading import Thread, active_count
from ast import literal_eval
from time import sleep
try:
    from .sub import PS_base_scanner as base_scan
except:
    from sub import PS_base_scanner as base_scan
    
class PSCalculator(QWidget):
    def __init__(self, parent = None):
        self.mainGui = parent
        QWidget.__init__(self, parent)
        self.layout = QGridLayout()

        self.b_Start = QPushButton('Start')
        self.b_Start.clicked.connect(self.c_Start)
        self.b_Input = QPushButton('Choose path')
        self.b_Input.clicked.connect(self.c_Input)
        self.b_Output = QPushButton('Choose path')
        self.b_Output.clicked.connect(self.c_Output)        
        
        self.l_Input = QLabel('Input path: ')
        self.v_Input = QLineEdit()
        self.l_Output = QLabel('Output path: ')
        self.v_Output = QLineEdit()
        
        self.l_Type = QLabel('Type: ')
        self.v_Type = QComboBox()
        self.v_Type.addItems(['Year', 'Set', 'Night', 'Star'])
        self.l_Type.setFixedWidth(150)
        self.v_Type.setFixedWidth(150)
        
        self.l_Diff = QLabel('Diff frames: ')
        self.v_Diff = QSpinBox()
        self.v_Diff.setValue(1)
        self.l_Diff.setFixedWidth(150)
        self.v_Diff.setFixedWidth(150)
        
        self.l_Acf = QLabel('ACF')
        self.v_Acf = QComboBox()
        self.v_Acf.addItems(['ON', 'OFF'])
        
        self.l_Save = QLabel('Save: ')
        self.v_Save = QComboBox()
        self.v_Save.addItems(['fits', 'OFF'])

        self.l_Shape = QLabel('Shape: ')
        self.v_Shape = QComboBox()
        self.v_Shape.addItems(['(1024,1024)', '(512,512)', '(2048,2048)', '(4096,4096)'])

        self.l_Rmbgr = QLabel('Removing BGR: ')
        self.v_Rmbgr = QComboBox()
        self.v_Rmbgr.addItems(['ON', 'OFF'])

        self.layout.addWidget(self.l_Input, 0, 0)
        self.layout.addWidget(self.v_Input, 0, 1, 1, 2)
        self.layout.addWidget(self.b_Input, 0, 3)
        self.layout.addWidget(self.l_Output, 1, 0)
        self.layout.addWidget(self.v_Output, 1, 1, 1, 2)
        self.layout.addWidget(self.b_Output, 1, 3)
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
        self.b_Start.setEnabled(False)
        params = {}
        params['input'] = {self.v_Type.currentText().lower() : self.v_Input.text()}
        params['output'] = {self.v_Type.currentText().lower() : self.v_Output.text()}
        params['type'] = self.v_Type.currentText().lower()
        params['diff'] = self.v_Diff.value() 
        if self.v_Acf.currentText() == 'ON':
            params['acf'] = True
        elif self.v_Acf.currentText() == 'OFF':
            params['acf'] = False
        if self.v_Save.currentText() == 'OFF':
            params['save'] = False
        else: params['save'] = self.v_Save.currentText()
        params['shape'] = literal_eval(self.v_Shape.currentText())
        if self.v_Rmbgr.currentText() == 'ON':
            params['rmbgr'] = True
        elif self.v_Rmbgr.currentText() == 'OFF':
            params['rmbgr'] = False
        if params['type'] == 'year':
            self.th = {
                '1' : Thread(target = base_scan.scan_year, args=(params, self)),
                '2' : Thread(target = self.check_of_end, args=(self.b_Start,))
            }
        elif params['type'] == 'set':
            self.th = {
                '1' : Thread(target = base_scan.scan_set, args=(params, self)),
                '2' : Thread(target = self.check_of_end, args=(self.b_Start,))
            }
        elif params['type'] == 'night':
            self.th = {
                '1' : Thread(target = base_scan.scan_night, args=(params, self)),
                '2' : Thread(target = self.check_of_end, args=(self.b_Start,))
            }
        elif params['type'] == 'star':
            self.th = {
                '1' : Thread(target = get_ps, args = (params['input']['star'],), kwargs={'diff':params['diff'], 'acf':params['acf'], 'save':params['save'], 'shape':params['shape'], 'output':params['output']['star'], 'rmbgr_on':params['rmbgr']}),
                '2' : Thread(target = self.check_of_end, args=(self.b_Start,))
            }
        else:
            return 1
        #self.th['1'].daemon = True
        self.th['1'].start()
        sleep(0.5)
        #self.th['2'].daemon = True        
        self.th['2'].start()
        self.mainGui.close()

    def c_Input(self):
        if self.v_Type.currentText().lower() == 'star':
            self.v_Input.setText(QFileDialog.getOpenFileName(self, 'Select Input Dat File', '.', "DAT (*.dat)")[0])
        else:
            self.v_Input.setText(QFileDialog.getExistingDirectory(self, "Select Input Directory", '.', QFileDialog.ShowDirsOnly))

    def c_Output(self):
        self.v_Output.setText(QFileDialog.getExistingDirectory(self, "Select Output Directory", '.', QFileDialog.ShowDirsOnly))
    
    def check_of_end(self, button):
        while True:
            sleep(1)
            if active_count() == 2:
                print('Завершено')
                break