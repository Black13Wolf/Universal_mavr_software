from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#import markdown
try:
    from .helps import *
except:
    from helps import *

class Help(QWidget):
    def __init__(self, parent = None):
        self.mainGui = parent
        QWidget.__init__(self, parent)
        self.layout = QGridLayout()

        self.l_Menu = QLabel('Выберите пункт меню: ')
        self.v_Menu = QComboBox()
        self.v_Menu.addItems(['', 'Автоматизация', 'Наблюдения', 'Помощь'])
        self.v_Menu.currentTextChanged.connect(self.ch_Menu)

        self.l_Name = QLabel('Выберите модуль: ')
        self.v_Name = QComboBox()
        self.v_Name.currentTextChanged.connect(self.ch_Name)
        
        self.browser = QTextBrowser()
        self.browser.setFixedSize(450, 200)
        
        self.layout.addWidget(self.l_Menu, 0, 0)
        self.layout.addWidget(self.v_Menu, 0, 1)
        self.layout.addWidget(self.l_Name, 1, 0)
        self.layout.addWidget(self.v_Name, 1, 1)
        self.layout.addWidget(self.browser, 2, 0, 1, 2)
        
        self.setLayout(self.layout)

        #with open('helps\\test.md', encoding='utf-8') as f:
        #    self.test_test = f.read()
        #    self.browser.setHtml(markdown.markdown(self.test_test))
    def ch_Menu(self):
        self.v_Name.clear()
        if self.v_Menu.currentText() == 'Автоматизация':
            self.v_Name.addItems(["", "Расчет спектра мощности", "Пересборщик"])
        elif self.v_Menu.currentText() == 'Наблюдения':
            self.v_Name.addItems(['',])
        elif self.v_Menu.currentText() == 'Помощь':
            self.v_Name.addItems(["", "О программе", "Помощь"])
    
    def ch_Name(self):
        self.browser.clear()