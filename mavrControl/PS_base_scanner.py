from os.path import join, isdir, basename
from os import walk, makedirs, system
import sys
from mavr.processing import get_ps
from time import time
from numpy import mean

def scan_year(params, loading_bars=False):
    sets = list(walk(params['input']['year']))[0][1]
    if loading_bars:
        loading_bars['sets'].setRange(0, len(sets))
        num_set = 0
    for month in sets:
        params['input']['set'] = join(params['input']['year'], month)
        params['output']['set'] = join(params['output']['year'], month)
        scan_set(params, loading_bars)
        if loading_bars:
            num_set += 1
            loading_bars['sets'].setValue(num_set)

def scan_set(params, loading_bars):
    if isdir(join(params['input']['set'], 'cut')):
        params['input']['subdir'] = join(params['input']['set'], 'cut')
    elif isdir(join(params['input']['set'], 'rebuild')):
        params['input']['subdir'] = join(params['input']['set'], 'rebuild')
    elif isdir(join(params['input']['set'], 'rebuilded')):
        params['input']['subdir'] = join(params['input']['set'], 'rebuilded')
    else:
        print('Error')
        return 1
    nights = list(walk(params['input']['subdir']))[0][1]
    if loading_bars:
        loading_bars['nights'].setRange(0, len(nights))
        num_night = 0
    for night in nights:
        params['input']['night'] = join(params['input']['subdir'], night)
        params['output']['night'] = join(params['output']['set'], night)
        scan_night(params, loading_bars)
        if loading_bars:
            num_night += 1
            loading_bars['nights'].setValue(num_night)

def scan_night(params, loading_bars=False):
    stars = []
    try:
        makedirs(params['output']['night'])
    except:
        pass
    for root, dirs, files in walk(params['input']['night']):
        for name in files:
            if not name.endswith('.dat') and name.startswith('dark') and name.startswith('flat') and 'moon' in name:
                continue
            else:
                stars.append(join(root, name))
        break
    if loading_bars:
        loading_bars['stars'].setRange(0, len(stars))
        num_star = 0
    for star in stars:
        get_ps(star, diff=params['diff'], acf=params['acf'], save=params['save'], shape=params['shape'], output=params['output']['night'], rmbgr_on=params['rmbgr'])
        if loading_bars:
            num_star += 1
            loading_bars['stars'].setValue(num_star)