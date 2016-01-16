 # -*- coding: utf-8 -*-


def API(player, available,state, txt,*args):
    '''
    与智能体的接口(人类或AI)
    player: 角色,通过class player(object)构建
    available: 当前选项，可出的牌和技能，如{1,2,3,w,e}
    state: 描述当前状态的变量，如'askforSha'
    *args: 描述当前状态的可选变量
    
    '''
    if player.mode ==0: #人类
        var = raw_input(txt)
    elif player.mode==1: #有限状态机器
        if len(args)>0: 
            var = player.AI.askforAI(available,state,args)
        else:
            var = player.AI.askforAI(available,state)
    elif player.mode==2: #神经网络
	pass #TODO
    return var
