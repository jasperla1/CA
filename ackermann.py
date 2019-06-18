# -*- coding: utf-8 -*-
"""
Created on Tue May 21 11:01:12 2019

@author: thoma
"""

a,b = input().split()
a=int(a)
b=int(b)

def ackermann(x,y):
    if x==0:
        return y+1
    elif x>0 and y==0:
        return ackermann(x-1,1)
    else:
        return ackermann(x-1,ackermann(x,y-1))
    
print(ackermann(a,b))