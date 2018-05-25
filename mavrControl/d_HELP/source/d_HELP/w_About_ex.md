[Назад][Back]

# Модуль **Помощь -> О программе**

## Описание

Модуль, который выводит информацию о текущей версии программы, о разработчике и контактах с ним, а так же дает возможность проверить обновления и обновить программу до последней версии

## Руководство программиста

---
### 1. Состав модуля:

#### 1.1 Используемые пакеты Python:
- PyQt5
- urllib
- json

#### 1.2 Компоненты модуля:
- **w_About.py**: Единственный компонент, включающий в себя и виджет отображения в главном GUI, и алгоритм отображения информации и обновления

---
### 2. Исходный код модуля:

#### 2.1. **w_About.py**:
```python
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import urllib.request
import json

class About(QWidget):
    def __init__(self,  __version__, parent = None):
        self.ver = __version__
        self.mainGui = parent
        QWidget.__init__(self, parent)
        self.main_layout = QGridLayout()

        self.l_name = sLabel('Название: Universal Mavr Software')
        self.l_version = sLabel('Версия: {}'.format(self.ver))
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

        self.main_layout.addWidget(self.l_name)
        self.main_layout.addWidget(self.l_version)
        self.main_layout.addWidget(self.l_programmer)
        self.main_layout.addWidget(self.l_mail)
        self.main_layout.addWidget(self.b_Check)
        self.main_layout.addWidget(self.l_git_version)
        self.main_layout.addWidget(self.b_Update)
          
        self.setLayout(self.main_layout)

    def c_Check_updates(self):
        try:
            with urllib.request.urlopen('https://api.github.com/repos/Black13Wolf/linux_mavr_software/tags') as url:
                data = json.loads(url.read().decode())
        except:
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

        if self.ver == self.last_update:
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
        
        from pip._internal import main as pip
        pip(['install', last_update['tarball_url'], '--user', '--proxy=http://squid.sao.ru:8080'])

class sLabel(QLabel):
    def __init__(self, text, parent = None):
        QLabel.__init__(self, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setText(text)
        self.setFixedWidth(450)
```

---
### 3. Алгоритм работы

Будет описан позднее

[Back]: ../index.html