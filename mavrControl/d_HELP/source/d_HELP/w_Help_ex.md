[Назад][Back]

# Модуль **Помощь -> Помощь**

## Описание

Модуль помощи, который отображают всю информацию о модулях данной программы

## Руководство программиста

---
### 1. Состав модуля

#### 1.1. Используемые пакеты 
- PyQt5
- functools
- os

#### 1.2. Компоненты модуля
- **w_Help.py**: Единственный компонент, включающий в себя и виджет отображения в главном GUI, и алгоритм отображения помощи

---
### 2. Исходный код

#### 2.1. **w_Help.py**:

```python
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from functools import partial
from os.path import join, dirname
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Help(QWidget):
    def __init__(self, parent = None):
        self.mainGui = parent
        QWidget.__init__(self, parent)
        self.main_layout = QGridLayout()

        self.browser = Browser(parent = self)
        self.main_layout.addWidget(self.browser, 0, 0)
        self.setLayout(self.main_layout)

class Browser(QWebEngineView):
    def __init__(self, parent = None):
        self.mainWidget = parent
        QWebEngineView.__init__(self, parent)
        self.setFixedSize(800,600)
        self.setUrl(QUrl.fromLocalFile(join(dirname(__file__), 'source', 'index.html')))
```

---
### 3. Алгоритм работы

Будет описан позднее

[Back]: ../index.html