from numpy import *
from os import walk
from os.path import isdir, join

def rebuild_set(params, parent = None, level = 0):
    nights = []
    for root, dirs, files in walk(params['input']['set']):
        for d in dirs:
            if d.startswith('2'):
                nights.append(d)
        break
    for night in nights:
        params['input']['night'] = join(params['input']['set'], night)
        params['output']['night'] = join(params['output']['set'], night)
        print('\t'*level + params['input']['night'])
        rebuild_night(params, parent, level+1)

def rebuild_night(params, parent = None, level = 0):
    stars = []
    for root, dirs, files in walk(params['input']['night']):
        for d in dirs:
            stars.append(d)
        break
    for star in stars:
        params['input']['star'] = join(params['input']['night'], star)
        params['output']['star'] = join(params['output']['night'], star)
        print('\t'*level + params['input']['star'])
        rebuild_star(params, parent, level+1)

def rebuild_star(params, parent = None, level = 0):
    serie_type = check_serie_type(params['input']['star'])
    if serie_type:
        print(serie_type)
    else:
        return 0

def check_serie_type(path_to_dir):
    files_num = 0
    for root, dirs, files in walk(path_to_dir):
        files_num += len(files)
    if files_num == 0:
        print(path_to_dir+' is empty folder.')
        return 0
    elif isdir(join(path_to_dir, 'spool')):
        return 'dat'
    elif files_num == 1:
        return 'big_tiff'
    else:
        print(path_to_dir+' have unknown format')