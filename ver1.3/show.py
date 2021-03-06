 # -*- coding: utf-8 -*-
            

def colored(txt,op):
    if op=='red':
        return '---'+txt+'----'
    else:
        return '***'+txt+'***'

def show_hua(char2):
    '''
    输入花色字母
    输出中文
    '''
    if char2[0]=='B':
        return '黑桃'+char2[1]
    if char2[0]=='R':
        return '红桃'+char2[1]
    if char2[0]=='C':
        return '草花'+char2[1]
    if char2[0]=='F':
        return '方片'+char2[1]

def show_pai(PAI,indx,op):
    '''
    返回文字 op in {huase, pai, pai_leixing, all}
    用于打印信息
    '''
    if op=='huase':
        return show_hua(PAI.PAI[indx][0])
    if op=='pai':
        return PAI.PAI[indx][1]
    if op=='all': #
        return PAI.PAI[indx][1]+'  '+show_hua(PAI.PAI[indx][0])
    if op=='pai_leixing':
        PAI.LEIXING[PAI.PAI[indx][0][1]]

def show(player,PAI,case):
    '''
    显示手牌
    在每次出牌前显示
    如
    1  决斗 黑桃1
    2  杀
    等等
    '''
    
    print player.name+case+'   ['+player.weapon()+']   ['+player.armor()+']   剩余血量'+str(player.hp)
    LE=''
    BING=''
    if len(player.LE_pai)>0:
        LE='乐'
    if len(player.BING_pai)>0:
        BING='兵'
    print '('+LE +') (' +BING+')'
    available = {}
    l = len(player.shoupai)
        #技能
    if case == '装备':
        if len(player.weapon_pai)>0:
            print 'w   武器   '+show_pai(PAI,player.weapon_pai[0],'all')
            available['w']=player.weapon_pai[0]
        if len(player.armor_pai)>0:
            print 'q   防具'+show_pai(PAI,player.armor_pai[0],'all')
            available['q']=player.armor_pai[0]            
    elif case == '出牌阶段':
        for i in range(l):
            temp1= show_hua(PAI.PAI[player.shoupai[i]][0])
            P = PAI.PAI[player.shoupai[i]][1]
            if (player.name=='赵云' and P=='闪' and (player.killed==0 or player.weapon()=='诸葛连弩')):
                print str(i+1)+'  '+P+'  '+temp1#能出的显示默认颜色
                available[i+1]=player.shoupai[i]
            elif (P in PAI.NE1) or (P=='桃' and player.hp >= player.hp_top) or (P=='杀' and player.killed==1 and player.weapon()!='诸葛连弩' and player.name!='张飞') or (player.adv.name=='陆逊' and P in {'顺手牵羊','乐不思蜀'}):
                print colored(str(i+1)+'  '+P+'  '+temp1,'red')#不能出的显示成红色
            elif P in {'过河拆桥','顺手牵羊'} and len(player.adv.shoupai)+len(player.adv.weapon_pai)+len(player.adv.armor_pai)==0:
                print colored(str(i+1)+'  '+P+'  '+temp1,'red')#不能出的显示成红色                
            else :
                print str(i+1)+'  '+P+'  '+temp1#能出的显示默认颜色
                available[i+1]=player.shoupai[i]
        if player.killed==0 and player.weapon() =='丈八蛇矛':
            print 'w   '+'使用丈八蛇矛'
            available['w']=player.weapon_pai[0]
        if player.name in player.JINENG.haveJINENG and player.magiced==0 and len(player.shoupai)>0:
            if player.name =='许褚':
                if player.U_skill ==1 and len(player.shoupai)>0 and len(player.adv.shoupai)>0:
                    pass
                else:
                    return available
            print 'e   使用'+player.magic
            available['e']=''
    elif case == '求闪':
        for i in range(l):
            temp1= show_hua(PAI.PAI[player.shoupai[i]][0])
            P = PAI.PAI[player.shoupai[i]][1]
            if P =='闪' or (player.name=='赵云' and P=='杀'):
                print str(i+1)+'  '+P+'  '+temp1
                available[i+1]=player.shoupai[i]
            else:
                print colored(str(i+1)+'  '+P+'  '+temp1,'red')
    elif case == '求桃':
        for i in range(l):
            temp1= show_hua(PAI.PAI[player.shoupai[i]][0])
            P = PAI.PAI[player.shoupai[i]][1]
            if P !='桃':
                print colored(str(i+1)+'  '+P+'  '+temp1,'red')
            else:
                print str(i+1)+'  '+P+'  '+temp1
                available[i+1]=player.shoupai[i]
    elif case == '求无懈':
        for i in range(l):
            temp1= show_hua(PAI.PAI[player.shoupai[i]][0])
            P = PAI.PAI[player.shoupai[i]][1]
            if P !='无懈可击':
                print colored(str(i+1)+'  '+P+'  '+temp1,'red')
            else:
                print str(i+1)+'  '+P+'  '+temp1
                available[i+1]=player.shoupai[i]
    elif case =='求杀':
        for i in range(l):
            temp1= show_hua(PAI.PAI[player.shoupai[i]][0])
            P = PAI.PAI[player.shoupai[i]][1]
            if P =='杀' or (player.name=='赵云' and P=='闪'):
                print str(i+1)+'  '+P+'  '+temp1
                available[i+1]=player.shoupai[i]
            else:
                print colored(str(i+1)+'  '+P+'  '+temp1,'red')
        if player.weapon() =='丈八蛇矛' and len(player.shoupai)>=2:
            print 'w   '+'使用丈八蛇矛'
            available['w']=''
        if player.name in {'关羽'}:
            print 'e   '+'发动技能'
            available['e']=''
    elif case == '选择任意手牌':
        for i in range(l):
            temp1= show_hua(PAI.PAI[player.shoupai[i]][0])
            P = PAI.PAI[player.shoupai[i]][1]
            print str(i+1)+'  '+P+'  '+temp1
            available[i+1]=player.shoupai[i]
    elif case == '选择所有牌':
        available = show(player,PAI,'选择任意手牌')
        if len(player.weapon_pai)>0:
            print 'w'+'  '+PAI.PAI[player.weapon_pai[0]][1]+'   '+show_hua(PAI.PAI[player.weapon_pai[0]][0])
        if len(player.armor_pai)>0:   
            print 'q'+'  '+PAI.PAI[player.armor_pai[0]][1]+'   '+show_hua(PAI.PAI[player.armor_pai[0]][0])
            
    elif case == '求黑':
        for i in range(l):
            temp1= show_hua(PAI.PAI[player.shoupai[i]][0])
            P = PAI.PAI[player.shoupai[i]][1]
            if PAI.PAI[player.shoupai[i]][0][0] in {'B','C'}:
                print str(i+1)+'  '+P+'  '+temp1
                available[i+1]=player.shoupai[i]
            else:
                print colored(str(i+1)+'  '+P+'  '+temp1,'red')
    elif case == '求红':
        for i in range(l):
            temp1= show_hua(PAI.PAI[player.shoupai[i]][0])
            P = PAI.PAI[player.shoupai[i]][1]
            if PAI.PAI[player.shoupai[i]][0][0] in {'R','F'}:
                print str(i+1)+'  '+P+'  '+temp1
                available[i+1]=player.shoupai[i]
            else:
                print colored(str(i+1)+'  '+P+'  '+temp1,'red')
    elif case =='选择方片':
        for i in range(l):
            temp1= show_hua(PAI.PAI[player.shoupai[i]][0])
            P = PAI.PAI[player.shoupai[i]][1]
            if PAI.PAI[player.shoupai[i]][0][0]=='F':
                print str(i+1)+'  '+P+'  '+temp1
                available[i+1]=player.shoupai[i]
            else:
                print colored(str(i+1)+'  '+P+'  '+temp1,'red')
        if len(player.weapon())>0:
            if PAI.PAI[player.weapon_pai[0]][0][0]=='F':
                print 'w'+'  '+PAI.PAI[player.weapon_pai[0]][1]+'   '+show_hua(PAI.PAI[player.weapon_pai[0]][0])
        if len(player.armor())>0:
            if PAI.PAI[player.armor_pai[0]][0][0]=='F':         
                print 'q'+'  '+PAI.PAI[player.armor_pai[0]][1]+'   '+show_hua(PAI.PAI[player.armor_pai[0]][0])

    elif case=='断粮':
        for i in range(l):
            temp1= show_hua(PAI.PAI[player.shoupai[i]][0])
            P = PAI.PAI[player.shoupai[i]][1]
            if PAI.PAI[player.shoupai[i]][0][0] in {'B','C'} and (PAI.LEIXING[P]!='jinnang'):
                print str(i+1)+'  '+P+'  '+temp1
                available[i+1]=player.shoupai[i]
            else:
                print colored(str(i+1)+'  '+P+'  '+temp1,'red')
        if len(player.weapon_pai)>0:
            if PAI.PAI[player.weapon_pai[0]][0][0] in {'B','C'}:
                print 'w'+'  '+PAI.PAI[player.weapon_pai[0]][1]+'   '+show_hua(PAI.PAI[player.weapon_pai[0]][0])
        if len(player.armor_pai)>0:
            if PAI.PAI[player.armor_pai[0]][0][0] in {'B','C'}:         
                print 'q'+'  '+PAI.PAI[player.armor_pai[0]][1]+'   '+show_hua(PAI.PAI[player.armor_pai[0]][0])
    elif case =='强袭':
        if len(player.weapon())>0:
            available['w']=player.weapon_pai[0]
        for i in range(l):
            P = PAI.PAI[player.shoupai[i]][1]
            if PAI.LEIXING[P]=='wuqi':
                available[i+1]=player.shoupai[i]
    elif case =='天香':
        for i in range(l):
            temp1= show_hua(PAI.PAI[player.shoupai[i]][0])
            P = PAI.PAI[player.shoupai[i]][1]
            if PAI.PAI[player.shoupai[i]][0][0] in {'R','B'}:
                print str(i+1)+'  '+P+'  '+temp1
                available[i+1]=player.shoupai[i]
            else:
                print colored(str(i+1)+'  '+P+'  '+temp1,'red')
            
        
    print '空'+'  '+'结束'
    
    print available
    return available
    
