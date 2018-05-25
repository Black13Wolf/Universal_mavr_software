[Назад][Back]

# Модуль **Автоматизация -> Расчет СПМ**

## Описание

Модуль предназначен для автоматического расчета спектров мощности (СПМ) и автокорреляционных функций (АКФ).
Способен рассчитать спектр мощности года/сета/ночи наблюдений или отдельно взятого объекта

## Руководство программиста

---
### 1. Состав модуля

#### 1.1 Используемые библиотеки Python
- PyQt5
- sys
- threading
- ast
- time
- os
- numpy
- astropy
- gc
- matplotlib

#### 1.2 Компоненты модуля
- **w_PSCalc.py**: Содержит описание виджета, отображаемого в GUI
- **p_PSBaseScan.py**: Содержит описание потока, запускаемого параллельно основному
- **m_PSCalc.py**: Содержит описание различных функций для выполнения алгоритма

---
### 2. Исходный код модулей

#### 2.1 **w_PSCalc.py**:
```python
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from threading import Thread, active_count
from ast import literal_eval
from time import sleep

from . import p_PSBaseScan as base_scan
from .m_PSCalc import get_ps
    
class PSCalculator(QWidget):
    sign_set_progress = pyqtSignal(int, int)    
    def __init__(self, parent = None):
        self.mainGui = parent
        QWidget.__init__(self, parent)
        self.main_layout = QGridLayout()

        self.b_Start = QPushButton('Start')
        self.b_Start.clicked.connect(self.c_Start)
        self.b_Input = QPushButton('Choose path')
        self.b_Input.clicked.connect(self.c_Input)
        self.b_Output = QPushButton('Choose path')
        self.b_Output.clicked.connect(self.c_Output)        
        
        self.l_Input = QLabel('Input path: ')
        self.v_Input = QLineEdit()
        self.v_Input.setFixedWidth(300)
        self.l_Output = QLabel('Output path: ')
        self.v_Output = QLineEdit()
        self.v_Output.setFixedWidth(300)
        
        self.l_Type = QLabel('Type: ')
        self.v_Type = QComboBox()
        self.v_Type.addItems(['Year', 'Set', 'Night', 'Star'])
        
        self.l_Diff = QLabel('Diff frames: ')
        self.v_Diff = QSpinBox()
        self.v_Diff.setValue(1)
        self.v_Diff.setMaximum(50)
        
        self.l_Acf = QLabel('ACF')
        self.v_Acf = QComboBox()
        self.v_Acf.addItems(['ON', 'OFF'])
        
        self.l_Save = QLabel('Save: ')
        self.v_Save = QComboBox()
        self.v_Save.addItems(['fits', 'OFF'])

        self.l_Shape = QLabel('Shape: ')
        self.v_Shape = QComboBox()
        self.v_Shape.addItems(['(1024,1024)', '(512,512)', '(2048,2048)', '(4096,4096)', '(512, 640)'])

        self.l_Rmbgr = QLabel('Removing BGR: ')
        self.v_Rmbgr = QComboBox()
        self.v_Rmbgr.addItems(['ON', 'OFF'])

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
        self.main_layout.addWidget(self.l_Diff, 2, 2)
        self.main_layout.addWidget(self.v_Diff, 2, 3)
        self.main_layout.addWidget(self.l_Acf, 3, 0)
        self.main_layout.addWidget(self.v_Acf, 3, 1)
        self.main_layout.addWidget(self.l_Save, 3, 2)
        self.main_layout.addWidget(self.v_Save, 3, 3)
        self.main_layout.addWidget(self.l_Shape, 4, 0)
        self.main_layout.addWidget(self.v_Shape, 4, 1)
        self.main_layout.addWidget(self.l_Rmbgr, 4, 2)
        self.main_layout.addWidget(self.v_Rmbgr, 4, 3)
        self.main_layout.addWidget(self.b_Start, 10, 1, 1, 2)
        self.main_layout.addWidget(self.progressbar, 11, 0, 1, 4)
        self.setLayout(self.main_layout)
    

    def c_Start(self):
        self.b_Start.setEnabled(False)
        self.b_Input.setEnabled(False)
        self.b_Output.setEnabled(False)
        self.progressbar.show()
        params = {}
        params['input'] = {self.v_Type.currentText().lower() : self.v_Input.text()}
        params['output'] = {self.v_Type.currentText().lower() : self.v_Output.text()}
        params['type'] = self.v_Type.currentText().lower()
        params['diff'] = self.v_Diff.value() 

        if self.v_Acf.currentText() == 'ON':
            params['acf'] = True
        elif self.v_Acf.currentText() == 'OFF':
            params['acf'] = False

        if self.v_Save.currentText() == 'OFF':
            params['save'] = False
        else:
            params['save'] = self.v_Save.currentText()

        params['shape'] = literal_eval(self.v_Shape.currentText())

        if self.v_Rmbgr.currentText() == 'ON':
            params['rmbgr'] = True
        elif self.v_Rmbgr.currentText() == 'OFF':
            params['rmbgr'] = False

        if params['type'] == 'year':
            self.th = Thread(target = base_scan.scan_year, args=(params, self))
        elif params['type'] == 'set':
            self.th = Thread(target = base_scan.scan_set, args=(params, self))
        elif params['type'] == 'night':
            self.th = Thread(target = base_scan.scan_night, args=(params, self))
        elif params['type'] == 'star':
            self.th = Thread(target = get_ps, args = (params['input']['star'],), kwargs={'diff':params['diff'], 'acf':params['acf'], 'save':params['save'], 'shape':params['shape'], 'output':params['output']['star'], 'rmbgr_on':params['rmbgr']})
        else:
            return 1
        self.th.start()

    def c_Input(self):
        if self.v_Type.currentText().lower() == 'star':
            self.v_Input.setText(QFileDialog.getOpenFileName(self, 'Select Input Dat File', '.', "DAT (*.dat)")[0])
        else:
            self.v_Input.setText(QFileDialog.getExistingDirectory(self, "Select Input Directory", '.', QFileDialog.ShowDirsOnly))

    def c_Output(self):
        self.v_Output.setText(QFileDialog.getExistingDirectory(self, "Select Output Directory", '.', QFileDialog.ShowDirsOnly))
    
    def slot_set_progress(self, v, maxv):
        self.progressbar.setRange(0, maxv)
        self.progressbar.setValue(v)
        if v == maxv:
            self.b_Start.setEnabled(True)
            self.b_Input.setEnabled(True)
            self.b_Output.setEnabled(True)
```

