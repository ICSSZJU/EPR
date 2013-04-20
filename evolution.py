# -*- coding: utf-8 -*-
"""
This work is licensed under the Creative Commons 
Attribution-NonCommercial-ShareAlike 3.0 Unported 
License. To view a copy of this license, visit 
http://creativecommons.org/licenses/by-nc-sa/3.0/.

Design:Chen Shu & Zhang Hong
Programming:Zhang Hong
"""
import numpy as np
import math
import random
from population import population
import observer
import ui

parameter=ui.parameters()

parameter.m=20
parameter.n=10000
parameter.number_of_B=0
parameter.number_of_X=50
parameter.number_of_E=50
parameter.battle_cost=2
parameter.endowment_effect=0.5
parameter.resource_rate=0.5
parameter.imitate_rate=0.01
parameter.selection_strength=0.5
parameter.real_trans=True
parameter.profit_function="x**endowment_effect"
parameter.batch_mode=True

parameter.configure_traits()

traits=parameter.__getstate__()

real_trans=parameter.real_trans

m=parameter.m #每期重复的轮次

n=parameter.n #期数

resource_rate=parameter.resource_rate #拥有资源的概率

imitate_rate=parameter.imitate_rate #变异率

c=parameter.battle_cost #战斗成本

evo_pop=population([parameter.number_of_B,parameter.number_of_X,parameter.number_of_E])   #设定B、X、E三者的人数

endowment_effect=parameter.endowment_effect #禀赋效应

pro_func=eval("lambda x:"+parameter.profit_function)

w=parameter.selection_strength #选择强度

