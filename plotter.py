# -*- coding: utf-8 -*-
"""
This work is licensed under the Creative Commons 
Attribution-NonCommercial-ShareAlike 3.0 Unported 
License. To view a copy of this license, visit 
http://creativecommons.org/licenses/by-nc-sa/3.0/.

Design:(Temporary Anonymous) & Zhang Hong
Programming:Zhang Hong
"""

import matplotlib.pyplot as plt

import matplotlib.animation as animation

class plotter(object):
    def __init__(self,gen,sum,iter,traits):
          
        self.fig=plt.figure()
        self.ax=self.fig.add_subplot(2,1,1)

        self.ax.set_ylim(0,sum)
        self.ax.set_xlim(0,iter)

        self.x=[]
        self.Bdata=[]
        self.Xdata=[]
        self.Edata=[]
     
      
        self.lines=self.ax.plot(self.x,self.Bdata,self.x,self.Xdata,self.x,self.Edata)     
        self.gen=gen
        
    def animate(self,data):

        d,p,j,g,s,f=data
        self.x.append(j)
        
        B,X,E=d
        self.Bdata.append(B)
        self.Xdata.append(X)
        self.Edata.append(E)
 

        for line in self.lines:
            line.set_xdata(self.x)
        self.lines[0].set_ydata(self.Bdata)
        self.lines[1].set_ydata(self.Xdata)
        self.lines[2].set_ydata(self.Edata)

        return self.lines
        
    def show(self):
        self.ani = animation.FuncAnimation(self.fig, self.animate, self.gen,
    interval=5, blit=True,repeat=False)
        plt.show()


