from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from threading import Thread, active_count
from ast import literal_eval
from time import sleep
from subprocess import call
from threading import Thread
from os import walk
from os.path import join, isdir

__DEBUG__ = True   

class starc_PS(QWidget):
    sign_change_progress = pyqtSignal(int, int, str)
    def __init__(self, parent = None):
        self.mainGui = parent
        QWidget.__init__(self, parent)

        self.sign_change_progress.connect(self.slot_change_progress)
        self.layout = QGridLayout()
        
        self.l_Starc = QLabel('STARC path: ')
        self.v_Starc = QLineEdit()
        self.v_Starc.setFixedWidth(250)
        self.b_Starc = QPushButton('Choose path')
        self.b_Starc.clicked.connect(self.c_Starc)

        self.l_Input = QLabel('Input path: ')
        self.v_Input = QLineEdit()
        self.b_Input = QPushButton('Choose path')
        self.b_Input.clicked.connect(self.c_Input)
        
        self.l_Output = QLabel('Output path: ')
        self.v_Output = QLineEdit()
        self.b_Output = QPushButton('Choose path')
        self.b_Output.clicked.connect(self.c_Output)
        
        self.l_Type = QLabel('Type: ')
        self.v_Type = QComboBox()
        self.v_Type.addItems(['Set', 'Year', 'Night', 'Star'])

        self.l_Diff = QLabel('Frame diff (/k): ')
        self.v_Diff = QComboBox()
        self.v_Diff.addItems(['-1', '0', '1', '2', '3', '5', '10', '25', '50', '100'])

        self.l_Size = QLabel('Resizing (/S): ')
        self.v_Size = QComboBox()
        self.v_Size.addItems(['2', '1', '4', '8'])

        self.l_Batch = QLabel('BG mode (/p): ')
        self.v_Batch = QComboBox()
        self.v_Batch.addItems(['ON', 'OFF'])

        self.l_Silent = QLabel('Silent mode (/s): ')
        self.v_Silent = QComboBox()
        self.v_Silent.addItems(['ON', 'OFF'])

        self.b_Start = QPushButton('Start')
        self.b_Start.clicked.connect(self.c_Start)

        self.PB = QProgressBar()
        self.PB.setValue(0)
        self.PB.hide()

        self.msg = QLabel('Collecting... ')
        self.msg.setAlignment(Qt.AlignCenter)
        self.msg.hide()
        
        self.layout.addWidget(self.l_Type, 0, 0)
        self.layout.addWidget(self.v_Type, 0, 1)
        self.layout.addWidget(self.b_Start, 0, 2, 1, 2)        
        self.layout.addWidget(self.l_Starc, 1, 0)
        self.layout.addWidget(self.v_Starc, 1, 1, 1, 2)
        self.layout.addWidget(self.b_Starc, 1, 3)
        self.layout.addWidget(self.l_Input, 2, 0)
        self.layout.addWidget(self.v_Input, 2, 1, 1, 2)
        self.layout.addWidget(self.b_Input, 2, 3)
        self.layout.addWidget(self.l_Output, 3, 0)
        self.layout.addWidget(self.v_Output, 3, 1, 1, 2)
        self.layout.addWidget(self.b_Output, 3, 3)
        self.layout.addWidget(self.l_Diff, 4, 0)
        self.layout.addWidget(self.v_Diff, 4, 1)
        self.layout.addWidget(self.l_Size, 4, 2)
        self.layout.addWidget(self.v_Size, 4, 3)
        self.layout.addWidget(self.l_Batch, 5, 0)
        self.layout.addWidget(self.v_Batch, 5, 1)
        self.layout.addWidget(self.l_Silent, 5, 2)
        self.layout.addWidget(self.v_Silent, 5, 3)
        self.layout.addWidget(self.PB, 6, 0, 1, 4)
        self.layout.addWidget(self.msg, 6, 0, 1, 4)

        self.setLayout(self.layout)

        if __DEBUG__:
            self.v_Starc.setText(r'd:\Prog\STARC')
            self.v_Input.setText(r'd:\!WORK\OBSERVATIONS\test_year')
            self.v_Output.setText(r'd:\!WORK\OBSERVATIONS\temp')

    def c_Input(self):
        if self.v_Type.currentText().lower() == 'star':
            self.v_Input.setText(QFileDialog.getOpenFileName(self, 'Select Input Dat File', '.', "DAT (*.dat)")[0])
        else:
            self.v_Input.setText(QFileDialog.getExistingDirectory(self, "Select Input Directory", '.', QFileDialog.ShowDirsOnly))

    def c_Output(self):
        self.v_Output.setText(QFileDialog.getExistingDirectory(self, "Select Output Directory", '.', QFileDialog.ShowDirsOnly))

    def c_Starc(self):
        self.v_Starc.setText(QFileDialog.getExistingDirectory(self, "Select Output Directory", '.', QFileDialog.ShowDirsOnly))
        
    def c_Start(self):
        self.PB.show()
        self.msg.show()
        self.params = {}
        self.params['basepath'] = self.v_Input.text()
        self.params['work'] = []
        self.th = Thread(target = self.process)
        self.th.start()
        self.b_Start.setEnabled(False)
    
    def slot_change_progress(self, v, max_v, text):
        if not self.PB.maximum == max_v:
            self.PB.setMaximum(max_v)
            self.PB.setValue(0)
        self.PB.setValue(v)
        self.msg.setText(text)
        
    def process(self):
        if self.v_Type.currentText().lower() == 'year':
            self.scan_year()
        elif self.v_Type.currentText().lower() == 'set':
            self.scan_set()
        elif self.v_Type.currentText().lower() == 'night':
            self.scan_night()
        elif self.v_Type.currentText().lower() == 'star':
            pass
        print(self.params)

    def scan_year(self):
        self.params['sets'] = {}
        self.params['sets']['paths'] = list(walk(self.params['basepath']))[0][1]
        self.scan_set()

    def scan_set(self):
        if 'sets' in self.params:
            for p_set in self.params['sets']['paths']:
                self.params['sets'][p_set] = {}
                if isdir(join(self.params['basepath'], p_set, 'cut')): subdir = 'cut'
                elif isdir(join(self.params['basepath'], p_set, 'rebuild')): subdir = 'rebuild'
                elif isdir(join(self.params['basepath'], p_set, 'rebuilded')): subdir = 'rebuilded'
                for root, dirs, files in walk(join(self.params['basepath'], p_set, subdir)):
                    self.params['sets'][p_set]['nights'] = [join(subdir, d) for d in dirs]                    
                    break
        else:
            self.params['nights'] = list(walk(join(self.params['basepath'])))[0][1]
        self.scan_night()

    def scan_night(self):
        if 'sets' in self.params:
            for p_set in self.params['sets']['paths']:
                for night in self.params['sets'][p_set]['nights']:
                    for root, dirs, files in walk(join(self.params['basepath'], p_set, night)):
                        for f in files:
                            if f.endswith('.dat') and not f.startswith('dark') and not f.startswith('flat') and not f.endswith('moon.dat'):
                                self.params['work'].append(join(self.params['basepath'], p_set, night, f))
        elif 'nights' in self.params:
            pass
        else:
            pass

    
    def calc_PS(self, level = 0):
        pass