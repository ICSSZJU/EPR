# -*- coding: utf-8 -*-
"""
This work is licensed under the Creative Commons 
Attribution-NonCommercial-ShareAlike 3.0 Unported 
License. To view a copy of this license, visit 
http://creativecommons.org/licenses/by-nc-sa/3.0/.

Design:Chen Shu & Zhang Hong
Programming:Zhang Hong
"""
import copy
import random
import numpy as np

class population(object):
    '''种群类，适用于各种种群动力学模型'''
    def __init__(self,ingredient):
        '''接受一个list类型数组，初始化种群
           例如：
               p=population([10,20])
           则p为一个种群，其中第一种类型（物
           种）数量为10，第二种数量为20
        '''
        self.__ingredient=copy.deepcopy(ingredient)
    
    def __getitem__(self,key):
        '''索引器方法，用于取得索引号为"key"的人口的数量
           例如:
               p=population([10,20])
               a=p[1]
           则a的值为20
        '''
        return self.__ingredient[key]
        
    def __setitem__(self,key,value):
        '''索引器方法，用于设置索引号为"key"的人口的数量
           例如：
               p=population([10,20])
               p[0]=5
           则p的第一种类型的数量变为5
        '''
        self.__ingredient[key]=value
        
    def __len__(self):
        '''取得种群的类型数
           例如：
               p=population([10,20])
               a=len(p)
           则a的值为2
        '''
        return len(self.__ingredient)        
    
    def __str__(self):
        '''种群的字符串表示，主要用于"print"函数'''
        return "population"+"("+str(self.__ingredient)+")"
        
    def __repr__(self):
        return self.__str__()
        
    def __add__(self,right):
        assert isinstance(right,population),"人口只能与人口相加"
        return population([x+y for x,y in zip(self,right)])
        
    def __sub__(self,right):
        assert isinstance(right,population),"人口只能与人口相减"
        return population([x-y for x,y in zip(self,right)])
        
    @property
    def population_size(self):
        '''取得种群的总人口数
           例如：
               p=population([10,20])
               a=p.population_size
           则a的值为30
        '''
        return sum(self.__ingredient)
        
    def reduce(self,index):
        '''根据index减少相应类型的人口
           例如：
               p=population([10,20])
               p.reduce(1)
        '''
        self.__ingredient[index]-=1
        if self.__ingredient[index]<0:
            self.__ingredient[index]+=1
            self.reduce(random.randint(0,len(self)-1))
        
    def __index_of(self,member):
        '''给定member，求它的索引号，判断它属于哪个类型
           此方法主要与抽样算法联合使用
        '''
        temp=0
        count=0
        for i in self.__ingredient:
            if member>=temp and member<temp+i:
                return count
            temp+=i
            count+=1
        return -1
    
    def sampling(self,amount):
        '''取出数量为amount的样本'''
        sample=random.sample(range(self.population_size),amount)
        participant_index=[self.__index_of(s) for s in sample]
        pop=population([0]*self.population_size)
        for s in sample:
            pop.add(self.__index_of(s))
        return pop,sample,participant_index
    
    def clone(self):
        return population(copy.deepcopy(self.__ingredient)) 
        
    def add(self,index):
        '''增加索引为index的类型的人口'''
        self.__ingredient[index]+=1
        
    def add_by_prob(self,prob):
        '''根据概率参数增加某种类型的人口'''
        self.add(self.select_by_prob(prob))
        
    def select_by_prob(self,prob):
        '''根据概率参数选择某种类型的人口，返回其索引值'''
        temp=0.0
        r=random.random()
        for i in range(len(self)):
            if r<=prob[i]+temp and r>=temp:
                return i
                break
            temp+=prob[i]
            
    def set_attr(self,p):
        '''给所有个体设置一个属性，每个个体以概率p获得这一属性'''
        assert p<=1 and p>=0,"概率必须大于0小于1."
        randlist=np.random.rand(self.population_size)
        attrlist=np.array([int(r<p) for r in randlist])
        return attrlist
    
    def set_random_attr(self,start,stop):
        r=stop-start
        return [start+a*r for a in np.random.rand(self.population_size)]
        
    def imitate(self,p):
        '''进行变异，每个个体以概率p变为另一类型的个体'''
        imitatelist=self.set_attr(p)
        for i in range(self.population_size):
            if imitatelist[i]:
                index=self.__index_of(i)
                indexlist=range(len(self))
                indexlist.remove(index)
                self.reduce(index)
                self.add(random.choice(indexlist))
                
    def split(self,attrlist):
        '''根据属性将种群分成两个'''
        p1=population([0]*len(self))
        p2=population([0]*len(self))
        for i in range(self.population_size):
            index=self.__index_of(i)
            if attrlist[i]==True:
                p1.add(index)
                continue
            else:
                p2.add(index)
                continue
        return p1,p2
    
    def join(self,right):
        '''连接两个种群'''
        return population([p for p in self]+[p for p in right])

