from numpy import *
from os import walk
def rebuild_set(params, parent = None, level = 0):
    nights = []
    for root, dirs, files in walk(params['input']['set']):
        for d in dirs:
            if d.startswith('2'):
                nights.append(d)
    for night in nights:
        pass

def rebuild_night(params, parent = None, level = 0):
    pass
    
def rebuild_star(params, parent = None, level = 0):
    pass
