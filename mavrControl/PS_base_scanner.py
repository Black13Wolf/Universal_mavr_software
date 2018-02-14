from os.path import join, isdir, basename
from os import walk, makedirs, system
import sys
from mavr.processing import get_ps
from time import time
from numpy import mean

def scan_year(params, parent = None):
    sets = list(walk(params['input']['year']))[0][1]
    if parent:
        num_set = 0
        parent.set_progress.emit('sets', len(sets), num_set)
        
    for month in sets:
        params['input']['set'] = join(params['input']['year'], month)
        params['output']['set'] = join(params['output']['year'], month)
        scan_set(params, parent)
        if parent:
            num_set += 1
            parent.set_progress.emit('sets', len(sets), num_set)

def scan_set(params, parent = None):
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
    if parent:
        num_night = 0
        parent.set_progress.emit('nights', len(nights), num_night)
    for night in nights:
        params['input']['night'] = join(params['input']['subdir'], night)
        params['output']['night'] = join(params['output']['set'], night)
        scan_night(params, parent)
        if parent:
            num_night += 1
            parent.set_progress.emit('nights', len(nights), num_night)

def scan_night(params, parent = False):
    stars = []
    try:
        makedirs(params['output']['night'])
    except:
        pass
    for root, dirs, files in walk(params['input']['night']):
        for name in files:
            if not name.endswith('.dat') or name.startswith('dark') or name.startswith('flat') or 'moon' in name:
                continue
            else:
                stars.append(join(root, name))
        break
    if parent:
        num_star = 0
        parent.set_progress.emit('stars', len(stars), num_star)
    for star in stars:
        get_ps(star, diff=params['diff'], acf=params['acf'], save=params['save'], shape=params['shape'], output=params['output']['night'], rmbgr_on=params['rmbgr'])
        if parent:
            num_star += 1
            parent.set_progress.emit('stars', len(stars), num_star)