 # -*- coding: utf-8 -*-
import random

def randperm(a):
    '''
    same as function randperm in matlab
    将一个list打乱顺序排列
    '''
    if(not a):
        return a
    b = []
    while(a.__len__()):
        r = random.choice(a)
        b.append(r)
        a.remove(r)
    return b
