#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 11:10:51 2019

@author: jasperlammers
"""


import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class GeneralCA:
    """
    nneighbors -> hexagon(6),square(8),line(2)
    initialconditions -> periodic, Dirichlet, Neumann
    ruleset -> game_of_life, rule_30, rule_34/2
    """
    def __init__(self, n, nneighbors, initialconditions):
        self.n = n
        self.nneighbors = nneighbors
        self.initialconditions = initialconditions 
        self.cells = []
        self.ims = []
        
        
    def update(self,t,rule):
        func = getattr(self,rule)
        for i in range(t):
            func()
"""    
class square(GeneralCA):
    def generate_cells(self,percent_fill):
        N = int(np.sqrt(self.n))
        for i in range(N):
            [
            for p in range(N):
                if rnd.random() < percent_fill:
                    i
            ]
"""        
        
class line(GeneralCA):
    def generate_cells(self,percent_fill):
        self.cells = [[]]
        for cel in range(self.n):
            if rnd.random() < percent_fill:
                self.cells[0].append(1)
            else:
                self.cells[0].append(0)
    
    def generate_middle(self):
        self.cells = [[0]*self.n]
        self.cells[0][self.n//2] = 1
    
    
    def rule30(self):
        temp_cells = self.cells[-1].copy()
        for i in range(1,self.n -1):

            if [self.cells[-1][i-1],self.cells[-1][i],self.cells[-1][i+1]] == [1,1,1]:

                temp_cells[i] = 0
            elif [self.cells[-1][i-1],self.cells[-1][i],self.cells[-1][i+1]] == [1,1,0]:
                temp_cells[i] = 0

            elif [self.cells[-1][i-1],self.cells[-1][i],self.cells[-1][i+1]] == [1,0,1]:
                temp_cells[i] = 0

            elif [self.cells[-1][i-1],self.cells[-1][i],self.cells[-1][i+1]] == [1,0,0]:
                temp_cells[i] = 1

            elif [self.cells[-1][i-1],self.cells[-1][i],self.cells[-1][i+1]] == [0,1,1]:
                temp_cells[i] = 1

            elif [self.cells[-1][i-1],self.cells[-1][i],self.cells[-1][i+1]] == [0,1,0]:
                temp_cells[i] = 1

            elif [self.cells[-1][i-1],self.cells[-1][i],self.cells[-1][i+1]] == [0,0,1]:
                temp_cells[i] = 1

            elif [self.cells[-1][i-1],self.cells[-1][i],self.cells[-1][i+1]] == [0,0,0]:
                temp_cells[i] = 0
        self.cells.append(temp_cells)
        
    def draw(self, t=-1):
        fig = plt.figure()
        im = plt.imshow(self.cells[0:t])
        plt.show()
        
"""
test = line(43,2,2)
test.generate_middle()
test.update(20,'rule30')
test.draw()

#for i in range(20):
#    test.rule30()
#plt.imshow(test.cells)


"""                
"""
def generate_cells(self):
        for row in range(0, self.grid_height):
            self.cells.append([])
            for col in range(0, self.grid_width):
                if rnd.random() < self.percent_fill:
                    self.cells[row].append(1)
                else:
                    self.cells[row].append(0)
"""


class Test1:
    def __init__(self,n,string):
        self.n = n
    
    def plus(self,p,q):
        
        return self.n+q
    
    def twee(self):
        self.n = 15


class Test2(Test1):
    def twee(self):
        self.n = 16 