 # -*- coding: utf-8 -*-
            
from show import *

class AI(object):
    '''
    初级AI
    '''
    def __init__(self,player):
        self.player=player
        self.PAI =player.PAI
        self.PD = player.PD
        self.JINENG =player.JINENG
    def app_rank_CHUPAI(self,available,option):
        pai_indx = available[option]
        if type(option) is int:
            txt = self.PAI.PAI[pai_indx][1]
            lx = self.PAI.LEIXING[txt]
            if lx=='yanchi':
                R=10
            elif lx=='jinnang':
                R=20
                if txt=='无中生有':
                    R+=0
                elif txt=='顺手牵羊':
                    R+=2
                elif txt=='过河拆桥':
                    R+=3
                else:
                    R+=4
            elif lx=='wuqi':
                R=30
            elif lx=='jiben':
                if txt=='杀':
                    R=40
                    if self.PAI.PAI[pai_indx][0][0] in{'R','F'}:
                        R=41
                    elif self.player.adv.armor()=='仁王盾' and self.player.weapon()!='青钢剑':
                        R=101
                elif txt=='闪':
                    R=80
                elif txt=='桃':
                    R=90
            elif lx=='fangju':
                R=60
        else:
            if option=='w':
                R=70
            elif option=='e':
                R=35
            elif option=='q':
                R=100
        return R

    def app_rank_QIPAI(self,available,option):
        pai_indx = available[option]
        if type(option) is int:
            txt = self.PAI.PAI[pai_indx][1]
            lx = self.PAI.LEIXING[txt]
            if lx=='yanchi':
                R=30
            elif lx=='jinnang':
                R=40
                if txt=='顺手牵羊':
                    R+=1
                elif txt=='过河拆桥':
                    R+=2
                else:
                    R+=3
            elif lx=='wuqi':
                R=10
            elif lx=='jiben':
                if txt=='杀':
                    R=50
                elif txt=='闪':
                    R=80
                elif txt=='桃':
                    R=90
            elif lx=='fangju':
                R=60
        else:
            if option=='w':
                R=35
            elif option =='q':
                R=70
            elif option=='e':
                R=60
                if self.player.name=='周瑜':
                    if len(self.player.shoupai)<=3:
                        R=101
                    else:
                        for i in self.player.shoupai:
                            if self.PAI.PAI[i][1]=='桃':
                                R=101
                                break                    
        return R
    def new(self):
        vPD = PD()#新建牌堆
        vPD.QP = copy.deepcopy(self.PD.QP)#拷贝弃牌堆
        vPD.QP+= self.PD.ZM
        for i in vPD.QP:
            vPD.MP.remove(i)
        for i in vPD.ZM:
            vPD.MP.remove(i)
        for i in self.player.shoupai:
            vPD.MP.remove(i)
        for i in self.player.weapon_pai:
            vPD.MP.remove(i)
        for i in self.player.armor_pai:
            vPD.MP.remove(i)
        for i in self.player.adv.weapon_pai:
            vPD.MP.remove(i)
        for i in self.player.adv.armor_pai:
            vPD.MP.remove(i) #移除可见牌
        vPD.MP = randperm(vPD.MP) #打乱不可见牌
        vP1 = player(self.player.name, vPD, self.JINENG, self.PAI, 1)
        vP2 = player(self.player.adv.name, vPD, self.JINENG, self.PAI, 1)
        for i in range(len(self.player.adv.shoupai)):
            vP2.shoupai.append(vPD.MOPAI())
        vP1.shoupai = copy.deepcopy(self.player.shoupai)
        vP1.weapon_pai = copy.deepcopy(self.player.weapon_pai)
        vP1.armor_pai = copy.deepcopy(self.player.armor_pai)
        vP2.weapon_pai = copy.deepcopy(self.player.adv.weapon_pai)
        vP2.armor_pai = copy.deepcopy(self.player.adv.armor_pai)
        vP1.adv=vP2
        vP2.adv=vP1
            
    def askforAI(self,available,state,*args,**kwargs):
        '''
        state in {'CHUPAI','askforSha','askforShan'}
        available in {'1','2','3'...,'e','w','q'}
        mode in {1,2}
        '''
        out=''
        D={}
        if len(available)>0:
            if state=='CHUPAI' or state=='askforSha':
                for i in available:
                    D[i]=self.app_rank_CHUPAI(available,i)
                    if D[i]>=100:
                        D.pop(i)
                if len(D)>0:
                    out = min(D,key=D.get) # get the key with the least value
                    if out=='w' and len(self.player.weapon_pai)>0:
                        out=''
            elif state=='QIPAI':
                for i in available:
                    D[i]=self.app_rank_QIPAI(available,i)                        
                out = min(D,key=D.get)
            elif state=='askforWuxie':
                if self.player.myround==1:
                    out=''
                    if len(self.player.LE_pai)>0 and len(self.player.shoupai)>=self.player.hp-1:
                        out=available.keys()[0]
                    if len(self.player.LE_pai)>0:
                        out=available.keys()[0]
                else:
                    out=available.keys()[0]
                    if len(args)>0:
                        ENV = args[0]
                        if ENV == 'moveJUEDOU':
                            if len(self.player.shoupai)>len(self.adv.shoupai):
                                out=''
                            else:
                                out=available.keys()[0]
                        elif ENV == 'moveNANMAN':
                            out=available.keys()[0]
                            for i in self.player.shoupai:
                                if show_pai(self.PAI,i,'pai')=='杀':
                                    out=''
                                    break
            elif state=='cast':
                out='1'
                if len(args)>0:
                    ENV = args[0]
                    if ENV=='moveSHUI' and len(self.player.armor_pai)>0 and self.player.hp>=2:
                        out='0'
                if self.player.name=='孟获' and self.player.hp_top-self.player.hp<=1:
                    out='0'
                elif self.player.name=='典韦' and len(show(self.player,self.PAI,'强袭'))==0 and self.player.hp<self.player.adv.hp:
                    out='0'
                elif self.player.name=='许褚':
                    if len(self.player.shoupai)>=len(self.player.adv.shoupai):
                        out='0'
                        for i in self.player.shoupai:
                            if show_pai(self.PAI,i,'pai')=='杀':
                                out='1'
                                break                    
                    else:
                        out='0'
                elif self.player.name=='夏侯惇' and self.player.adv.name=='小乔' and self.player.myround ==1:
                    out='0'
            elif state=='askforShan':
                for i in available:
                    D[i]=self.app_rank_QIPAI(available,i)
                out = max(D,key=D.get)
            elif state=='app_NAPAI':
                for i in available:
                    D[i]=self.app_rank_QIPAI(available,i)
                out = max(D,key=D.get) # get the key with the least value
            elif state=='moveCHAI':
                out='1'
                if len(self.player.adv.armor_pai)>0:
                    out = '1'
                elif len(self.player.adv.shoupai)>0:
                    out = '2'
            elif state=='app_QIPAI':
                for i in available:
                    D[i]=self.app_rank_QIPAI(available,i)
                out = max(D,key=D.get) # get the key with the least value
            elif state=='useHANBING':
                if self.player.adv.name in {'郭嘉','夏侯惇'} and len(self.player.adv.shoupai)>=2:
                    out='1'
                else:
                    out='0'
            elif state=='花色':
                out='4'
                print out
            elif state=='askforBlack':
                for i in available:
                    D[i]=self.app_rank_QIPAI(available,i)
                out = min(D,key=D.get)
            elif state=='天命':
                out=''
            elif state=='askforTAO':
                target = args[0]
                if target=='self' and len(available)>0:
                    out = available.keys()[0]
                else:
                    out=''
            elif state=='国色':
                for i in available:
                    D[i]=self.app_rank_QIPAI(available,i)
                out = min(D,key=D.get) # get the key with the least value
            elif state=='观星':
                out='1'
            elif state=='拼点':
                for i in available:
                    D[i]=self.app_rank_QIPAI(available,i)
                out = min(D,key=D.get)
            elif state=='强袭':
                if len(available)>0:
                    for i in available:
                        D[i]=self.app_rank_QIPAI(available,i)
                    out = min(D,key=D.get)
        if self.player.step>len(self.player.shoupai)+5 and state=='CHUPAI':
            out=''
        print out
        return str(out)
            
