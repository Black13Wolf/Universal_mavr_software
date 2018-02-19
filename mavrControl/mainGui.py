from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
try:
    from . import __version__
except:
    from __init__ import __version__
import sys
try:    
    from .PSCalculator import PSCalculator
    from .Rebuilder import Rebuilder
    from .About import About
except:
    from PSCalculator import PSCalculator
    from Rebuilder import Rebuilder
    from About import About

class mainGUI(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.startWidget = QWidget()
        self.startLayout = QGridLayout()
        self.setWindowTitle('LINUX MAVR SOFTWARE. VER: {}'.format(__version__))
        self.label = QLabel('LINUX MAVR SOFTWARE. VER: {}'.format(__version__))
        self.label.setStyleSheet('font-size: 20pt')
        
        #____ MainMenu
            #____ Menu buttons
        mainMenu = self.menuBar() 
        m_Auto = mainMenu.addMenu('Автоматизация')
        m_Obs = mainMenu.addMenu('Наблюдения')
        m_Help = mainMenu.addMenu('Помощь')
            #____ Menu signals
        m_Auto_PSCalculator = QAction(QIcon(''), 'Расчет спектра мощности', self)
        m_Auto_PSCalculator.setStatusTip('Автоматический расчет спектра мощности по году, сету, ночи или файлу')
        m_Auto_PSCalculator.triggered.connect(self.t_PSCalculator)
        m_Auto.addAction(m_Auto_PSCalculator)

        m_Auto_Rebuilder = QAction(QIcon(''), 'Пересборщик', self)
        m_Auto_Rebuilder.setStatusTip('Автоматическая пересборка сырых данных камеры Andor в единые файлы формата "dat"')
        m_Auto_Rebuilder.triggered.connect(self.t_Rebuilder)
        m_Auto.addAction(m_Auto_Rebuilder)
            
            #____ Help signals
        m_Help_About = QAction(QIcon(''), 'О программе', self)
        m_Help_About.setStatusTip('Информация о программе')
        m_Help_About.triggered.connect(self.t_About)
        m_Help.addAction(m_Help_About)

        #____ Layout Settings
        self.startLayout.addWidget(self.label, 0, 0)
        self.startWidget.setLayout(self.startLayout)
        self.setCentralWidget(self.startWidget)
    
    def t_PSCalculator(self):
        self.setCentralWidget(PSCalculator(parent = self))
    
    def t_Rebuilder(self):
        self.setCentralWidget(Rebuilder(parent = self))
    
    def t_About(self):
        self.setCentralWidget(About(parent = self))
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    g = mainGUI()
    g.show()
    app.exec_()