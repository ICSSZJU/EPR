# -*- coding: utf-8 -*-
"""
This work is licensed under the Creative Commons 
Attribution-NonCommercial-ShareAlike 3.0 Unported 
License. To view a copy of this license, visit 
http://creativecommons.org/licenses/by-nc-sa/3.0/.

Design:Chen Shu & Zhang Hong
Programming:Zhang Hong
"""

import os
import datetime


class datacollector(object):
    
    def __init__(self,data_gen,sum,n,traits):
        self.data_gen=data_gen()
        self.traits=traits
        self.curd=os.path.abspath(os.curdir)
        curt=datetime.datetime.now()
        self.dname=str(curt.year)+str(curt.month)+str(curt.day)+str(curt.minute)+str(curt.second)
        self.datad=self.curd+'\\'+self.dname
        os.mkdir(self.datad)
        
    def write_data(self):
        with open(self.datad+r'\data.csv','w') as f:
            f.write("generation,Bamount,Xamount,Eamount,battlerob,g1,g2,g3,s1,s2,s3,fitB,fitX,fitE\n")
            for d,b,i,g,s,fit in self.data_gen:
                f.write(str(i+1)+","+str(d[0])+","+str(d[1])+","+str(d[2])+","+str(b)+","+str(g[0])+","+str(g[1])+","+str(g[2])+","+str(s[0])+","+str(s[1])+","+str(s[2])+","+str(fit[0])+","+str(fit[1])+","+str(fit[2])+"\n")
            
        
    def show(self):
        f=open(self.datad+"\plot.py","w")
        script='''import pandas as pd
import matplotlib.pyplot as plt
data=pd.read_csv("data.csv")

ax=plt.subplot2grid((6,1), (0, 0), rowspan=3)
bx=plt.subplot2grid((6,1), (4, 0), rowspan=2)
data["battlerob"].plot(ax=bx,title="Battle count")
amount=data[["Bamount","Xamount","Eamount"]]
amount=amount/float(amount.ix[0].sum())
lines=ax.plot(amount)
amount.plot(ax=ax,title="The evolution of property rights")
ax.set_ylim(top=1.0)

box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])
ax.set_xlabel("Generation",fontsize=14)
ax.set_ylabel("Percentage",fontsize=14)
bx.set_xlabel("Generation",fontsize=14)
bx.set_ylabel("Battle",fontsize=14)
ax.legend(lines,["B Percentage","X Percentage","E Percentage"],loc='upper center', bbox_to_anchor=(0.5, -0.2),
          fancybox=True, ncol=3)
plt.show()
                    '''
            
        f.write(script)
        f.close()
        f=open(self.datad+"\parameters.txt","w")
        
        for key,value in self.traits.items():
            if key!="__traits_version__":
                f.write(key+"="+str(value)+"\n")
        f.close()      
        self.write_data()
        exec(script.replace("data.csv",self.dname+"\\"+"data.csv"))
        print "done!"
       