#### 2.2 **p_PSBaseScan.py**:
```python
from os.path import join, isdir, basename
from os import walk, makedirs, system, listdir
import sys
from time import time
from numpy import mean

from .m_PSCalc import get_ps
    
def scan_year(params, parent = None, level = 0):
    sets = list(walk(params['input']['year']))[0][1]
    for month in sets:
        params['input']['set'] = join(params['input']['year'], month)
        params['output']['set'] = join(params['output']['year'], month)
        print('\t'*level + params['input']['set'])
        scan_set(params, parent, level+1)
        
def scan_set(params, parent = None, level = 0):
    if isdir(join(params['input']['set'], 'cut')):
        params['input']['subdir'] = join(params['input']['set'], 'cut')
    elif isdir(join(params['input']['set'], 'rebuild')):
        params['input']['subdir'] = join(params['input']['set'], 'rebuild')
    elif isdir(join(params['input']['set'], 'rebuilded')):
        params['input']['subdir'] = join(params['input']['set'], 'rebuilded')
    else:
        params['input']['subdir'] = params['input']['set']
    
    nights = list(walk(params['input']['subdir']))[0][1]
    for night in nights:
        params['input']['night'] = join(params['input']['subdir'], night)
        params['output']['night'] = join(params['output']['set'], night)
        print('\t'*level + params['input']['night'])        
        scan_night(params, parent)
        
def scan_night(params, parent = False, level = 0):
    stars = []
    try:
        makedirs(params['output']['night'])
        print('Dir created: '+params['output']['night'])
    except:
        print('Error create: '+params['output']['night'])
    for root, dirs, files in walk(params['input']['night']):
        for name in files:
            if not name.endswith('.dat') or name.startswith('dark') or name.startswith('flat') or 'moon' in name or 'bin' in name:
                continue
            else:
                stars.append(join(root, name))
        break
    i=0
    parent.sign_set_progress.emit(i, len(stars))    
    for star in stars:
        print('\t'*level + star)                
        get_ps(star, diff=params['diff'], acf=params['acf'], save=params['save'], shape=params['shape'], output=params['output']['night'], rmbgr_on=params['rmbgr'])
        i+=1
        parent.sign_set_progress.emit(i, len(stars))
        
```

