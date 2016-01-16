 # -*- coding: utf-8 -*-
from randperm import *
from show import *
from api import *


class PD(object):
    '''
    摸牌堆和弃牌堆
    '''
    def __init__(self):
        self.MP = randperm(range(52))#摸牌堆
        self.QP = []#弃牌堆
        self.ZM = []#桌面
    def MOPAI(self):
        if len(self.MP)==0:
            self.MP+=self.QP
            self.QP=[]
        pai_indx = self.MP.pop(0)
        return pai_indx


    
class PAI_def(object):
    '''
    定义48张pai的花色，内容，类型
    以及各种出牌
    '''
    def __init__(self,PD):
        '''
        定义48张pai的花色，内容，类型
        '''
        self.PD=PD
        temp1=['1','2','3','4','5','6','7','8','9','10','J','Q','K']
        temp2=(['决斗','八卦阵','过河拆桥','顺手牵羊','杀','青钢剑','杀','杀','寒冰剑','杀','顺手牵羊','丈八蛇矛','南蛮入侵','万箭齐发','闪','桃','桃','闪','乐不思蜀','无中生有','无中生有','桃','杀','杀','过河拆桥','无懈可击','决斗','仁王盾','过河拆桥','杀','杀','杀','水淹七军','杀','杀','杀','杀','兵粮寸断','无懈可击','诸葛连弩','闪','闪','顺手牵羊','贯石斧','杀','闪','闪','杀','闪','闪','桃','杀'])
        temp3 = []
        n=0
        for i in ['B','R','C','F']:
            for j in temp1:
                temp3.append([i+j,temp2[n]])
                n+=1
        self.ZILEI = list(set(temp2))
        self.PAI = temp3
        self.LEIXING = {'决斗':'jinnang','水淹七军':'jinnang','过河拆桥':'jinnang','顺手牵羊':'jinnang','南蛮入侵':'jinnang','万箭齐发':'jinnang','无中生有':'jinnang','无懈可击':'jinnang','乐不思蜀':'yanchi','兵粮寸断':'yanchi','八卦阵':'fangju','诸葛连弩':'wuqi','青钢剑':'wuqi','丈八蛇矛':'wuqi','贯石斧':'wuqi','寒冰剑':'wuqi','仁王盾':'fangju','杀':'jiben','闪':'jiben','桃':'jiben'}
        self.NE1 = {'闪','无懈可击'}
        self.W_ZILEI = ['诸葛连弩','青钢剑','丈八蛇矛','贯石斧','寒冰剑']
        self.Q_ZILEI = ['仁王盾','八卦阵']
        print self.LEIXING.keys()

    def hp_check(self,O):
        '''
        检查是否有处于濒死状态的人
        并求桃
        '''          
        if O.hp<=0:
            O.hp=0
            if O.name=='周泰':
                O.buqu_pai.append(self.PD.MOPAI())
                temp1=[]
                for i in O.buqu_pai:
                    temp1.append(self.PAI[i][0][1])
                print temp1
                if len(set(temp1))<len(temp1):
                    O.alive = 0
                    return 0
                else:
                    O.alive =1
                    return 1                
            elif self.askforTAO(O,'self'):
                O.hp+=1
                return 1
            elif self.askforTAO(O.adv,'adv'):
                lived =1
                return 1
            else:
                O.alive = 0
                return 0
        else:
            return 1

    def pop_shoupai(self,O,indx):
        '''
        可能包含陆逊的弃手牌行为经过此函数
        '''
        out = O.shoupai.pop(indx)
        if O.name=='陆逊' and len(O.shoupai)==0:
            print '陆逊: 牌不是万能的，但是没牌是万万不能的'
            O.shoupai.append(self.PD.MOPAI())
        return out
                
    def move(self,movename,O,T):
        '''
        回合内出牌行为经过此函数
        '''
        isvalidmove =1
        if O.name=='陆逊' and len(O.shoupai)==0:
            print '陆逊: 牌不是万能的，但是没牌是万万不能的'
            O.shoupai.append(self.PD.MOPAI())
        if movename=='杀':
            isvalidmove = self.moveSHA(O,T)
        elif movename=='桃':
            self.moveTAO(O)
        elif movename=='决斗':
            if int(self.askforWuxie(O,'moveJUEDOU')):
                return 1,1
            elif int(self.askforWuxie(T,'moveJUEDOU')):
                return 1,1
            else:
                self.moveJUEDOU(O,T)
        elif movename=='顺手牵羊':
            isvalidmove = self.moveSHUN(O,T)
        elif movename== '过河拆桥':
            isvalidmove = self.moveCHAI(O,T)
        elif movename=='万箭齐发':
            self.moveWANJIAN(O,T)
        elif movename=='南蛮入侵':
            self.moveNANMAN(O,T)
        elif movename=='水淹七军':
            self.moveSHUI(O,T)
        elif movename=='无中生有':
            self.moveWUZHONG(O)
        elif movename=='乐不思蜀':
            isvalidmove = self.moveLE(T)
        elif movename=='兵粮寸断':
            self.moveBING(T)
        elif movename=='使用丈八蛇矛':
            isvalidmove = self.useZHANGBA(O,T)
            if isvalidmove:
                self.moveSHA(O,T)
        elif movename in {'诸葛连弩','青钢剑','丈八蛇矛','贯石斧','寒冰剑'}:
            if len(O.weapon_pai)>0:
                self.PD.QP.append(O.weapon_pai.pop(0))
                if O.name=='孙尚香':
                    O.shoupai.append(self.PD.MOPAI())
                    O.shoupai.append(self.PD.MOPAI())
                elif O.adv.name=='孙尚香':
                    O.adv.shoupai.append(self.PD.QP.pop(-1))                
            O.weapon_pai.append(self.PD.ZM.pop(-1))
        elif movename in {'仁王盾','八卦阵'}:
            if len(O.armor_pai)>0:
                self.PD.QP.append(O.armor_pai.pop(0))
                if O.name=='孙尚香':
                    O.shoupai.append(self.PD.MOPAI())
                    O.shoupai.append(self.PD.MOPAI())
                elif O.adv.name=='孙尚香':
                    O.adv.shoupai.append(self.PD.QP.pop(-1))
            O.armor_pai.append(self.PD.ZM.pop(-1))
        elif movename=='闪' and O.name=='赵云':
            isvalidmove = self.moveSHA(O,T)
        if O.name =='黄月英' and isvalidmove:
            if self.LEIXING.get(movename)=='jinnang':
                print '黄月英: 哼'
                O.shoupai.append(self.PD.MOPAI())
        bothlive = O.alive and T.alive
        return isvalidmove, bothlive
    def app_PINDIAN(self,O,T):
        '''
        拼点
        '''
        rank =[]
        for i in range(10):
            rank.append(str(i+1))
        rank+=['J','Q','K']
        available = show(O,self,'选择任意手牌')
        var = API(O, available,'拼点', O.name+'选择拼点牌','self')
        while 1:
            if var.isdigit() and int(var) in available:
                temp1 = self.pop_shoupai(O,int(var)-1)
                self.PD.ZM.append(temp1)
                num1 = rank.index(self.PAI[temp1][0][1])
                print O.name+'拼点使用'+show_pai(self,temp1,'all')
                break
        available = show(T,self,'选择任意手牌')
        var = API(T, available,'拼点', T.name+'选择拼点牌','self')
        while 1:
            if var.isdigit() and int(var) in available:
                temp2 = self.pop_shoupai(T,int(var)-1)
                self.PD.ZM.append(temp2)
                num2 = rank.index(self.PAI[temp2][0][1])
                print T.name+'拼点使用'+show_pai(self,temp2,'all')
                break
        if num1>num2:
            print O.name+'胜'
            return 1
        else:
            print T.name+'胜'
            return 0
            
    def app_damage(self,O,T,damage_type):
        '''
        一切O对T造成伤害经过此函数
        '''
        
        if damage_type =='杀':
            if T.armor() == '仁王盾' and O.weapon()!='青钢剑':
                if self.PAI[self.PD.ZM[-1]][0][0] in {'B','C'} or (T.name == '小乔' and self.PAI[self.PD.ZM[-1]][0][0] in {'C'}):
                    return
            elif O.weapon() == '寒冰剑' and len(T.shoupai)>0:
                var = API(O, {''},'useHANBING', O.name+'是否使用寒冰剑','self')
                if len(var)>0:
                    self.useHANBING(O,T)
                    return
            if O.name=='祝融' and len(O.shoupai)>0 and len(T.shoupai)>0:
                var = API(O, {''},'cast', '是否发动技能')
                if len(var)>0:
                    print '祝融: 尝尝我飞刀的厉害'
                    if self.app_PINDIAN(O,T): # 如果拼点赢了
                        self.app_NAPAI(O,T)
            if O.name=='许褚' and O.special==1:
                T.hp-=1
                print T.name+'受到1点伤害，伤害来源：'+O.name
        elif damage_type=='决斗':
            if O.name=='许褚' and O.special==1:
                T.hp-=1
                print T.name+'受到1点伤害，伤害来源：'+O.name
                
        if T.name =='小乔':
            var = API(T,['','1'],'cast', '是否使用天香?')
            if len(var)>0:
                available = show(T,self,'天香')
                while 1:
                    var = API(T,available,'QIPAI',"请选择天香牌")
                    if var =='':
                        break
                    elif var.isdigit() and int(var) in available:
                        self.PD.QP.append(self.pop_shoupai(T,int(var)-1))
                        self.app_damage(O,O,'')
                        for i in range(O.hp_top-O.hp):
                            O.shoupai.append(self.PD.MOPAI())
                        return        
        T.hp-=1
        print T.name+'受到1点伤害，伤害来源：'+O.name
        print T.name+'当前生命值：'+str(T.hp)
        lived = self.hp_check(T)
        if lived == 0:
            return
        if T.name=='郭嘉' and T.hp>0:
            T.shoupai.append(self.PD.MOPAI())
            T.shoupai.append(self.PD.MOPAI())
        elif T.name=='曹操' and T.hp>0:
            var = API(T, ['','1'],'cast', '是否发动奸雄?')
            if len(var)>0:
                print '曹操：宁教我负天下人，休叫天下人负我'
                T.shoupai+=self.PD.ZM
                self.PD.ZM=[]
        elif T.name=='司马懿' and T.hp>0:
            self.app_NAPAI(T,O)
            print '下次注意点'
        elif T.name=='夏侯惇' and T.hp>0:
            var = API(T, ['','1'],'cast', '是否使用刚烈?')
            if len(var)>0:
                self.PD.QP+=self.PD.ZM
                self.PD.ZM=[]
                print '以彼之道，还施彼身'
                temp=self.PD.MOPAI()
                self.PD.QP.append(temp)
                print '判定为'+show_pai(self,temp,'all')
                if self.PAI[temp][0][0]!='R':
                    if len(O.shoupai)>=2:
                        var = API(O, ['','1'],'cast', '是否弃两张手牌免除伤害?')
                        if len(var)>0:
                            while 1:
                                available = show(O,self,'选择任意手牌')
                                var = API(O, available,'QIPAI', "请出第一张牌")
                                if var =='':
                                    self.app_damage(T,O,'')
                                    break
                                elif var.isdigit() and int(var) in available:
                                    self.PD.QP.append(self.pop_shoupai(O,int(var)-1))
                                    break
                            while 1:
                                available = show(O,self,'选择任意手牌')
                                var = API(O, available,'QIPAI', "请出第二张牌")
                                if var =='':
                                    self.app_damage(T,O,'')
                                    O.shoupai.append(self.PD.QP.pop(-1))
                                    break
                                elif var.isdigit() and int(var) in available:
                                    self.PD.QP.append(self.pop_shoupai(O,int(var)-1))
                                    break
                        else:
                            self.app_damage(T,O,'')
                    else:
                        self.app_damage(T,O,'')

        if O.name == '魏延' and O.hp<O.hp_top:
            temp=self.PD.MOPAI()
            self.PD.QP.append(temp)
            print '判定为'+show_pai(self,temp,'all')
            if self.PAI[temp][0][0] in {'B','C'}:
                print '魏延：真是美味啊'
                O.hp+=1
            

    def useHANBING(self,O,T):
        '''
        寒冰剑
        '''
        l= len(T.weapon_pai)+len(T.armor_pai)+len(T.shoupai)
        if l>=2:
            l=2
        for i in range(l):
            self.app_QIPAI(O,T)
        
    def moveSHA(self,O,T):
        '''
        主动杀
        '''
        if T.name=='诸葛亮' and len(T.shoupai)==0:
            return 0
        elif T.name=='大乔':
            T.shoupai.append(self.PD.MOPAI())
        if O.name=='吕布':
            print '吕布： 神挡杀神，佛挡杀佛'
            if int(self.askforShan(O,T)):
                if int(self.askforShan(O,T)):
                    pass
                else:
                    self.app_damage(O,T,'杀')
            else:
                self.app_damage(O,T,'杀')
        elif O.name=='马超':
            var = API(O, ['','1'],'cast', '是否使用突袭?')
            if len(var)>0:
                temp = self.PD.MOPAI()
                self.PD.QP.append(temp)
                print '判定为'+show_pai(self,temp,'all')
                if self.PAI[temp][0][0] in {'R','F'}:
                    print '马超:全军突击！'
                    self.app_damage(O,T,'杀')
                elif int(self.askforShan(O,T)):
                    print '闪'
                else:
                    self.app_damage(O,T,'杀')
        elif O.name=='黄忠':
            if len(T.shoupai)>=O.hp:
                self.app_damage(O,T,'杀')
        elif O.name=='张飞' and O.killed==1:
                print '张飞：啊！！！'
        elif int(self.askforShan(O,T)):
            print '闪'
            if O.name=='庞德' and len(T.shoupai)+len(T.weapon_pai)+len(T.armor_pai)>0:
                var= API(O, ['','1'],'cast', '是否使用猛进?')
                if len(var)>0:
                    self.app_QIPAI(O,T)
        else:
            self.app_damage(O,T,'杀')
        O.killed=1
        return 1

    def app_QIPAI(self,O,T):
        '''
        主动弃对方牌，如寒冰剑触发
        '''
        print '选择要拆的牌'
        while 1:
            available={}
            if len(T.weapon_pai)>0:
                print 'w   武器   '+show_pai(self,T.weapon_pai[0],'all')
                available['w']=''
            if len(T.armor_pai)>0:
                print 'q   防具'+show_pai(self,T.armor_pai[0],'all')
                available['q']=''
            if len(T.shoupai)>0:
                print 'e   手牌'
                available['e']=''
            var=API(O, available,'app_QIPAI', '选择要拆的')
            if var=='e' and len(T.shoupai)>0:
                var = random.randint(1,len(T.shoupai))
                card_indx = self.pop_shoupai(T,var-1)
                self.PD.QP.append(card_indx)
                print T.name+'的一张'+self.PAI[card_indx][1]+'被拆掉了'
                break
            elif var=='w':
                card_indx = T.weapon_pai.pop(0)
                self.PD.QP.append(card_indx)
                print T.name+'的武器'+show_pai(self,card_indx,'all')+'被拆掉了'
                break
            elif var=='q':
                card_indx = T.armor_pai.pop(0)
                self.PD.QP.append(card_indx)
                print T.name+'的防具'+show_pai(self,card_indx,'all')+'被拆掉了'
                break
            
    def app_NAPAI(self,O,T):
        '''
        各种获取对方牌
        '''
        print '选择要顺的牌'
        available={}
        if len(T.weapon_pai)>0:
            print 'w   武器   '+show_pai(self,T.weapon_pai[0],'all')
            available['w']=''
        if len(T.armor_pai)>0:
            print 'q   防具   '+show_pai(self,T.armor_pai[0],'all')
            available['q']=''
        if len(T.shoupai)>0:
            print 'e   手牌'
            available['e']=''
        var=API(O, available,'app_NAPAI','选择要顺的牌')
        if var=='e' and len(T.shoupai)>0:
            var = random.randint(1,len(T.shoupai))
            card_indx = self.pop_shoupai(T,var-1)
            O.shoupai.append(card_indx)
            print O.name+'你得到了'+T.name+'的一张'+self.PAI[O.shoupai[-1]][1]
            return 1
        if var=='w' and len(T.weapon_pai)>0:
            card_indx = T.weapon_pai.pop(0)
            O.shoupai.append(card_indx)
            print O.name+'你得到了'+T.name+'的一张'+self.PAI[O.shoupai[-1]][1]
            return 1
        if var=='q' and len(T.armor_pai)>0:
            card_indx = T.armor_pai.pop(0)
            O.shoupai.append(card_indx)
            print O.name+'你得到了'+T.name+'的一张'+self.PAI[O.shoupai[-1]][1]
            return 1
        else:
            return 0
            
    def useZHANGBA(self,O,T):
        out = 0        
        temp = []
        for i in [1,2]:
            available = show(O,self,'选择任意手牌')
            while 1:
                var = API(O, available,'QIPAI', "选择丈八蛇矛弃牌"+str(i))
                if var =='':
                    return 0
                if int(var) not in available:
                    continue
                if int(var) in available:
                    out = 1
                    break
            card_indx = O.shoupai[int(var)-1]# 比如0 /48
            self.pop_shoupai(O,int(var)-1)                #从手中移除
            temp.append(card_indx)#移动到temp
        if out == 0: #没有执行
            O.shoupai +=temp
        else :#执行了
            self.PD.ZM+=temp                        #放到桌面
        return out

    def moveTAO(self,O):
        if O.hp<O.hp_top:
            if O.name =='周泰' and len(O.buqu_pai)>0:
                self.PD.QP.append(O.buqu_pai.pop(random.randint(0,len(O.buqu_pai)-1)))
                if len(O.buqu_pai)==0:
                    O.hp=1
            else:
                O.hp+=1
                print O.name+'生命回复1点'
                print O.name+'当前生命值：'+str(O.hp)
        else:
            print '无效的出牌，血满'
            O.shoupai.append(self.PD.ZM.pop(-1))

    def moveJUEDOU(self,O,T):
        #决斗
        if O.name == '吕布':
            print '吕布： 神挡杀神，佛挡杀佛'
            if int(self.askforSha(T)):
                print T.name+'杀'+O.name
                if int(self.askforSha(T)):
                    print T.name+'杀'+O.name
                    self.moveJUEDOU(T,O)
                else:
                    self.app_damage(O,T,'')
            else:
                self.app_damage(O,T,'')
        else: #不是吕布
            if int(self.askforSha(T)):
                print T.name+'杀'+O.name
                self.moveJUEDOU(T,O)
            else:
                self.app_damage(O,T,'决斗')

    def moveCHAI(self,O,T):
        '''
        过河拆桥
        '''
        if int(self.askforWuxie(O,'moveCHAI')):
            return 1
        elif int(self.askforWuxie(T,'moveCHAI')):
            return 1
        else:
            if len(T.weapon_pai)>0 or len(T.armor_pai)>0 or len(T.shoupai)>0:
                while 1:
                    var1 = API(O, ['1','2'],'moveCHAI', '要拆手牌还是装备? 1.装备 2.手牌')
                    if var1.isdigit() and int(var1) in {1,2}:
                        if var1=='1' and len(T.weapon_pai)+len(T.armor_pai)>0:
                            available = show(T,self,'装备')
                            while 1:
                                var2 =API(O, available,'app_QIPAI', '选择要拆的装备')
                                if var2=='w' and len(T.weapon_pai)>0:
                                    card_indx = T.weapon_pai.pop(0)
                                    self.PD.QP.append(card_indx)
                                    print T.name+'的武器'+show_pai(self,card_indx,'all')+'被拆掉了'
                                    return 1
                                elif var2=='q' and len(T.armor_pai)>0:    
                                    card_indx = T.armor_pai.pop(0)
                                    self.PD.QP.append(card_indx)
                                    print T.name+'的防具'+show_pai(self,card_indx,'all')+'被拆掉了'
                                    return 1
                        elif var1=='2' and len(T.shoupai)>0:
                            available = show(T,self,'选择任意手牌')
                            while 1:
                                var2 = API(O, available,'app_QIPAI', '选择要拆的手牌')   
                                if var2.isdigit() and int(var2) in available:
                                    card_indx = self.pop_shoupai(T,int(var2)-1)
                                    self.PD.QP.append(card_indx)
                                    print T.name+'的一张'+self.PAI[card_indx][1]+'被拆掉了'
                                    return 1
            else:
                return 0#失败

            
    def moveSHUN(self,O,T):
        '''
        顺手牵羊
        '''
        if T.name=='陆逊':
            return 0
        if int(self.askforWuxie(O,'moveSHUN')):
            return 1
        elif int(self.askforWuxie(T,'moveSHUN')):
            return 1
        else:
            if len(T.weapon_pai)>0 or len(T.armor_pai)>0 or len(T.shoupai)>0:
                return self.app_NAPAI(O,T)              
            else:
                return 0

    def moveWANJIAN(self,O,T):
        '''
        万箭齐发
        '''
        
        if int(self.askforWuxie(O,'moveWANJIAN')):
            return 1
        elif int(self.askforWuxie(T,'moveWANJIAN')):
            return 1
        elif int(self.askforShan(O,T)):
            return 1
        else:
            self.app_damage(O,T,'')

    def moveNANMAN(self,O,T):
        '''
        南蛮
        '''
        if T.name in {'祝融','孟获'}:
            print '无效'
            return
        if int(self.askforWuxie(O,'moveNANMAN')):
            return 1
        elif int(self.askforWuxie(T,'moveNANMAN')):
            return 1
        elif int(self.askforSha(T)):
            return 1
        else:
            self.app_damage(O,T,'')

    def moveSHUI(self,O,T):
        '''
        水淹
        '''
        if int(self.askforWuxie(O,'moveSHUI')):
            return 1
        elif int(self.askforWuxie(T,'moveSHUI')):
            return 1
        else:
            if len(T.weapon())>0 or len(T.armor())>0:
                var =API(T, ['','1'],'cast', '水淹七军，是否弃装备?','moveSHUI')
                if len(var)>0:
                    self.PD.QP+=T.armor_pai
                    self.PD.QP+=T.weapon_pai
                    T.armor_pai=[]
                    T.weapon_pai=[]
                else:
                    self.app_damage(O,T,'')
            else:
                self.app_damage(O,T,'')

    def moveWUZHONG(self,O):
        '''
        无中生有
        '''
        if int(self.askforWuxie(O,'moveWUZHONG')):
            return 1
        elif int(self.askforWuxie(O.adv,'moveWUZHONG')):
            return 1
        else:
            O.shoupai.append(self.PD.MOPAI())
            O.shoupai.append(self.PD.MOPAI())

    def moveLE(self,T):
        '''
        乐不思蜀
        '''
        print self.PD.ZM
        if T.name=='陆逊':
            return 0
        if len(T.LE_pai)==0:
            T.LE_pai.append(self.PD.ZM.pop(-1))
            return 1
        else :
            print T.name+ '已经被乐'
            return 0
        

    def moveBING(self,T):
        '''
        兵粮寸断
        '''
        if len(T.BING_pai)==0:
            T.BING_pai.append(self.PD.ZM.pop(-1))
            return 1
        else:
            print T.name +'已经被兵'
            return 0

    def askforShan(self,O,T):
        '''
        求闪
        '''
        out=0
        available = show(T,self,'求闪')
        print available
        if T.armor() == '八卦阵' and O.weapon()!='青钢剑':  #八卦阶段
            var = API(T, ['','1'],'cast', '是否使用八卦阵?')
            if len(var)>0:
                temp = self.PD.MOPAI()
                print '八卦阵判定为'+show_pai(self,temp,'all')
                if T.name=='郭嘉':
                    T.shoupai.append(temp)
                else:
                    self.PD.QP.append(temp)
                if self.PAI[temp][0][0] in {'B','C'} or (T.name=='小乔' and self.PAI[temp][0][0] in {'C'}):
                    print '判定失败'
                    out=0
                else:
                    print '判定成功'
                    out=1
                    return out
                                    # 非八卦阶段
        if T.name=='甄姬': #甄姬有装备时
            if len(T.weapon())>0:
                var = API(T, ['','1'],'cast', '是否放弃武器牌当作闪使用?')
                if len(var)>0:
                    self.PD.ZM.append(T.weapon_pai.pop(0))
                    return 1
            if len(T.armor())>0:
                var = API(T, ['','1'],'cast', '是否放弃装备牌当作闪使用?')
                if len(var)>0:
                    self.PD.ZM.append(T.armor_pai.pop(0))
                    return 1
        while 1:
            var = API(T, available,'askforShan', "请出一张闪")
            if var =='':
                return 0
            elif var.isdigit() and int(var) in available:
                out = 1
                break
        card_indx = T.shoupai[int(var)-1]# 比如0 /48
        self.pop_shoupai(T,int(var)-1)
        self.PD.QP.append(card_indx)                         #放到桌面
        print T.name+': 闪'
        if O.weapon()=='贯石斧':
            if self.useGUANSHIFU(O):
                out=0
            else:
                out=1
        return out

    def useGUANSHIFU(self,O):
        var = API(O, ['','1'],'cast', "是否使用贯石斧?")
        valid=0
        if len(var)>0:
            l = len(O.shoupai)+len(O.armor_pai)
            if l>=2:
                available = show(O,self,'选择任意手牌')
                if len(O.armor_pai)>0:
                    print 'q   防具   '+O.armor()
                    available['q']=''
                while 1:
                    var1 = API(O, available,'QIPAI','选择弃制牌1')
                    if var1.isdigit() and int(var1) in available:
                        self.PD.QP.append(O.shoupai[int(var1)-1])
                        break
                    elif var1=='q' and len(O.armor_pai)>0:
                        self.PD.QP.append(O.armor_pai.pop(0))
                        break
                    
                available = show(O,self,'选择任意手牌')
                if len(O.armor_pai)>0:
                    print 'q   防具   '+O.armor()
                    available['q']=''
                while 1:
                    var2 = API(O, available,'QIPAI', '选择弃制牌2')
                    if var2.isdigit() and int(var2) in available:
                        self.PD.QP.append(O.shoupai[int(var2)-1])
                        break
                    elif var2=='q' and len(O.armor_pai)>0:
                        self.PD.QP.append(O.armor_pai.pop(0))
                        break
                valid=1
            else:
                print '牌不够'
        return valid
    
    def askforSha(self,T):
        available = show(T,self,'求杀')
        print available
        while 1:
            var = API(T, available,'askforSha',"请出一张杀")
            if var =='':
                return 0
            elif var.isdigit() and int(var) in available:
                out = 1
                card_indx = T.shoupai[int(var)-1]# 比如0 /48
                self.pop_shoupai(T,int(var)-1)                #从手中移除
                self.PD.ZM.append(card_indx)                         #放到桌面
                break
            elif var=='w' and T.weapon()=='丈八蛇矛':
                out = self.useZHANGBA(T,T.adv)
            elif var=='e' and T.name=='关羽':
                available = show(T,self,'求红')
                if len(T.weapon_pai)>0 and self.PAI[T.weapon_pai[0]][0] in {'R','F'}:
                    print 'w   武器'
                var = API(T, available,'QIPAI', '选张红')
                while 1:
                    if var=='':
                        valid=0
                        break
                    elif var=='w':
                        if self.PAI[T.weapon_pai[0]][0] in {'R','F'}:
                            self.PD.ZM.append(T.weapon_pai.pop(0))
                            return 1
                        else:
                            print T.name+'无效的出牌'
                    elif var.isdigit() and int(var) in available:
                        self.PD.ZM.append(T.shoupai.pop(int(var)-1))
                        return 1
                    else:
                        print T.name+'无效的出牌'

        print T.name+': 杀'
        return out

    def askforWuxie(self,T,ENV):
        available = show(T,self,'求无懈')
        print available
        if len(available)==0:
            print T.name+'没有无懈可击'
            return 0
        while 1:
            var = API(T, available,'askforWuxie', "请出一张无懈可击",ENV)
            if var =='':
                return 0
            if var.isdigit() and int(var) in available:
                out = 1
                break
        card_indx = T.shoupai[int(var)-1]# 比如0 /48
        self.pop_shoupai(T,(int(var)-1))                    #从手中移除
        self.PD.QP.append(card_indx)                         #放到桌面
        print T.name+': 无懈可击'
        if T.name=='黄月英':
            T.shoupai.append(self.PD.MOPAI())
            print T.name +': 哼!'
        return out

    def askforTAO(self,T,target):
        available = show(T,self,'求桃')
        print available
        while 1:
            var = API(T, available,'askforTAO', "请出一张桃",target)
            if var =='':
                return 0
            if var.isdigit() and int(var) in available:
                out = 1
                break
        card_indx = T.shoupai[int(var)-1]# 比如0 /48
        self.pop_shoupai(T,(int(var)-1))                    #从手中移除
        self.PD.QP.append(card_indx)                         #放到桌面
        print T.name+': 桃'
        return out

