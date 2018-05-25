from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import webbrowser
from os.path import join, dirname
from time import sleep

from . import __version__
from .d_AUTO.w_PSCalc import PSCalculator
from .d_AUTO.w_Rebuilder import Rebuilder
from .d_OBS.w_HPMS import HPMS
from .d_HELP.w_About import About
from .d_HELP.w_Help import Help
from .d_WIN.w_starc_Mask import starc_MASK
from .d_WIN.w_starc_PS import starc_PS

class mainGUI(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.startWidget = QWidget()
        self.startLayout = QGridLayout()
        self.setWindowTitle('UMS v.: {}'.format(__version__))
        self.label = QLabel('Universal Mavr Software v.: {}'.format(__version__))
        self.label.setStyleSheet('font-size: 20pt')
        self.setFixedSize(0,0)
        
        #____ MainMenu
            #____ Menu buttons
        mainMenu = self.menuBar() 
        m_Auto = mainMenu.addMenu('Автоматизация')
        m_Obs = mainMenu.addMenu('Наблюдения')
        m_Win = mainMenu.addMenu('WindowsOnly')
        if not (sys.platform == 'win32' or sys.platform == 'win64'):
            m_Win.setEnabled(False)        
        m_Help = mainMenu.addMenu('Помощь')

            #____ AUTO signals
        m_Auto_PSCalculator = QAction(QIcon(''), 'Расчет СПМ', self)
        m_Auto_PSCalculator.setStatusTip('Автоматический расчет спектра мощности по году, сету, ночи или файлу')
        m_Auto_PSCalculator.triggered.connect(self.t_PSCalculator)
        m_Auto.addAction(m_Auto_PSCalculator)

        m_Auto_Rebuilder = QAction(QIcon(''), 'Пересборщик', self)
        m_Auto_Rebuilder.setStatusTip('Автоматическая пересборка сырых данных камеры Andor в единые файлы формата "dat"')
        m_Auto_Rebuilder.triggered.connect(self.t_Rebuilder)
        m_Auto.addAction(m_Auto_Rebuilder)

            #____ OBS signals
        m_Obs_HPMS = QAction(QIcon(''), 'Координаты HPMS', self)
        m_Obs_HPMS.setStatusTip('Пересчет координат для объектов с сильным собственным движением')
        m_Obs_HPMS.triggered.connect(self.t_HPMS)
        m_Obs.addAction(m_Obs_HPMS)            

            #____ OBS signals
        m_Win_Mask = QAction(QIcon(''), 'Рассчет масок', self)
        m_Win_Mask.setStatusTip('Рассчет положения пучков в масках используя модуль model.exe пакета starc')
        m_Win_Mask.triggered.connect(self.t_starc_Mask)
        m_Win.addAction(m_Win_Mask)

        m_Win_PS = QAction(QIcon(''), 'СПМ и АКФ', self)
        m_Win_PS.setStatusTip('Рассчет спектров мощности и АвтоКорреляционной функции звезд используя модуль spectr.exe пакета starc')
        m_Win_PS.triggered.connect(self.t_starc_PS)
        m_Win.addAction(m_Win_PS)  

            #____ HELP signals
        m_Help_About = QAction(QIcon(''), 'О программе', self)
        m_Help_About.setStatusTip('Информация о программе')
        m_Help_About.triggered.connect(self.t_About)
        m_Help.addAction(m_Help_About)

        m_Help_Help = QAction(QIcon(''), 'Помощь', self)
        m_Help_Help.setStatusTip('Информация о модулях программы')
        m_Help_Help.triggered.connect(self.t_Help)
        m_Help.addAction(m_Help_Help)
        #m_Help_Help.setEnabled(False)


        #____ Layout Settings
        self.startLayout.addWidget(self.label, 0, 0)
        self.startWidget.setLayout(self.startLayout)
        self.setCentralWidget(self.startWidget)
        self.setGeometry(320, 240, 0, 0)                
    
    def t_PSCalculator(self):
        self.setCentralWidget(PSCalculator(parent = self))
        self.update_sizes()
    
    def t_Rebuilder(self):
        self.setCentralWidget(Rebuilder(parent = self))
        self.update_sizes()
    
    def t_About(self):
        self.setCentralWidget(About(__version__, parent = self))
        self.update_sizes()
    
    def t_HPMS(self):
        self.setCentralWidget(HPMS(parent = self))
        self.update_sizes()

    def t_Help(self):
        self.setCentralWidget(Help(parent = self))
        self.update_sizes()

    def t_starc_Mask(self):
        self.setCentralWidget(starc_MASK(parent = self))
        self.update_sizes()
    
    def t_starc_PS(self):
        self.setCentralWidget(starc_PS(parent = self))
        self.update_sizes()

    def update_sizes(self):
        self.setGeometry(self.geometry().x(), self.geometry().y(), 0, 0)
        sleep(0.001)
        self.update()
        self.updateGeometry()
        self.setFixedSize(0,0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    g = mainGUI()
    g.show()
    app.exec_()