#### 2.3 **m_PSCalc.py**:
```python
def get_ps(path_to_dat, diff=0, acf=False, save=False, shape=(512,512), output=False, rmbgr_on=True):
    from numpy import memmap, zeros, fft, any
    from os.path import basename, join
    if output:
        output_file = join(output, basename(path_to_dat))
    else:
        output_file = path_to_dat
    serie = memmap(path_to_dat, dtype='uint16').astype('float32')
    if shape == (512, 640): lims = (512, 640)
    else: lims = (512,512)
    frames = int(serie.size/lims[0]/lims[1])
    serie = serie.reshape((frames, lims[0], lims[1]))

    serie, frames = partickle_searcher(serie, path_to_dat, output_file, output)

    output_ps = zeros(shape)
    for num in range(frames):
        frame = zeros(shape)
        if diff and num<frames-diff:
            frame[:lims[0], :lims[1]] += serie[num] - serie[num+diff]
            frame[:lims[0], :lims[1]] += serie[num] - serie[num+diff]
        else:
            frame[:lims[0], :lims[1]] += serie[num]
        output_ps += abs(fft.fft2(frame)**2)                                                                                                                                                                                                                                                                                                                                                                                            
    output_ps /= frames  
    if rmbgr_on: 
        output_ps = fft.fftshift(rmbgr(fft.fftshift(output_ps), 100))
          
    if acf: output_acf = abs(fft.ifft2(fft.fftshift(output_ps)))
    if save:
        if save == 'fits':
            from astropy.io import fits
            fits.writeto(output_file+'_ps_diff{}_shape{}.{}'.format(diff, shape, save), fft.fftshift(output_ps))
            if acf: fits.writeto(output_file+'_acf_diff{}_shape{}.{}'.format(diff, shape, save), fft.fftshift(output_acf))
        else:
            print('Unknown format: {}'.format(save))
        import gc
        memory = gc.collect()
        print('Очищено объектов из памяти: {}'.format(memory))
    else:
        if acf:
            return fft.fftshift(output_ps), fft.fftshift(output_acf)
        else:
            return fft.fftshift(output_ps)
    
def rmbgr(middle_star, xlim): 
    from numpy import mean
    outbound = middle_star[0:xlim] 
    slice_out = mean(outbound, axis=0) 
    middle_star_clean = middle_star - slice_out 
    return middle_star_clean 

def partickle_searcher(data, name, output_path, log_path):
    print('Поиск частиц')
    print(data.shape)
    from numpy import std, array, mean, where, delete, save
    from matplotlib.pyplot import clf, plot, savefig, hlines
    from os.path import join
    
    sf = data.shape[0]
    mvs = []
    for i in data:
        mvs.append(i.max())
    mvs = array(mvs)
    mvs -= mvs.min()
    mvs /= mvs.max()
    ad = mean(mvs)
    print('Коэфф: {:.2f}'.format(ad))
    plot(mvs)
    k = mean(mvs)*2 + std(mvs)*4
    hlines(k, 0, data.shape[0], color='red')
    savefig(output_path+'.maxvalues.png')
    clf()
    bad_frames = where(mvs > k)[0]
    
    if 0 < len(bad_frames) < data.shape[0] * 0.025:
        data = delete(data, bad_frames, axis = 0)
    print('Конец поиска частиц')
    with open(join(log_path, 'logfile.txt'), 'a+') as log:
        log.write('{}\t koeff: {:.2f}\t Bad frames: {}({:.2f}) \t {}\n'.format(name, ad, len(bad_frames), (len(bad_frames)/sf)*100, str(bad_frames)))
    return data, data.shape[0]

```

---
### 3. Алгоритм работы

Будет описан позже


[Back]: ../index.html