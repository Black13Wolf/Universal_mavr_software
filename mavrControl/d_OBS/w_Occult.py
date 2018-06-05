from datetime import datetime as dt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from astropy.io import fits
from numpy import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.pyplot import xlim
from time import sleep


class Occultation(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.main_layout = QGridLayout()

        #-----------------------------
        self.b_Input = QPushButton('Choose path')
        self.b_Input.clicked.connect(self.c_Input)
        self.b_Output = QPushButton('Choose path')
        self.b_Output.clicked.connect(self.c_Output)

        self.l_Input = QLabel('Input path: ')
        self.v_Input = QLineEdit()
        self.l_Output = QLabel('Output path: ')
        self.v_Output = QLineEdit()

        self.l_Binning = QLabel('Binning:')
        self.v_Binning = QComboBox()
        self.v_Binning.addItems(['16x16', '8x8', '4x4', '2x2'])

        self.b_Show = QPushButton('Show')
        self.b_Show.clicked.connect(self.c_Show)
        self.b_Save = QPushButton('Save')
        self.b_Save.clicked.connect(self.c_Save)
        self.b_Save.setEnabled(False)

        w = 150
        self.l_LVal = QLabel('Left VALUE:')
        self.l_LVal.setFixedWidth(w)
        self.v_LVal = QLineEdit()
        self.v_LVal.setFixedWidth(w)        
        self.l_RVal = QLabel('Right VALUE:')
        self.l_RVal.setFixedWidth(w)
        self.v_RVal = QLineEdit()
        self.v_RVal.setFixedWidth(w)
        #-----------------------------
        
        self.img = Imager(parent = self)
        
        self.main_layout.addWidget(self.l_Input, 0, 0)
        self.main_layout.addWidget(self.v_Input, 0, 1, 1, 2)
        self.main_layout.addWidget(self.b_Input, 0, 3)
        self.main_layout.addWidget(self.l_Output, 1, 0)
        self.main_layout.addWidget(self.v_Output, 1, 1, 1, 2)
        self.main_layout.addWidget(self.b_Output, 1, 3)
        self.main_layout.addWidget(self.l_Binning, 2, 0)
        self.main_layout.addWidget(self.v_Binning, 2, 1)
        self.main_layout.addWidget(self.b_Show, 2, 2)
        self.main_layout.addWidget(self.b_Save, 2, 3)
        self.main_layout.addWidget(self.img, 3, 0, 1, 4)
        self.main_layout.addWidget(self.l_LVal, 4, 0)
        self.main_layout.addWidget(self.v_LVal, 4, 1)
        self.main_layout.addWidget(self.l_RVal, 4, 2)
        self.main_layout.addWidget(self.v_RVal, 4, 3)

        self.setLayout(self.main_layout)
    
    def c_Input(self):
        self.v_Input.setText(QFileDialog.getOpenFileName(self, 'Select Input Dat File', '.', "DAT (*.dat)")[0])

    def c_Output(self):
        self.v_Input.setText(QFileDialog.getExistingDirectory(self, "Select Input Directory", '.', QFileDialog.ShowDirsOnly))

    def c_Show(self):
        if self.v_Input.text():
            self.v_Input.setEnabled(False)
            self.serie = memmap(self.v_Input.text(), dtype='uint16')
            b = int(512/int(self.v_Binning.currentText().split('x')[0]))
            frames = int(self.serie.size/b**2)
            self.serie = self.serie.reshape(frames, b, b)
            intense = sum(self.serie, axis=(1,2))
            self.img.fig.clf()
            self.img.ax = self.img.fig.add_subplot(111)
            self.img.ax.plot(intense, '.')
            self.img.canvas.draw()
            self.b_Save.setEnabled(True)

    def c_Save(self):
        xmin, xmax = self.img.ax.get_xlim()
        if self.v_LVal.text() and int(self.v_LVal.text())>0:
            left_frame = int(self.v_LVal.text())
        else:
            if xmin < 0: left_frame = 0
            else: left_frame = int(xmin)

        if self.v_RVal.text() and int(self.v_RVal.text())>0:
            right_frame = int(self.v_RVal.text())
        else:
            right_frame = int(xmax)
        if self.v_Output.text():
            fits.writeto(self.v_Output.text()+'.fits', self.serie[left_frame:right_frame])
        else:
            fits.writeto(self.v_Input.text()+'.fits', self.serie[left_frame:right_frame])            

class Imager(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.main_widget = parent
        self.main_layout = QGridLayout()
        self.setFixedSize(640, 480)
    
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.main_layout.addWidget(self.canvas, 0, 0)
        self.main_layout.addWidget(self.toolbar, 1, 0)
        self.setLayout(self.main_layout)

        self.ax = self.fig.add_subplot(111)
        self.ax.plot(random.random(100))
        