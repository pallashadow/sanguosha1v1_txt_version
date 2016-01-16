 # -*- coding: utf-8 -*-

from show import *
from api import *
import random

class JINENG(object):
    '''
    定义武将主动技能
    '''
    def __init__(self,PAI,PD):
        self.PAI=PAI
        self.PD=PD
        self.K_char={'甄姬'}
        self.P_char_all={'司马懿','张角'}
        self.P_char = {'司马懿','张角'}
        self.haveJINENG = {'大乔':'国色','徐晃':'断粮','周瑜':'反间','黄盖':'苦肉','孙权':'制衡','典韦':'强袭','许褚':''}
    def C(self,O,T):
        if O.name=='黄盖':
            O.hp-=1
            self.PAI.hp_check(O)
            O.shoupai.append(self.PD.MOPAI())
            O.shoupai.append(self.PD.MOPAI())
            valid=1
        elif O.name=='典韦':
            available = show(O,self.PAI,'强袭')
            var = API(O, available,'强袭','强袭弃牌')
            while 1:
                if var=='':
                    O.hp-=1
                    self.PAI.hp_check(O)
                    self.PAI.app_damage(O,T,'')
                    self.PAI.hp_check(T)
                    break
                elif var=='w' and len(O.weapon_pai)>0:
                    self.PD.QP.append(O.weapon_pai.pop(0))
                    self.PAI.app_damage(O,T,'')
                    self.PAI.hp_check(T)
                    break
                elif var.isdigit() and int(var) in available:
                    self.PD.QP.append(O.shoupai.pop(int(var)))
                    self.PAI.app_damage(O,T,'')
                    self.PAI.hp_check(T)
                    break            
            valid=1
        elif O.name=='关羽':
            available = show(O,PAI,'求红')
            if len(O.weapon_pai)>0 and self.PAI.PAI[O.weapon_pai[0]][0] in {'R','F'}:
                print 'w   武器'
            var = API(O, available,'askforRed', '选张红')
            while 1:
                if var=='':
                    valid=0
                    break
                elif var=='w':
                    if self.PAI.PAI[O.weapon_pai[0]][0] in {'R','F'}:
                        self.PD.ZM.append(O.weapon_pai.pop(0))
                        return PAI.move(move,self,self.adv)
                    else:
                        print O.name+'无效的出牌'
                elif var.isdigit() and int(var) in available:
                    self.PD.ZM.append(O.shoupai.pop(int(var)-1))
                    return PAI.move(move,self,self.adv)
                else:
                    print O.name+'无效的出牌'
            valid=1
            self.PAI.moveSha(O,T)
        elif O.name=='甘宁':
            available = show(O,PAI,'求黑')
            if len(O.weapon_pai)>0 and self.PAI.PAI[O.weapon_pai[0]][0] in {'B','C'}:
                print 'w   武器'
            if len(O.armor_pai)>0 and self.PAI.PAI[O.armor_pai[0]][0] in {'B','C'}:
                print 'q   防具'
            var = API(O, available,'askforBlack', '选张黑')
            while 1:
                if var=='':
                    valid=0
                    break
                elif var=='w':
                    if self.PAI.PAI[O.weapon_pai[0]][0] in {'B','C'}:
                        self.PD.ZM.append(O.weapon_pai.pop(0))
                        return PAI.move(move,self,self.adv)#move('决斗',O,T)# valid, lived
                    else:
                        print '无效的出牌'
                elif var=='q':
                    if self.PAI.PAI[O.armor_pai[0]][0] in {'B','C'}:
                        self.PD.ZM.append(O.armor_pai.pop(0))
                        return PAI.move(move,self,self.adv)#move('决斗',O,T)# valid, lived
                    else:
                        print '无效的出牌'            
                elif var.isdigit() and int(var) in available:
                    self.PD.ZM.append(O.shoupai.pop(int(var)-1))
                    return PAI.move(move,self,self.adv)#move('决斗',O,T)# valid, lived
                else:
                    print '无效的出牌'

        elif O.name=='孙权':
            l = len(O.shoupai)+len(O.weapon_pai)+len(O.armor_pai)
            mopaitime=0
            if l>0:
                while l>=1 and mopaitime==0:
                    available = show(O,self.PAI,'选择所有牌')
                    var1 = API(O, available,'QIPAI', '选择制衡牌1')
                    if var1=='':
                        return 0,1
                    elif var1.isdigit() and int(var1) in available:
                        temp1 = O.shoupai.pop(int(var1)-1)
                        mopaitime+=1
                        print var1
                        break
                    elif var1=='w' and len(O.weapon_pai)>0:
                        temp1 = O.weapon_pai.pop(0)
                        mopaitime+=1
                        break
                    elif var1=='q' and len(O.armor_pai)>0:
                        temp1 = O.armor_pai.pop(0)
                        mopaitime+=1
                        break
                while l>=2 and mopaitime==1:
                    available = show(O,self.PAI,'选择所有牌')
                    var2 = API(O, available,'QIPAI','选择制衡牌2')
                    if var2=='':
                        break
                    elif var2.isdigit() and int(var2) in available:
                        temp2 = O.shoupai.pop(int(var2)-1)
                        O.shoupai.append(self.PD.MOPAI())
                        break
                    elif var2=='w' and len(O.weapon_pai)>0:
                        temp2 = O.weapon_pai.pop(0)
                        O.shoupai.append(self.PD.MOPAI())
                        break
                    elif var2=='q' and len(O.armor_pai)>0:
                        temp2 = O.armor_pai.pop(0)
                        O.shoupai.append(self.PD.MOPAI())
                        break
                try:
                    if O.adv.name=='孙尚香' and self.PAI.LEIXING[self.PAI.PAI[temp1][1]] in {'wuqi','fangju'}:
                            self.adv.shoupai.append(temp1)
                    else:
                        self.PD.QP.append(temp1)
                except Exception,e:
                    print str(e)
                try:
                    if O.adv.name=='孙尚香' and self.PAI.LEIXING[self.PAI.PAI[temp2][1]] in {'wuqi','fangju'}:
                        self.adv.shoupai.append(temp2)
                    else:
                        self.PD.QP.append(temp2)
                except Exception,e:
                    print str(e)
                if mopaitime==1:
                    O.shoupai.append(self.PD.MOPAI())
                valid=1
            else:
                valid=0
                
        elif O.name=='周瑜' and len(O.shoupai)>0:
            print O.name+'对'+T.name+'使用反间'
            print '1 黑桃\n2 红桃\n3 草花\n4 方片'
            var = API(T, {''},'花色', '请选择花色')
            L = ['B','R','C','F']
            temp = O.shoupai.pop(random.randint(0,len(O.shoupai)-1))#随机弃一张
            print T.name+'抽到了'+show_pai(self.PAI,temp,'all')
            T.shoupai.append(temp)
            while 1:
                if var.isdigit() and int(var) in [1,2,3,4]:
                    if L[int(var)-1]!=self.PAI.PAI[temp][0][0]:#抽错了
                        self.PAI.app_damage(O,T,'')
                    break
            valid=1
        elif O.name=='大乔':
            available = show(O,self.PAI,'选择方片')
            var = API(O, available,'国色', '选择方片当作乐不思蜀使用')
            while 1:
                if var.isdigit():
                    if int(var) in available:
                        if len(T.LE_pai)==0:
                            T.LE_pai.append(O.shoupai.pop(int(var)-1))
                            valid=1
                            break
                        else:
                            '已经有乐'
                            valid=0
                            break
                    elif int(var) not in available:
                        continue
                else:
                        valid=0
                        break
        elif O.name=='徐晃':
            available = show(O,self.PAI,'断粮')
            var = API(O, available,'askforBlack', '选择黑色基本牌或黑色装备当作兵粮寸断使用')
            if len(T.BING_pai)>0:
                return 0,1
            while 1:
                if var.isdigit() and int(var) in available:
                    T.BING_pai.append(O.shoupai.pop(int(var)-1))
                    valid =1
                    break
                elif var in {'q','w'}:#装备，武器
                    if var=='q':
                        T.BING_pai.append(O.armor_pai.pop(0))
                        valid=1
                        break
                    elif var=='w':
                        T.BING_pai.append(O.weapon_pai.pop(0))
                        valid= 1
                        break
                else:
                    valid= 0
                    break
        elif O.name=='许褚':
            O.U_skill=0
            if self.PAI.app_PINDIAN(O,T):
                self.PD.QP+=self.PD.ZM
                self.PD.ZM=[]
                self.PAI.moveJUEDOU(O,T)
                valid=1
            else:
                self.PD.QP+=self.PD.ZM
                self.PD.ZM=[]
                self.PAI.moveJUEDOU(T,O)
                valid=1
        lived = O.hp>0 and T.hp>0
        return valid, lived
                
                
    def P(self,O,T,panding_indx):
        '''
        判定技能
        '''
        if O.name in self.P_char:
            if O.name == '司马懿':
                available = show(O,self.PAI,'选择任意手牌')
                while 1:
                    var = API(O, available,'天命', "司马懿，请出一张判定牌")
                    if var =='':
                        return 0,panding_indx #放弃，没有改
                    if int(var) not in available:
                        continue
                    if int(var) in available:
                        changed = 1 #改了
                        break
                card_indx = O.shoupai[int(var)-1]# 比如0 /48
                O.shoupai.pop(int(var)-1)                    #从手中移除
                self.PD.QP.append(card_indx)                         #放到
                print O.name+': 天命'
                print '司马懿将判定牌"'+panding_indx+'"替换成了'+card_indx
                return changed, card_indx

            elif O.name == '张角':
                available = show(O,self.PAI,'出示黑牌')
                while 1:
                    var = API(O, available,'鬼道', "张角，请出一张判定牌")
                    if var =='':
                        return 0,panding_indx#放弃，没有改
                    if int(var) not in available:
                        continue
                    if int(var) in available:
                        changed = 1 #改了
                        break
                card_indx = O.shoupai[int(var)-1]# 比如0 /48
                self.PD.ZM.append(O.shoupai.pop(int(var)-1))       #从手中移除放到桌面
                O.shoupai.append(self.PD.ZM.pop(-2))        #获得判定牌
                
                self.PD.ZM.append(card_indx)                         #放到桌面
                print O.name+': 苍天已死，黄天当立'
                print '张角将判定牌"'+self.PAI.PAI[panding_indx][1]+'"替换成了'+self.PAI.PAI[card_indx][1]
                return changed, card_indx
        else: #没有司马和张角
            return 0, panding_indx
