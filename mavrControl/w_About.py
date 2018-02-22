from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import urllib.request
import json

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
        
        self.l_git_version = sLabel('')
        self.l_git_version.hide()
        
        self.b_Check = QPushButton('Проверить обновления')
        self.b_Check.clicked.connect(self.c_Check_updates)
        self.b_Check.setFixedHeight(25)
        
        self.b_Update = QPushButton('Обновить')
        self.b_Update.clicked.connect(self.c_Update)
        self.b_Update.setFixedHeight(25)
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
        proxies = {
    "http" : "http://squid.sao.ru:8080",
    "https" : "http://squid.sao.ru:8080",
        }
        proxy_support = urllib.request.ProxyHandler(proxies)
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        with urllib.request.urlopen('https://api.github.com/repos/Black13Wolf/linux_mavr_software/tags') as url:
            data = json.loads(url.read().decode())
        self.last_update = data[0]['name']

        if __version__ == self.last_update:
            self.l_git_version.setText('У Вас установлена самая последняя версия.')
        else:
            self.l_git_version.setText('Последняя версия: {}'.format(self.last_update))           
            self.b_Update.show() 
        self.l_git_version.show()

    def c_Update(self):
        self.b_Check.setEnabled(False)
        self.b_Update.setEnabled(False)
        proxies = {
            "http" : "http://squid.sao.ru:8080",
            "https" : "http://squid.sao.ru:8080",
        }
        proxy_support = urllib.request.ProxyHandler(proxies)
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        with urllib.request.urlopen('https://api.github.com/repos/Black13Wolf/linux_mavr_software/tags') as url:
            data = json.loads(url.read().decode())
        last_update = data[0]
        self.mainGui.close()

class sLabel(QLabel):
    def __init__(self, text, parent = None):
        QLabel.__init__(self, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setText(text)
        self.setFixedWidth(450)
        