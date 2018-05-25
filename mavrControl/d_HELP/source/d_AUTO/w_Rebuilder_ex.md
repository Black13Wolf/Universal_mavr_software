[Назад][Back]

# Модуль **Автоматизация -> Пересборщик**

## Описание

Модуль предназначен для приведения выходных файлов камер Andor (SpoolDataXX.dat или spool.tif) и SWIR InGaAs Snake-640 (Serie tif) к бинарному формату, который используется большинством программ обработки группы.

## Руководство программиста

---
### 1. Состав модуля

#### 1.1 Используемые библиотеки Python
- PyQt5
- sys
- os
- time
- threading
- numpy
- PIL (pillow)

#### 1.2 Компоненты модуля
- **w_Rebuilder.py**: Содержит описание виджета, отображаемого в GUI
- **p_Rebuild.py**: Содержит описание потока, запускаемого параллельно основному
- **m_Rebuild.py**: Содержит описание различных функций для выполнения алгоритма

---
### 2. Исходный код модулей

#### 2.1 **w_Rebuilder.py**
```python
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from os.path import join, abspath, dirname, pardir
from time import sleep
from threading import Thread, active_count

from . import p_Rebuild as rebuilder

class Rebuilder(QWidget):
    sign_set_progress = pyqtSignal(int, int)
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.mainGui = parent        
        self.main_layout = QGridLayout()

        self.b_Input = QPushButton('Choose path')
        self.b_Input.clicked.connect(self.c_Input)
        self.b_Output = QPushButton('Choose path')
        self.b_Output.clicked.connect(self.c_Output)
        self.b_Start = QPushButton('Пересобрать')
        self.b_Start.clicked.connect(self.c_Start)        
        
        self.l_Input = QLabel('Input path: ')
        self.v_Input = QLineEdit()
        self.v_Input.setFixedWidth(300)
        self.v_Input.textChanged.connect(self.s_Def_path)
        self.l_Output = QLabel('Output path: ')
        self.v_Output = QLineEdit()
        self.v_Output.setFixedWidth(300)

        self.l_Type = QLabel('Type: ')
        self.v_Type = QComboBox()
        self.v_Type.addItems(['Set', 'Night', 'Star'])
        
        self.progressbar = QProgressBar()
        self.sign_set_progress.connect(self.slot_set_progress)
        self.progressbar.hide()

        self.main_layout.addWidget(self.l_Input, 0, 0)
        self.main_layout.addWidget(self.v_Input, 0, 1, 1, 2)
        self.main_layout.addWidget(self.b_Input, 0, 3)
        self.main_layout.addWidget(self.l_Output, 1, 0)
        self.main_layout.addWidget(self.v_Output, 1, 1, 1, 2)
        self.main_layout.addWidget(self.b_Output, 1, 3)
        self.main_layout.addWidget(self.l_Type, 2, 0)
        self.main_layout.addWidget(self.v_Type, 2, 1)
        self.main_layout.addWidget(self.b_Start, 2, 2, 1, 2)
        self.main_layout.addWidget(self.progressbar, 3, 0, 1, 4)
        self.setLayout(self.main_layout)

    def c_Input(self):
        self.v_Input.setText(QFileDialog.getExistingDirectory(self, "Select Input Directory", '.', QFileDialog.ShowDirsOnly))

    def c_Output(self):
        self.v_Output.setText(QFileDialog.getExistingDirectory(self, "Select Output Directory", '.', QFileDialog.ShowDirsOnly))

    def c_Start(self):
        self.b_Start.setEnabled(False)
        self.b_Input.setEnabled(False)
        self.b_Output.setEnabled(False)
        self.progressbar.show()

        params = {}
        params['type'] = self.v_Type.currentText().lower()
        params['input'] = {self.v_Type.currentText().lower() : self.v_Input.text()}
        params['output'] = {self.v_Type.currentText().lower() : self.v_Output.text()}
        self.th = Thread(target = rebuilder.rebuild_start, args=(params, self))
        self.th.start()
                
    def s_Def_path(self):
        if self.v_Output.text() == '' and self.v_Type.currentText().lower() == 'star':
            self.v_Output.setText(join(self.v_Input.text()))
        elif self.v_Output.text() == '' and (self.v_Type.currentText().lower() == 'night' or self.v_Type.currentText().lower() == 'set'):
            self.v_Output.setText(join(self.v_Input.text(), 'rebuild'))
        
    def slot_set_progress(self, v, maxv):
        self.progressbar.setRange(0, maxv)
        self.progressbar.setValue(v)
        if v == maxv:
            self.b_Start.setEnabled(True)
            self.b_Input.setEnabled(True)
            self.b_Output.setEnabled(True)
```
#### 2.2 **p_Rebuild.py**
```python
from numpy import *
from os import walk, makedirs
from os.path import isdir, join, isfile, dirname

from .m_Rebuild import *

def rebuild_start(params, parent = None):
    if params['type'] == 'set':
        params['nights'] = {}
        params['nights']['inputs'] = []
        params['nights']['outputs'] = []
        append_i = params['nights']['inputs'].append
        append_o = params['nights']['outputs'].append
        for root, dirs, files in walk(params['input']['set']):
            for d in dirs:
                append_i(join(params['input']['set'], d))
                append_o(join(params['output']['set'], d))
            break
        params['stars'] = {}
        params['stars']['inputs'] = []
        params['stars']['outputs'] = []        
        append_i = params['stars']['inputs'].append
        append_o = params['stars']['outputs'].append
        for n in range(len(params['nights']['inputs'])):
            for root, dirs, files in walk(params['nights']['inputs'][n]):
                for d in dirs:
                    append_i(join(root, d))
                    append_o(join(params['nights']['outputs'][n], d))
                break

    elif params['type'] == 'night':
        params['stars'] = {}
        params['stars']['inputs'] = []
        params['stars']['outputs'] = []        
        append_i = params['stars']['inputs'].append
        append_o = params['stars']['outputs'].append
        for root, dirs, files in walk(params['input']['night']):
            for d in dirs:
                append_i(join(root, d))
                append_o(join(params['output']['night'], d))
            break

    elif params['type'] == 'star':
        params['stars'] = {}
        params['stars']['inputs'] = [params['input']['star'],]
        params['stars']['outputs'] = [params['output']['star'],]

    params['files'] = len(params['stars']['inputs'])
    parent.sign_set_progress.emit(0, params['files'])

    for i in range(len(params['stars']['inputs'])):
        rebuild_star(params['stars']['inputs'][i], params['stars']['outputs'][i])
        parent.sign_set_progress.emit(i+1, params['files'])
        
def rebuild_star(path_i, path_o):
    try:
        makedirs(dirname(path_o))
    except:
        pass
    print(path_i)
    serie_type = check_serie_type(path_i)

    if not serie_type:
        return 0
    if serie_type == 'dat':
        spool(path_i, path_o)
    elif serie_type == 'big_tif':
        big_tif(path_i, path_o)       
    elif serie_type == 'serie_tif':
        serie_tif(path_i, path_o)

def check_serie_type(path_to_dir):
    files_num = 0
    for root, dirs, files in walk(path_to_dir):
        files_num += len(files)
    if files_num == 0:
        print(path_to_dir+' is empty folder.')
        return 0
    elif isdir(join(path_to_dir, 'spool')):
        return 'dat'
    elif isfile(join(path_to_dir, 'spool.tif')):
        return 'big_tif'
    elif files_num > 100 and files[-1].endswith('.tif'):
        return 'serie_tif'
    else:
        print(path_to_dir+' have unknown format')
```
#### 2.3 **m_Rebuild.py**
```python
def spool(main_path, output_dir):
    from os import walk, path
    from numpy import memmap, where
    spools=[]
    for root, dirs, files in walk(path.join(main_path, 'spool')):
        for d in dirs:
            if d.startswith('Spool'):
                spools.append(d)
    spool_num = 0
    for spool in spools:
        spool_num += 1
        files = list(walk(path.join(main_path, 'spool', spool)))[0][2]
        files.sort()
        for f in files:
            datfile = memmap(path.join(main_path, 'spool', spool, f), dtype='uint16')
            if any(datfile == 0):
                for i in where(datfile == 0)[0]:
                    if datfile[i:i+10].sum()==0:
                        if i:
                            with open(path.join(output_dir+'.dat'), 'ab') as f:
                                f.write(datfile[:i])
                        break
                else:
                    with open(path.join(output_dir+'.dat'), 'ab') as f:
                        f.write(datfile)
            else:
                with open(path.join(output_dir+'.dat'), 'ab') as f:
                    f.write(datfile)
        
def serie_tif(path_to_dir, output_dir):
    from PIL import Image
    from numpy import array, uint16
    from os import walk, path

    files = list(walk(path_to_dir))[0][2]
    for f in files:
        if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png') or f.endswith('.tif') or f.endswith('.gif'):
            img_path = path.join(path_to_dir, f)
            img = Image.open(img_path).convert('I')
            img = array(img).astype('uint16')
            with open(path.join(output_dir+'.dat'), 'ab') as output:
                output.write(img)

def big_tif(path_to_dir, output_dir):
    from PIL import Image
    from numpy import array, uint16
    from os import stat, path, walk

    if stat(path.join(path_to_dir, 'spool.tif')).st_size == 8:
        print('{}: Ошибка в директории. Пересоберите вручную.'.format(main_path))
        return 0
    tiffs = list(walk(path_to_dir))[0][2]
    if len(tiffs) == 1:
        serie = Image.open(path.join(path_to_dir, 'spool.tif'))
        frames = serie.n_frames
        for i in range(frames):
            serie.seek(i)
            with open(path.join(output_dir+'.dat'), 'ab') as output:
                output.write(array(serie).astype('uint16'))
    else:
        for f in tiffs:
            if stat(path.join(path_to_dir, f)).st_size == 8:
                continue
            else:
                serie = Image.open(path.join(path_to_dir, f))
                frames = serie.n_frames
                for i in range(frames):
                    serie.seek(i)
                    with open(path.join(output_dir+'.dat'), 'ab') as output:
                        output.write(array(serie).astype('uint16'))
```

---
### 3. Алгоритм работы

Будет описан позже



[Back]: ../index.html