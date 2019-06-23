#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 12:01:28 2019

@author: jasperlammers
"""

import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy

class General_CA:
    def __init__(self):
        self.cells = [[]]
        self.cell_columns = 50
        self.cell_rows = 50
        self.states = 2
        self.initialconditions = 'dirichlet0' #periodic, dirichlet0, dirichlet1
        self.neighbours = 'square' #1d->(one,two) 2d->(square,hexagon,square2)
        self.born = [3]
        self.upgrade = []
        self.lives = [2,3]
        self.colormap = 'hot' #hot, greys
        self.interpolation = 'none' #bilinear

"""
------------------------------------------------------------------------------------
------------------------------------------------------------------------------------
----------------------------------One Dim--------------------------------------
------------------------------------------------------------------------------------
------------------------------------------------------------------------------------
"""

class One_Dim(General_CA):
#---------------------------Generate cells-------------------------------------
    def Generate_Cells(self):
        self.cells = [[0]*self.cell_columns]
    
    def Generate_Random_Cells(self,percentage):
        self.Generate_Cells()
        for i in range(self.cell_columns):
            if rnd.random() < percentage: #Gives cell on position i value 1 if random number is lower than percentage
                self.cells[0][i] = 1
            
    def Generate_Middle_Cells(self):
        self.Generate_Cells()
        self.cells[0][self.cell_columns//2] = 1
    
#-------------------------------Rule-------------------------------------------
    def Temp_Cells_One(self):
        temp_cells = self.cells[-1].copy()
        
        if self.initialconditions == 'periodic':
            temp_cells.insert(0,temp_cells[-1])
            temp_cells.append(temp_cells[1])
        
        elif self.initialconditions ==  'dirichlet0':
            temp_cells.insert(0,0)
            temp_cells.append(0)
            
        elif self.initialconditions ==  'dirichlet1':
            temp_cells.insert(0,1)
            temp_cells.append(1)
            
        return temp_cells
    
    
    def Temp_Cells_Two(self):
        temp_cells = [[],[]]
        try:
            temp_cells[0] = copy.deepcopy(self.cells[-2])
        except:
            temp_cells[0] = copy.deepcopy(self.cells[-1])
        temp_cells[1] = copy.deepcopy(self.cells[-1])
        
        if self.initialconditions == 'periodic':
            temp_cells[1].insert(0,temp_cells[1][-1])
            temp_cells[1].insert(0,temp_cells[1][-2])
            temp_cells[1].append(temp_cells[1][2])
            temp_cells[1].append(temp_cells[1][3])
            temp_cells[0].insert(0,temp_cells[0][-1])
            temp_cells[0].insert(0,temp_cells[0][-2])
            temp_cells[0].append(temp_cells[0][2])
            temp_cells[0].append(temp_cells[0][3])
        
        elif self.initialconditions ==  'dirichlet0':
            temp_cells[0].insert(0,0)
            temp_cells[0].insert(0,0)
            temp_cells[0].append(0)
            temp_cells[0].append(0)
            temp_cells[1].insert(0,0)
            temp_cells[1].insert(0,0)
            temp_cells[1].append(0)
            temp_cells[1].append(0)
            
        elif self.initialconditions == 'dirichlet1':
            temp_cells[0].insert(0,1)
            temp_cells[0].insert(0,1)
            temp_cells[0].append(1)
            temp_cells[0].append(1)
            temp_cells[1].insert(0,1)
            temp_cells[1].insert(0,1)
            temp_cells[1].append(1)
            temp_cells[1].append(1)
            
        return temp_cells
    
    
    def Rule_One(self,rule):
        value = format(int(rule),'08b')
        
        placing = [[1,1,1],[1,1,0],[1,0,1],[1,0,0],[0,1,1],[0,1,0],[0,0,1],[0,0,0]]
        
        temp_cells = self.Temp_Cells_One()
        new_cells = [0]*self.cell_columns
        
        
        for i in range(1,self.cell_columns+1):
            for j in range(len(value)):
                if [temp_cells[i-1],temp_cells[i],temp_cells[i+1]] == placing[j]:
                    new_cells[i-1] = int(value[j])
                    
        self.cells.append(new_cells)
        
        
    def Rule_Two(self,rule):
        value = format(int(rule),'11b')[::-1]
        
        
        temp_cells = self.Temp_Cells_Two()
        new_cells = [0]*self.cell_columns
        
        for i in range(2,self.cell_columns+2):
            s = 1
            for j in range(2):
                for k in range(i-2,i+3):
                    if temp_cells[j][k] == 1:
                        s += 1
            try:
                new_cells[i-2] = int(value[-s])
            except: 
                new_cells[i-2] = 0
        self.cells.append(new_cells)        
            
        
    def Update(self,t,rule):
        if self.neighbours == 'one':
            for i in range(t):
                self.Rule_One(rule)
        elif self.neighbours == 'two':
            for i in range(t):
                self.Rule_Two(rule)
        
        
    def Draw(self, t=0):
        if t == 0:
            t = self.cell_columns
        fig = plt.figure()
        im = plt.imshow(self.cells[0:t])
        plt.show()
        
"""
------------------------------------------------------------------------------------
------------------------------------------------------------------------------------
----------------------------------Two Dim--------------------------------------
------------------------------------------------------------------------------------
------------------------------------------------------------------------------------
"""
      
class Two_Dim(General_CA):
    def Generate_Cells(self):
        self.cells[0]=[[0 for i in range(self.cell_columns)] for k in range(self.cell_rows)]
        
    def Generate_Middle_Cells(self):
        self.Generate_Cells()
        self.cells[0][self.cell_rows//2][self.cell_columns//2] = 1
    
    
    def Generate_Random_Cells(self,percent_fill):
        self.Generate_Cells()
        for i in range(self.cell_rows):            
            for p in range(self.cell_colunns):
                if rnd.random() < percent_fill:
                    self.cells[0][i][p] = 1
     

    def Add_Gun(self):
        if self.cell_columns < 39 and self.cell_rows < 20:
            print("grid is to small")
        else:
            startx = rnd.randint(0,self.cell_rows-12)
            starty = rnd.randint(0,self.cell_columns-39)
            self.cells[0][startx + 5][starty + 1] = 1
            self.cells[0][startx + 5][starty + 2] = 1
            self.cells[0][startx + 6][starty + 1] = 1
            self.cells[0][startx + 6][starty + 2] = 1
            
            self.cells[0][startx + 5][starty + 11] = 1
            self.cells[0][startx + 6][starty + 11] = 1
            self.cells[0][startx + 7][starty + 11] = 1
            
            self.cells[0][startx + 4][starty + 12] = 1
            self.cells[0][startx + 8][starty + 12] = 1
            
            self.cells[0][startx + 3][starty + 13] = 1
            self.cells[0][startx + 9][starty + 13] = 1
            self.cells[0][startx + 3][starty + 14] = 1
            self.cells[0][startx + 9][starty + 14] = 1
            
            self.cells[0][startx + 6][starty + 15] = 1
            
            self.cells[0][startx + 4][starty + 16] = 1
            self.cells[0][startx + 8][starty + 16] = 1
            
            self.cells[0][startx + 5][starty + 17] = 1
            self.cells[0][startx + 6][starty + 17] = 1
            self.cells[0][startx + 7][starty + 17] = 1
            
            self.cells[0][startx + 6][starty + 18] = 1
            
            self.cells[0][startx + 3][starty + 21] = 1
            self.cells[0][startx + 4][starty + 21] = 1
            self.cells[0][startx + 5][starty + 21] = 1
            
            self.cells[0][startx + 3][starty + 22] = 1
            self.cells[0][startx + 4][starty + 22] = 1
            self.cells[0][startx + 5][starty + 22] = 1
            
            self.cells[0][startx + 2][starty + 23] = 1
            self.cells[0][startx + 6][starty + 23] = 1
            
            self.cells[0][startx + 1][starty + 25] = 1
            self.cells[0][startx + 2][starty + 25] = 1
            self.cells[0][startx + 6][starty + 25] = 1
            self.cells[0][startx + 7][starty + 25] = 1
            
            self.cells[0][startx + 3][starty + 35] = 1
            self.cells[0][startx + 4][starty + 35] = 1
            self.cells[0][startx + 3][starty + 36] = 1
            self.cells[0][startx + 4][starty + 36] = 1
            
            
            
    def Temp_Cells(self):
        if self.initialconditions == 'periodic':
            
            temp_cells = copy.deepcopy(self.cells[-1])
            copy_cells = copy.deepcopy(self.cells[-1])
            
            x = copy_cells[0].copy()
            y = copy_cells[self.cell_rows-1].copy()
            
            temp_cells.append(x)
            temp_cells.insert(0,y)
            
            temp_cells[0].append(copy_cells[self.cell_rows-1][0])
            temp_cells[0].insert(0,copy_cells[self.cell_rows-1][self.cell_columns-1])
            temp_cells[self.cell_rows+1].append(copy_cells[0][0])
            temp_cells[self.cell_rows+1].insert(0,copy_cells[0][self.cell.columns-1])
            
            for i in range(1,self.cell_rows+1):
                temp_cells[i].append(copy_cells[i-1][0])
                temp_cells[i].insert(0,copy_cells[i-1][self.cell_columns-1])
            
            
        
        elif self.initialconditions == 'dirichlet0':
            
            temp_cells = copy.deepcopy(self.cells[-1])
            
            for i in range(self.cell_rows):
                temp_cells[i].append(0)
                temp_cells[i].insert(0,0)
                
            temp_cells.append([0]*(self.cell_columns+2))
            temp_cells.insert(0,[0]*(self.cell_columns+2))
            
            
        elif self.initialconditions == 'dirichlet1':
            
            temp_cells = copy.deepcopy(self.cells[-1])
            
            for i in range(self.cell_rows):
                temp_cells[i].append(1)
                temp_cells[i].insert(0,1)
                
            temp_cells.append([1]*(self.cell_columns+2))
            temp_cells.insert(0,[1]*(self.cell_columns+2))
            
        return temp_cells


    def Rule(self):
        new_cells = [[0 for j in range(self.cell_columns)] for i in range(self.cell_rows)]
        temp = self.Temp_Cells()
        
        
        if self.neighbours == 'hexagon':
            for i in range(1,self.cell_rows+1):
                for j in range(1,self.cell_columns+1):               
                    s = 0
                    s += temp[i-1][j]
                    s += temp[i-1][j+1] 
                    s += temp[i][j-1]
                    s += temp[i][j+1]
                    s += temp[i+1][j-1]
                    s += temp[i+1][j]
    
                    
                    if temp[i][j] == 0 and s in self.born:
                        new_cells[i-1][j-1] = 1
                    elif temp[i][j] > 0 and temp[i][j] < self.states-1 and s in self.upgrade:
                        new_cells[i-1][j-1] = temp[i][j] + 1
                    elif temp[i][j] > 0 and temp[i][j] < self.states-1 and s in self.lives:
                        new_cells[i-1][j-1] = temp[i][j]
                    elif temp[i][j] == self.states-1 and s in self.lives:
                        new_cells[i-1][j-1] = temp[i][j]
                        
        
        elif self.neighbours == 'square':
            for i in range(1,self.cell_rows+1):
                for j in range(1,self.cell_columns+1):               
                    s = 0
                    s += temp[i-1][j-1]
                    s += temp[i-1][j]
                    s += temp[i-1][j+1] 
                    s += temp[i][j-1]
                    s += temp[i][j+1]
                    s += temp[i+1][j-1]
                    s += temp[i+1][j]
                    s += temp[i+1][j+1] 
    
                    
                    if temp[i][j] == 0 and s in self.born:
                        new_cells[i-1][j-1] = 1
                    elif temp[i][j] > 0 and temp[i][j] < self.states-1 and s in self.upgrade:
                        new_cells[i-1][j-1] = temp[i][j] + 1
                    elif temp[i][j] > 0 and temp[i][j] < self.states-1 and s in self.lives:
                        new_cells[i-1][j-1] = temp[i][j]
                    elif temp[i][j] == self.states-1 and s in self.lives:
                        new_cells[i-1][j-1] = temp[i][j]
                        
        elif self.neighbours == 'beehive':
            m = [[0,1,2,1,2,0,0],[0,2,2,2,1,1],[0,0,2,2,0],[0,2,2,0],[0,0,2],[2,0],[0]]
            self.states = 3
            for i in range(1,self.cell_rows+1):
                for j in range(1,self.cell_columns+1):               
                    een = 0
                    twee = 0 
                    if temp[i-1][j-1] == 1 :
                        een += 1 
                    elif temp[i-1][j-1] == 2 :
                        twee += 1
                    if temp[i-1][j] == 1 :
                        een += 1 
                    elif temp[i-1][j] == 2 :
                        twee += 1
                    if temp[i][j-1] == 1 :
                        een += 1 
                    elif temp[i][j-1] == 2 :
                        twee += 1 
                    if temp[i][j+1] == 1 :
                        een += 1 
                    elif temp[i][j+1] == 2 :
                        twee += 1 
                    if temp[i+1][j] == 1 :
                        een += 1 
                    elif temp[i+1][j] == 2 :
                        twee += 1 
                    if temp[i+1][j+1] == 1 :
                        een += 1 
                    elif temp[i+1][j+1] == 2 :
                        twee += 1
                    
                    new_cells[i-1][j-1] = m[twee][een]
                    
                    
        self.cells.append(new_cells)

    
    def Update(self,t):
        for i in range(t):
            self.Rule()
            
        
    def Draw(self, t = -1):
        fig = plt.figure()
        im = plt.imshow(self.cells[t], cmap = self.colormap, interpolation = self.interpolation)
        plt.show()
        
        
    def Animation(self,nfr,fps):
        fig = plt.figure()
        data = np.array(self.cells[0])
        lsquare = plt.imshow(data,cmap = self.colormap, interpolation = self.interpolation )
        temp = self
        norm = plt.Normalize(vmin=0, vmax=self.states-1)
        
        def init():
            data = np.array(temp.cells[0])
            lsquare.set_data(data)
            return [lsquare]
        
        def animate(i):
            
            data = np.array(temp.cells[i])
            
            lsquare.set_array(data)
            lsquare.set_norm(norm)
            return [lsquare]
        
        
        anim = animation.FuncAnimation(fig, animate, frames = nfr, blit=False, interval=1000/fps, init_func=init, repeat=True)
        return anim
        
"""
------------------------------------------------------------------------------------
------------------------------------------------------------------------------------
----------------------------------Test cases--------------------------------------
------------------------------------------------------------------------------------
------------------------------------------------------------------------------------
"""

test = Two_Dim()
test.Generate_Cells()
test.states = 3
test.neighbours = 'beehive'
test.cells[0][test.cell_rows//2][test.cell_columns//2] = 1
#test.Add_Gun()
test.Update(8)
x = test.Animation(9,1)




    
