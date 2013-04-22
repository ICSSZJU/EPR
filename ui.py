# -*- coding: utf-8 -*-
"""
This work is licensed under the Creative Commons 
Attribution-NonCommercial-ShareAlike 3.0 Unported 
License. To view a copy of this license, visit 
http://creativecommons.org/licenses/by-nc-sa/3.0/.

Design:(Temporary Anonymous) & Zhang Hong
Programming:Zhang Hong
"""

import enthought.traits.api as trait
from enthought.traits.ui.api import View,Group,Item
class parameters(trait.HasTraits):
    number_of_B=trait.Int
    number_of_X=trait.Int
    number_of_E=trait.Int
    m=trait.Int
    n=trait.Int
    resource_rate=trait.Float
    imitate_rate=trait.Float
    battle_cost=trait.Float
    endowment_effect=trait.Float
    selection_strength=trait.Float
    real_trans=trait.Bool
    profit_function=trait.Str
    batch_mode=trait.Bool
    
    view=View(
              Group(
                  Group(Item('number_of_B',label=u"B数量"),
                        Item('number_of_X',label=u"X数量"),
                        Item('number_of_E',label=u"E数量"),show_border=True,label=u"人口设置"),
                  Group(Item('profit_function',label=u"收益函数f(s)"),
                        Item('endowment_effect',label=u"禀赋效应（α）"),
                        Item('battle_cost',label=u"战斗成本（c）"),
                        Item('resource_rate',label=u"资源比例（g）"),
                        show_border=True,label=u"博弈参数设置"),
                  Group(Item('n',label=u"仿真代数（N）"),
                        Item('m',label=u"重复轮次（n）"),
                        Item('selection_strength',label=u"选择强度（ω）"),
                        Item('imitate_rate',label=u"变异率(μ)"),show_border=True,label=u"演化环境设置"),
                  Group(Item('batch_mode',label="batch mode"),show_border=True,label=u"观察者模式设置") 
                
                     
             ),buttons=["OK"],width=280,height=480,title=u"产权演化参数设置")
