from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import socket

try:
    from . import __version__
except:
    from __init__ import __version__

class About(QWidget):
    def __init__(self, parent = None):
        self.mainGui = parent
        QWidget.__init__(self, parent)
        self.layout = QGridLayout()

        self.l_name = sLabel('Название: Linux Mavr Software')
        self.l_version = sLabel('Версия: {}'.format(__version__))
        self.l_programmer = sLabel('Разработчик: Бескакотов А. С.')
        self.l_mail = sLabel('eMail: beskakotov.as@gmail.com')

        self.b_Check = QPushButton('Проверить обновления')
        self.b_Check.clicked.connect(self.c_Check_updates)
        
        self.l_git_version = sLabel('')
        self.l_git_version.hide()
        
        self.b_Update = QPushButton('Обновить')
        self.b_Update.clicked.connect(self.c_Update)
        self.b_Update.hide()

        self.layout.addWidget(self.l_name)
        self.layout.addWidget(self.l_version)
        self.layout.addWidget(self.l_programmer)
        self.layout.addWidget(self.l_mail)
        self.layout.addWidget(self.b_Check)
        self.layout.addWidget(self.l_git_version)
        self.layout.addWidget(self.b_Update)
          
        self.setLayout(self.layout)

    def c_Check_updates(self):
        self.last_version = '0.1.2'
        self.l_git_version.setText('Последняя версия: {}'.format(self.last_version))
        self.l_git_version.show()

    def c_Update(self):
        pass

class sLabel(QLabel):
    def __init__(self, text, parent = None):
        QLabel.__init__(self, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setText(text)
        