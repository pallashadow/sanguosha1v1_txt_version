## san guo sha
 # -*- coding: utf-8 -*-
'''
作者: pallashadow
欢迎访问人工智能吧 http://tieba.baidu.com/f?kw=%C8%CB%B9%A4%D6%C7%C4%DC&pn=0
相关讨论：http://tieba.baidu.com/p/4305684246
LICENSE: BSD
游戏规则基于web.sanguosha.com，1v1模式

搭建了游戏基本规则和一个低级有限状态机AI（只写了手牌价值的顺序）
写这个东西主要是为了检验在一个繁琐的游戏规则下，各种AI算法的可行性
也可以当作游戏来玩
比我最开始想象的复杂不少，游戏本身就用了1000+行代码
后来烂尾了，神经网络部分没完成

各脚本介绍：
1.main.py，底层
2.scripts.py，四个脚本，
3.round1.py，定义startGame(wj1,wj2,op1,op2,op3):开始一局游戏
主函数 startGame(wj1,wj2,op1,op2,op3)
wj1 wj2 为武将名称 可选武将：
['张辽','陆逊','孙权','大乔','周瑜','黄盖','孙尚香','诸葛亮','黄月英','祝融','孟获','黄忠','马超','魏延','张飞','关羽','赵云','曹操','徐晃','司马懿','夏侯惇','郭嘉','许褚','典韦','甄姬','吕布','貂蝉','颜良文丑','庞德']
op1 op2 为'人／机选项' 0表示手动操作，1表示AI自动
op3 0或1 1为记录局势为神经网络array，会减慢运行速度#未启用
4.paidui.py 定义牌堆，和各种出牌事件
5.player.py 定义玩家
6.jineng.py 定义武将技能
7.ai.py 定义有限状态机
8.api.py 游戏本体和智能体接口

'''
import codecs
import random
import copy
import pickle

from scripts import *
from wujiang import *


print '三国杀新1v1 v1.2文字版'
print '可选武将：'
WJ = WUJIANG()
text =''
for i in WJ:
    text+=i+'  '
print text
print '游戏开始'
#M,V= script1(WJ,1)   #全武将AI互相PK
#script2(WJ)   #单武将随机AI
#script3(WJ)                #单武将AI对全武将AI，逐一PK测试
script4(WJ) #人机对战
#wj1 = '周泰'
#wj2 = WJ[random.randint(0,len(WJ)-1)]
#op1=0
#op2=1
#main(wj1,wj2,op1,op2,0)
