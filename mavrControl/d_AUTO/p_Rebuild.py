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
                    append_o(join(params['nights']['outputs'][n], d+'.dat'))
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
                append_o(join(params['output']['night'], d+'.dat'))
            break

    elif params['type'] == 'star':
        params['stars'] = {}
        params['stars']['inputs'] = [params['input']['star'],]
        params['stars']['outputs'] = [params['output']['star']+'.dat',]

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
    elif files_num > 500 and files[-1].endswith('.tif'):
        return 'serie_tif'
    else:
        print(path_to_dir+' have unknown format')