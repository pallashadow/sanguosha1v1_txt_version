 # -*- coding: utf-8 -*-

from paidui import *
from jineng import *
from player import *


def startGame(wj1,wj2,op1,op2,op3):
    paidui = PD()
    PAI = PAI_def(paidui)
    jineng = JINENG(PAI,paidui)
    P1 = player(wj1,paidui,jineng,PAI,op1,op3)
    P2 = player(wj2,paidui,jineng,PAI,op2,op3)
    P1.init_adv(P2)
    while 1:
        if P1.alive and P2.alive:
            P1.newround()
        else:
            break
        if P1.alive and P2.alive:
            P2.newround()
        else:
            break

    if P1.alive:
        winner = P1.name
        out=1
    else:
        winner = P2.name
        out=0
    X=[]
    Y=[]
    if op3:
        p1target = [out]*len(P1.tobewritten)
        p2target = [int(not out)]*len(P2.tobewritten)
##    for i in P1.tobewritten:
##        i.append(out)
##    for i in P2.tobewritten:
##        i.append(int(not out))
        X = P1.tobewritten+P2.tobewritten
        Y = p1target+p2target
    #f1 = open("save.p",'w')
    #cPickle.dump(L, f1)
        
    #f1.close()
    print '游戏结束\n获胜的玩家是'+winner
    return out,X,Y
