# -*- coding: utf-8 -*-
"""
This work is licensed under the Creative Commons 
Attribution-NonCommercial-ShareAlike 3.0 Unported 
License. To view a copy of this license, visit 
http://creativecommons.org/licenses/by-nc-sa/3.0/.

Design:Chen Shu & Zhang Hong
Programming:Zhang Hong
"""

import matplotlib.pyplot as plt

import matplotlib.animation as animation

class plotter(object):
    def __init__(self,gen,sum,iter,traits):
          
        self.fig=plt.figure()
        self.ax=self.fig.add_subplot(1,1,1,title="The evolution of property rights")

        self.ax.set_ylim(0,1)
        self.ax.set_xlim(0,iter)
        self.x=[]
        self.Bdata=[]
        self.Xdata=[]
        self.Edata=[]
        self.ax.set_xlabel("Generation",fontsize=14)
        self.ax.set_ylabel("Percentage",fontsize=14)
        box = self.ax.get_position()
        self.ax.set_position([box.x0, box.y0 + box.height * 0.3,
                 box.width, box.height * 0.6])
        self.lines=self.ax.plot(self.x,self.Bdata,self.x,self.Xdata,self.x,self.Edata) 
        self.ax.legend(self.lines,["B Percentage","X Percentage","E Percentage"],loc='upper center', bbox_to_anchor=(0.5, -0.2),
          fancybox=True, ncol=3)    
        self.gen=gen
        
    def animate(self,data):

        d,p,j,g,s,f=data
        self.x.append(j)
        
        B,X,E=d
        total=B+X+E
        self.Bdata.append(float(B)/total)
        self.Xdata.append(float(X)/total)
        self.Edata.append(float(E)/total)
 

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


