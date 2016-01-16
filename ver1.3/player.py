 # -*- coding: utf-8 -*-

from wujiang import *
from ai import *
from show import *
from api import *
import random

class player(object):
    '''
    玩家
    '''
    def __init__(self,playername,PD,JINENG,PAI,mode,op3):
        '''
        先摸4张
        '''
        self.WJ=WUJIANG()
        self.record = op3 #record or not
        if op3 ==1:
            self.tobewritten=[]
        self.alive = 1
        self.round=0
        self.myround=0
        self.killed=0
        self.PAI=PAI
        self.PD=PD
        self.name = playername
        self.JINENG=JINENG
        if self.name in {'周泰','曹仁','孙权','张辽','黄盖','祝融','孟获','马超','黄忠','魏延','张飞','关羽','赵云','曹操','徐晃','夏侯惇','许褚','吕布','颜良文丑','庞德','典韦'}:
            self.hp_top = 4
        elif self.name in {'陆逊','大乔','小乔','周瑜','孙尚香','诸葛亮','黄月英','司马懿','甄姬','貂蝉','郭嘉'}:
            self.hp_top = 3
        if self.name =='周泰':
            self.buqu_pai=[]
        elif self.name=='曹仁':
            self.special_fanmian=0
        elif self.name=='许褚':
            self.U_skill = 1
        self.hp= self.hp_top
        self.shoupai = []
        self.panding = []
        self.weapon_pai=[]
        self.armor_pai=[]
        self.LE_pai=[]
        self.BING_pai=[] #2
        self.magic=JINENG.haveJINENG.get(self.name)#武将主动技能
        self.magiced=0 #已经使用技能如反间
        self.special = 0 #特殊状态 如许褚裸衣
        self.mode = mode # 0 for human, 1 for AI
        self.AI=AI(self)
        self.step=0
        for i in range(self.hp_top):      
            self.shoupai.append(self.PD.MOPAI())
        print self.name+'从牌堆摸了'+str(self.hp_top)+'张牌'
    def newround(self):
        self.myround=1
        self.round+=1
        self.step=0
        lived=1
        if self.name=='曹仁' and self.special_fanmian==1:
            self.special_fanmian=0
            self.myround=0
            return
        self.Kaiju()
        M,C = self.Panding()
        if M:
            self.Mopai()
        if C:
            lived = self.Chupai()
        if lived:
            self.QIPAI()
        self.myround=0
         
    def weapon(self):
        '''
        显示武器为文字
        '''
        if len(self.weapon_pai)>0:
            return self.PAI.PAI[self.weapon_pai[0]][1]
        else:
            return ''
    def armor(self):
        '''
        显示护甲为文字
        '''
        if len(self.armor_pai)>0:
            return self.PAI.PAI[self.armor_pai[0]][1]
        else:
            return ''
    def init_adv(self,adversary):
        '''
        定义对手，以及初始化，启动技能
        '''
        self.adv=adversary
        self.adv.adv=self
        print self.name+'的对手是'+self.adv.name
        if self.name=='关羽':
            self.PAI.moveSHUI(self,self.adv)
            print self.name+'释放虎威'
        elif self.name in {'马超','庞德'}:
            self.PAI.moveSHA(self,self.adv)
            print self.name+'出场杀'
        elif self.name in {'祝融','孟获'}:
            self.PAI.moveNANMAN(self,self.adv)
            print self.name+'释放蛮裔'



    def Kaiju(self):
        '''
        执行开局阶段
        '''
        if self.name=='甄姬':
            while 1:
                print '甄姬：仿佛兮若轻云之蔽月，飘飖兮若流风之回雪'
                temp = self.PD.MOPAI()
                if self.PAI.PAI[temp][0][0] in {'B','C'}:
                    self.shoupai.append(temp)
                    print '洛神得到：'+self.PAI.PAI[temp][1]+'  '+show_hua(self.PAI.PAI[temp][0])+self.PAI.PAI[temp][0][1]
                else:
                    print show_hua(self.PAI.PAI[temp][0])+self.PAI.PAI[temp][0][1]+'，  洛神失败'
                    break
        elif self.name=='诸葛亮':
            show(self,self.PAI,'选择任意手牌')
            print '诸葛亮: 知天易，逆天难'
            print '诸葛亮发动了观星,展示两张牌\n'
            X=[]
            X.append(self.PD.MOPAI())
            X.append(self.PD.MOPAI())
            print show_pai(self.PAI,X[0],'all')
            print show_pai(self.PAI,X[1],'all')
            print '选项: 1.不放 2.放第一张 3.放第二张 4.全放 5.交换位置'
            while 1:
                var = API(self, {''},'观星','请选择')
                if var.isdigit() and int(var) in {1,2,3,4,5}:
                    if var=='1':
                        self.PD.MP.insert(0,X[1])
                        self.PD.MP.insert(0,X[0])
                    elif var=='2':
                        self.PD.MP.append(X[0])
                        self.PD.MP.insert(0,X[1])
                    elif var=='3':
                        self.PD.MP.append(X[1])
                        self.PD.MP.insert(0,X[0])
                    elif var=='4':
                        self.PD.MP.append(X[0])
                        self.PD.MP.append(X[1])
                    elif var=='5':
                        self.PD.MP.insert(0,X[0])
                        self.PD.MP.insert(0,X[1])
                    break       
        
    def Panding(self):
        '''
        执行判定阶段
        '''
        M=1
        C=1
        if len(self.BING_pai)>0:
            print '兵粮寸断'
            if int(self.PAI.askforWuxie(self,'BING')):
                pass
            elif int(self.PAI.askforWuxie(self.adv,'BING')):
                pass
            else:
                panding_indx = self.PD.MOPAI()
                self.PD.ZM.append(panding_indx)
                print self.name + '的兵粮寸断判定为' +show_hua(self.PAI.PAI[panding_indx][0]) +' '+self.PAI.PAI[panding_indx][1]
                changed, panding_indx = self.JINENG.P(self,self.adv,panding_indx)        #检查场上可用的判定技能
                if changed:
                    print self.name + '的兵粮寸断判定为' +show_hua(self.PAI.PAI[panding_indx][0]) +' '+self.PAI.PAI[panding_indx][1]
                if self.PAI.PAI[panding_indx][0][0][0] == 'C':  #是草花
                    print '判定失败'
                else:
                    M=0
                    print '判定成功，跳过摸牌阶段'
            temp = self.BING_pai.pop(0)
            if self.name=='郭嘉':
                self.shoupai.append(temp)
            else:
                self.PD.QP.append(temp)
            self.PD.QP+=self.PD.ZM
            self.PD.ZM=[]
        if len(self.LE_pai)>0:
            print '乐不思蜀'
            if int(self.PAI.askforWuxie(self,'LE')):
                pass
            elif int(self.PAI.askforWuxie(self.adv,'LE')):
                pass
            else:
                panding_indx = self.PD.MOPAI()
                self.PD.ZM.append(panding_indx)
                print self.name + '的乐不思蜀判定为' +show_hua(self.PAI.PAI[panding_indx][0]) +' '+self.PAI.PAI[panding_indx][1]
                if self.PAI.PAI[panding_indx][0][0][0] == 'R' or (self.name=='小乔' and self.PAI.PAI[panding_indx][0][0][0] in {'R','B'}):  #是红桃
                    print '判定失败'
                else:
                    C=0
                    print '判定成功，跳过出牌阶段'
            temp = self.LE_pai.pop(0)
            if self.name=='郭嘉':
                self.shoupai.append(temp)
            else:
                self.PD.QP.append(temp)
            self.PD.QP+=self.PD.ZM
            self.PD.ZM=[]
        return M , C
            
    def Mopai(self):
        '''
        执行摸牌阶段
        '''
        if self.name =='颜良文丑':
            var = API(self, ['','1'],'cast', '是否发动双雄')
            if len(var)>0:
                print '颜良文丑: 吾乃河北上将颜良/文丑是也'
                self.shoupai.append(self.PD.MOPAI())
                self.special=1
                return
        elif self.name =='张辽':
            if len(self.shoupai)<len(self.adv.shoupai):
                self.shoupai.append(self.adv.shoupai.pop(random.randint(0,len(self.adv.shoupai)-1)))
                self.shoupai.append(self.PD.MOPAI())
                return
        elif self.name =='孟获':
            if self.hp<self.hp_top:
                var = API(self, ['','1'],'cast','是否发动再起')
                if len(var)>0:
                    print '孟获: 起！'
                    for i in range(self.hp_top-self.hp):
                        temp = self.PD.MOPAI()
                        print '孟获再起摸到了'+show_pai(self.PAI,temp,'all')
                        if self.PAI.PAI[temp][0][0] == 'R':
                            self.PD.QP.append(temp)
                            self.hp+=1
                            print '孟获回复1点体力'
                        else:
                            self.shoupai.append(temp)
                    return
        elif self.name =='许褚':
            var = API(self, ['','1'],'cast','是否发动裸衣')
            if len(var)>0:
                print '许褚: 脱！'
                self.shoupai.append(self.PD.MOPAI())
                self.special = 1
                return
        elif self.name=='周瑜':
            self.shoupai.append(self.PD.MOPAI())
            print self.name+': 哈哈哈'                 
        else:
            print self.name+'摸牌成功'
        if self.round!=1:
            self.shoupai.append(self.PD.MOPAI())
        self.shoupai.append(self.PD.MOPAI())
    def information(self):
        temp1 = self.WJ.index(self.name)
        v = [[]]*10
        v[0] = [0]*len(self.WJ)
        v[0][temp1]=1
        temp2 = self.WJ.index(self.adv.name)
        v[1] = [0]*len(self.WJ)
        v[1][temp2]=1
        v[2] = [self.myround,self.hp,self.adv.hp,len(self.shoupai),len(self.adv.shoupai),self.killed,self.magiced]
        v[3]=[0]*len(self.PAI.ZILEI)
        v[4]=[0]*len(self.PAI.ZILEI)
        for i in self.shoupai:
            v[3][self.PAI.ZILEI.index(self.PAI.PAI[i][1])]+=1
        for i in self.adv.shoupai:
            v[4][self.PAI.ZILEI.index(self.PAI.PAI[i][1])]+=1
        v[5] = [len(self.LE_pai),len(self.BING_pai),len(self.adv.LE_pai),len(self.adv.BING_pai)]
        v[6] = [0]*len(self.PAI.W_ZILEI)
        v[7] = [0]*len(self.PAI.Q_ZILEI)
        v[8] = [0]*len(self.PAI.W_ZILEI)
        v[9] = [0]*len(self.PAI.Q_ZILEI)
        if len(self.weapon_pai):
            v[6][self.PAI.W_ZILEI.index(self.PAI.PAI[self.weapon_pai[0]][1])]+=1        
        if len(self.armor_pai):
            v[7][self.PAI.Q_ZILEI.index(self.PAI.PAI[self.armor_pai[0]][1])]+=1
        if len(self.adv.weapon_pai):
            v[8][self.PAI.W_ZILEI.index(self.PAI.PAI[self.adv.weapon_pai[0]][1])]+=1
        print v[9]
        if len(self.adv.armor_pai):
            v[9][self.PAI.Q_ZILEI.index(self.PAI.PAI[self.adv.armor_pai[0]][1])]+=1        
        V=[]
        for i in v:
            V+=i
        return V 
        
    def Chupai(self):
        '''
        执行出牌阶段
        '''
        if self.record ==1:
            self.tobewritten.append(self.information())
        lived =1
        self.killed = 0
        self.magiced= 0
        while lived:
            available = show(self,self.PAI,'出牌阶段')
            #var = raw_input("你要出哪一张: ")#比如1
            var = API(self,available,'CHUPAI','你要出哪一张: ')
            if var=='':
                break
            elif var in {'w','e','r'}:#武器或技能
                if var=='w':
                    move='使用丈八蛇矛'
                    validmove, lived = self.PAI.move(move,self,self.adv)#move('使用丈八蛇矛',O,T)
                if var=='e':
                    validmove,lived = self.JINENG.C(self,self.adv)
                    if validmove ==1 and self.name not in {'黄盖','赵云','关羽','甘宁'}:
                        self.magiced=1
            elif var.isdigit() and int(var) in available:
                card_indx = self.shoupai[int(var)-1]# 比如0 /48
                self.PAI.pop_shoupai(self,(int(var)-1))                    #从手中移除
                self.PD.ZM.append(card_indx)                         #放到桌面
                move = self.PAI.PAI[card_indx][1]#'决斗'
                print colored(move,'green')#print 决斗
                validmove, lived = self.PAI.move(move,self,self.adv)#move('决斗',O,T)
                if not validmove:
                    print '无效的出牌'
                    self.shoupai.append(self.PD.ZM.pop(-1))
                else:
                    self.PD.QP+=self.PD.ZM
                    self.PD.ZM=[]#桌面入弃牌堆
            else:
                print '错误的选项'
            self.step+=1
        return lived
    def QIPAI(self):
        '''
        执行弃牌阶段
        '''
        num1= len(self.shoupai)-self.hp            
        while num1>0: #弃牌循环
            available = show(self,self.PAI,'选择任意手牌')
            print '你还需要弃'+str(num1)+'张牌'
            var = API(self, available,'QIPAI', "你放弃哪一张: ")#比如1
            if var=='':
                continue
            if var.isdigit() and int(var) in available:
                card_indx = self.shoupai.pop(int(var)-1)# 比如0 /48
                #从手中移除
                if self.adv.name=='孙尚香' and self.PAI.LEIXING[self.PAI.PAI[card_indx][1]] in {'wuqi','fangju'}:
                    self.adv.shoupai.append(card_indx)
                else:
                    self.PD.QP.append(card_indx)
                self.PD.QP+=self.PD.ZM           #桌面入弃牌堆
                self.PD.ZM=[]
                num1-=1
                show(self,self.PAI,'选择任意手牌')
        if self.name =='貂蝉':
            self.shoupai.append(self.PD.MOPAI())
            print '貂蝉：失礼了'
            print '貂蝉获得了'+self.PAI.PAI[self.shoupai[-1]][1]
        elif self.name=='曹仁':
            var = API(self, ['','1'],'cast', '是否发动据守?')
            if var=='':
                pass
            else:
                for i in range(3):
                    self.shoupai.append(self.PD.MOPAI())
                self.special_fanmian = 1
                print '曹仁: 我先休息一会'