class evolution(object):
    def __init__(self,evo_pop,pro_func,endowment_effect,resource_rate,battle_cost,imitate_rate,selection_strength,m,n):
        self.evo_pop=evo_pop
        self.profit_func=pro_func
        self.endowment_effect=endowment_effect
        self.resource_rate=resource_rate
        self.battle_cost=battle_cost
        self.imitate_rate=imitate_rate
        self.selection_strength=selection_strength
        self.m=m
        self.n=n
        
        #无产者与有产者相遇时的博弈(函数)矩阵
        self.nonp_p_game=[[self.avoid,self.rob_avoid,self.conditional_rob_avoid_avoid],
                          [self.battle,self.rob,self.conditional_rob_battle],
                          [self.conditional_battle_avoid,self.conditional_rob_rob_avoid,self.conditional_rob_avoid]]
        
    
    def grow_resource(self): 
        '''增长资源，假如某个体拥有资源，它的资源增加1单位'''
        for i in np.arange(self.evo_pop.population_size):
            if self.resource[i]!=0:
                self.resource[i]+=1
            else:
                continue
            
    def trans_resource(self,nonp,p):
        '''将某有产者(p)的资源转向某无产者(nonp)''' 
        if real_trans:
            self.resource[nonp[1]]=1
            self.resource[p[1]]=0

    
    def add_payoff(self,member):    
        '''给指定成员(member)增加收益(payoff)'''
        self.payoff[member[0]]+=self.profit_func(self.resource[member[1]])
    
    def rob_avoid(self,nonp,p):
        if random.choice([True,False]):
            self.trans_resource(nonp,p)
            self.add_payoff(nonp)
        else:
            self.avoid(nonp,p)
    
    def conditional_rob_avoid_avoid(self,nonp,p):
        if self.convention_standard[nonp[1]]>self.convention_standard[p[1]]:
            self.rob_avoid(nonp,p)
        else:
            self.avoid(nonp,p)
    
    def conditional_rob_rob_avoid(self,nonp,p):
        if self.convention_standard[nonp[1]]>self.convention_standard[p[1]]:
            self.rob(nonp,p)
        else:
            self.rob_avoid(nonp,p)
            
    def avoid(self,nonp,p):
        '''无产者遇有产者时避免接触'''
        self.add_payoff(p)
        
    def battle(self,nonp,p):
        '''无产者(nonp)试图抢有产者(p),引发战斗'''
        self.battle_count+=1
        if random.choice([True,False]):
            self.trans_resource(nonp,p)
            self.payoff[nonp[0]]+=self.profit_func(self.resource[nonp[1]])-c
            self.payoff[p[0]]-=c
        else:
            self.payoff[nonp[0]]-=c
            self.payoff[p[0]]+=self.profit_func(self.resource[p[1]])-c

    def rob(self,nonp,p):
        '''无产者(nonp)抢有产者(p)'''
        self.trans_resource(nonp,p)
        self.add_payoff(nonp)
        
    def conditional_rob_battle(self,nonp,p):
        '''根据惯例标准，进行战斗或抢劫'''
        if self.convention_standard[nonp[1]]>self.convention_standard[p[1]]:
            self.rob(nonp,p)
        else:
            self.battle(nonp,p)
            
    def conditional_battle_avoid(self,nonp,p):
        '''根据惯例标准，战斗或避开'''
        if self.convention_standard[nonp[1]]>self.convention_standard[p[1]]:
            self.battle(nonp,p)
        else:
            self.add_payoff(p)
            
    def conditional_rob_avoid(self,nonp,p):
        '''根据战斗标准，抢劫或避开'''
        if self.convention_standard[nonp[1]]>self.convention_standard[p[1]]:
            self.rob(nonp,p)
        else:
            self.add_payoff(p)
            
    def run(self):
        for i in xrange(self.n):
         
            #初始化payoff数组
            self.payoff=np.zeros(len(self.evo_pop))
            #分配初始资源
            self.resource=evo_pop.set_attr(self.resource_rate)
            #分配惯例标准
            self.convention_standard=evo_pop.set_random_attr(0,1)
            self.battle_count=0
            B,X,E=self.evo_pop
            rB=self.resource[:B]
            rX=self.resource[B:B+X]
            rE=self.resource[B+X:]
            gB=[]
            gX=[]
            gE=[]
            sB=[]
            sX=[]
            sE=[]
            for j in range(self.m):
                sB.append(np.sum(rB)/float(B) if B!=0 else 0)
                sX.append(np.sum(rX)/float(X) if X!=0 else 0)
                sE.append(np.sum(rE)/float(E) if E!=0 else 0)
                gB.append((np.count_nonzero(rB))/float(B) if B!=0 else 0)
                gX.append((np.count_nonzero(rX))/float(X) if X!=0 else 0)
                gE.append((np.count_nonzero(rE))/float(E) if E!=0 else 0)
                
                sample,participants,index=self.evo_pop.sampling(2)
                pleft,pright=participants
                ileft,iright=index
                left=(ileft,pleft)
                right=(iright,pright)
                #以上代码取得博弈样本，left和right索引0的
                #值为它们所属类型（索引），索引1的值代表它
                #们是哪个个体，例如，left可能是(1,67)
                self.game(left,right)
                #根据取得的样本进行博弈
                self.grow_resource()
                #增长资源
            #以下代码为策略更新和变异  
            
            ag=(np.average(gB),np.average(gX),np.average(gE))
            ar=(np.average(sB),np.average(sX),np.average(sE))
            fitness=[math.exp(x*w) for x in self.payoff]
            
            evo_pop.add_by_prob([x/sum(fitness) for x in fitness])
            evo_pop.reduce(random.randint(0,2))
            evo_pop.imitate(self.imitate_rate)
            yield self.evo_pop,self.battle_count,i,ag,ar,fitness
            
    def game(self,left,right):
        if self.resource[left[1]] and self.resource[right[1]]:
            '''两者都有资源，分别增加收益'''
            self.add_payoff(left)
            self.add_payoff(right)
        elif self.resource[left[1]]==0 and self.resource[right[1]]: 
            '''左无产有有产，根据博弈矩阵进行博弈'''
            self.nonp_p_game[left[0]][right[0]](left,right)
        elif self.resource[left[1]] and self.resource[right[1]]==0: 
            '''左有产右无产，根据博弈矩阵进行博弈(因为博弈是对称的，交换位置进行即可)'''
            self.nonp_p_game[right[0]][left[0]](right,left)
        else:
            '''两者都是无产者'''
            pass
       
e=evolution(evo_pop,pro_func,endowment_effect,resource_rate,c,imitate_rate,w,m,n) 
      
p=observer.observer(e.run,sum(evo_pop),n,traits,batchmode=parameter.batch_mode)        
p.start()



