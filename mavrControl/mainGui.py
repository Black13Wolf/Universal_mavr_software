from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from __init__ import __version__
import sys

from PSCalculator import PSCalculator
from Rebuilder import Rebuilder

class mainGUI(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.startWidget = QWidget()
        self.startLayout = QGridLayout()
        self.label = QLabel('LINUX MAVR SOFTWARE. VER: {}'.format(__version__))
        self.label.setStyleSheet('font-size: 20pt')
        
        #____ MainMenu
            #____ Menu buttons
        mainMenu = self.menuBar() 
        m_Auto = mainMenu.addMenu('Automatisation')
        m_Obs = mainMenu.addMenu('Observations')
        m_Help = mainMenu.addMenu('Help')
            #____ Menu signals
        m_Auto_PSCalculator = QAction(QIcon(''), 'PS Calculator', self)
        m_Auto_PSCalculator.setStatusTip('Автоматический расчет спектра мощности по году, сету, ночи или файлу')
        m_Auto_PSCalculator.triggered.connect(self.t_PSCalculator)
        m_Auto.addAction(m_Auto_PSCalculator)

        m_Auto_Rebuilder = QAction(QIcon(''), 'Rebuilder', self)
        m_Auto_Rebuilder.setStatusTip('Автоматическая пересборка сырых данных камеры Andor в единые файлы формата "dat"')
        m_Auto_Rebuilder.triggered.connect(self.t_Rebuilder)
        m_Auto.addAction(m_Auto_Rebuilder)

        #____ Widgets
        self.widgets = {
            'PSCalculator' : PSCalculator(),
            'Rebuilder' : Rebuilder()
        }
        
        #____ Layout Settings
        self.startLayout.addWidget(self.label, 0, 0)
        self.startWidget.setLayout(self.startLayout)
        self.setCentralWidget(self.startWidget)
    
    def t_PSCalculator(self):
        self.setCentralWidget(self.widgets['PSCalculator'])
    
    def t_Rebuilder(self):
        self.setCentralWidget(self.widgets['Rebuilder'])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    g = mainGUI()
    g.show()
    app.exec_()