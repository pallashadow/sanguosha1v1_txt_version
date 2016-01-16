 # -*- coding: utf-8 -*-
import codecs
import random
import copy
import pickle

from round1 import *



def analysis(M,WJ,N):
    D={}
    v1=[]
    v2=[]
    v3=[]
    v4=[]
    v5=[]
    for i in range(len(WJ)):
        v1.append(0)#先手i胜利M[i][j]==1
        v2.append((len(WJ)-1)*N)
        v3.append(0)
        v4.append(0)
        v5.append(0)
        for j in range(len(WJ)):
            v2[i]-=M[j][i] #后手
        v1[i]+=sum(M[i]) #先手
        v3[i]=float(v1[i]+v2[i])/len(WJ)/N/2 # 全战绩
        v4[i]= float(v1[i])/len(WJ) #先手胜率
        v5[i]= float(v2[i])/len(WJ) #后手胜率
        print WJ[i]+ '  全   '+"%.2f" % v3[i]
        print WJ[i]+ '  先   '+"%.2f" % v4[i] 
        print WJ[i]+ '  后   '+"%.2f" % v5[i]
    return (v1,v2,v3,v4,v5)

def script1(WJ,N):
    '''
    全武将AI互相PK N次
    '''
    M=[]
    XX=[]
    YY=[]
    #f1 = open("save.p",'r')
    #(XX,YY)=pickle.load(f1)
    #f1.close()
    for i in range(len(WJ)):
        wj1=WJ[i]
        M.append([])
        for j in range(len(WJ)):
            wj2=WJ[j]
            M[i].append(0)
            if wj1==wj2:
                continue
            for e in range(N):
                score,X,Y = startGame(wj1,wj2,1,1,1)
                M[i][j]+= score
                XX+=X
                YY+=Y
    #f1 = open("save.p",'w')
    #pickle.dump((XX,YY), f1)        
    #f1.close()    
    V= analysis(M,WJ,N)
    return M,V

def script2(WJ):
    '''
    单武将AI随机PK
    '''
    wj1=WJ[random.randint(0,len(WJ)-1)]
    wj2=WJ[random.randint(0,len(WJ)-1)]
    startGame(wj1,wj2,1,1,1)
def script3(WJ):
    '''
    单武将AI对全武将AI，逐一PK
    '''
    score=0
    beaten=[]
    #for i in range(len(WJ)):
    for i in range(len(WJ)):
        wj1='周泰'
        wj2='徐晃'
        if startGame(wj1,wj2,1,0,0)[0]:
            score+=1
            beaten.append(wj1+':'+wj2)
        else:
            beaten.append(wj2+':'+wj1)
    print score
    for i in beaten:
        print i
   
def script4(WJ):
    '''
    人机对战一局
    '''
    wj1=WJ[random.randint(0,len(WJ)-1)]
    wj2=WJ[random.randint(0,len(WJ)-1)]
    startGame(wj1,wj2,1,0,1)