#遗弃代码
#def add_resource(rlist):
#    for i in range(len(rlist)):
#        if rlist[i]>0:
#            rlist[i]+=1
#        else:
#            continue
#
#def trans_resource(rlist,left,right):
#    '''left转移至right'''
#    rlist[left]=0
#    rlist[right]=1
#    
#def get_res(parti,res):
#    return (res[parti[0]],res[parti[1]])
#    
#
#        
#def evo_run():
#    yield evo_pop,0
#    for j in xrange(n):
#        
#        payoff=[0]*len(evo_pop)
#        
#        conven_standard=evo_pop.set_random_attr(0,1)
#        resource=[int(x) for x in evo_pop.set_attr(resource_rate)]  
#        
#        for i in range(m):
#           
#            sample,parti,participants=evo_pop.sampling(2)
#            
#            res=get_res(parti,resource)
#            
#            parti_conven=(conven_standard[parti[0]],conven_standard[parti[1]])
#            
#            left=participants[0]
#            right=participants[1]
#            rleft=res[0]
#            rright=res[1]
#
#            
#            if all(res):
#                payoff[left]+=pro_func(rleft)
#                payoff[right]+=pro_func(rright)
#            elif rleft==0 and rleft==0:
#                pass
#            elif rleft==0:
#                if left==0:
#                    payoff[right]+=pro_func(rright)
#                elif left==1:
#                    if right==0:
#                        if random.choice([0,1]):
#                                trans_resource(resource,parti[1],parti[0])
#                                payoff[left]+=pro_func(1)-c
#                                payoff[right]-=c
#                        else:
#                            payoff[left]-=c
#                            payoff[right]+=pro_func(rright)-c
#                    elif right==1:
#                        trans_resource(resource,parti[1],parti[0])
#                        payoff[left]+=pro_func(1)
#                    else:
#                        if parti_conven[0]>parti_conven[1]:
#                            trans_resource(resource,parti[1],parti[0])
#                            payoff[left]+=pro_func(1)
#                        else:
#                            if random.choice([0,1]):
#                                trans_resource(resource,parti[1],parti[0])
#                                payoff[left]+=pro_func(1)-c
#                                payoff[right]-=c
#                            else:
#                                payoff[left]-=c
#                                payoff[right]+=pro_func(rright)-c
#                else:
#                    if right==0:
#                        if parti_conven[0]>parti_conven[1]:
#                            if random.choice([0,1]):
#                                trans_resource(resource,parti[1],parti[0])
#                                payoff[left]+=pro_func(1)-c
#                                payoff[right]-=c
#                            else:
#                                payoff[left]-=c
#                                payoff[right]+=pro_func(rright)-c
#                        else:
#                            payoff[right]+=pro_func(rright)
#                    else:
#                        if parti_conven[0]>parti_conven[1]:
#                            trans_resource(resource,parti[1],parti[0])
#                            payoff[left]+=pro_func(1)
#                        else:
#                            payoff[right]+=pro_func(rright)
#            else:
#                if left==0:
#                    if right==0:
#                        payoff[left]+=pro_func(rleft)
#                    elif right==1:
#                        if random.choice([0,1]):
#                            trans_resource(resource,parti[0],parti[1])
#                            payoff[left]-=c
#                            payoff[right]+=pro_func(1)-c
#                        else:
#                            payoff[left]+=pro_func(rleft)-c
#                            payoff[right]-=c
#                    else:
#                        if parti_conven[0]>parti_conven[1]:
#                            payoff[left]+=pro_func(rleft)
#                        else:
#                            if random.choice([0,1]):
#                                trans_resource(resource,parti[0],parti[1])
#                                payoff[left]-=c
#                                payoff[right]+=pro_func(1)-c
#                            else:
#                                payoff[left]+=pro_func(rleft)-c
#                                payoff[right]-=c
#                elif left==1:
#                    if right==0:
#                        payoff[left]+=pro_func(rleft)
#                    elif right==1:
#                        trans_resource(resource,parti[0],parti[1])
#                        payoff[1]+=pro_func(1)
#                    else:
#                        if parti_conven[0]>parti_conven[1]:
#                            payoff[left]+=pro_func(rleft)
#                        else:
#                                trans_resource(resource,parti[0],parti[1])
#                                payoff[right]+=pro_func(1)-c
#
#                else:
#                    if right==0:
#                        payoff[left]+=pro_func(rleft)
#                    elif right==1:
#                        if parti_conven[0]>parti_conven[1]:
#                            if random.choice([0,1]):
#                                trans_resource(resource,parti[0],parti[1])
#                                payoff[left]-=c
#                                payoff[right]+=pro_func(1)-c
#                            else:       
#                                payoff[right]-=pro_func(1)
#                    else:
#                        if parti_conven[0]>parti_conven[1]:
#                            payoff[left]+=pro_func(rleft)
#                        else:
#                            trans_resource(resource,parti[0],parti[1])
#                            payoff[right]+=pro_func(1)
#            add_resource(resource)    
#    
#        fitness=[math.exp(x*w) for x in payoff]        
#        evo_pop.add_by_prob([x/sum(fitness) for x in fitness])
#        evo_pop.reduce(random.randint(0,2))
#        evo_pop.imitate(imitate_rate)
#        yield evo_pop,j+1
#        
#
#p=plotter.plotter(evo_run,sum(evo_pop),n)        
#p.run()
#

