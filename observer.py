# -*- coding: utf-8 -*-
"""
This work is licensed under the Creative Commons 
Attribution-NonCommercial-ShareAlike 3.0 Unported 
License. To view a copy of this license, visit 
http://creativecommons.org/licenses/by-nc-sa/3.0/.

Design:Chen Shu & Zhang Hong
Programming:Zhang Hong
"""
import datacollector
import plotter
class observer(object):
    def __init__(self,data_gen,sum,n,traits,batchmode=True):
        if batchmode:
            self.dataviewer=datacollector.datacollector(data_gen,sum,n,traits)
        else: 
            self.dataviewer=plotter.plotter(data_gen,sum,n,traits)
            
    def start(self):
        self.dataviewer.show()