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
        self.cells = [[]] #list with nested lists, every nested list is 1 timestep of the CA
        self.cell_columns = 50 #number of cell columns
        self.cell_rows = 50 #number of cell rows
        self.states = 2 #number of states that a cell can have 
        self.boundary_conditions = 'dirichlet0' #periodic, dirichlet0 (default), dirichlet1
        self.neighbours = 'square' #1d->(one,two) 2d->(square,hexagon,beehive,honeycomb,triangle)
        self.born = [3] #Total value of the neighbours surrounding a cell that 'gives the cell life' 
        #(for instance, if the cell has two neighbours of state 2 and one of state 1 then the combined value is 5)
        self.upgrade = []#Total value of the neighbours surrounding a cell that 'upgrades the cell'
        self.lives = [2,3] #Total value of the neighbours surrounding a cell that 'lets the cell live'
        #attributes for visualization:
        self.colormap = 'inferno' #color map of the plot, possible values -> (hot, Greys, https://matplotlib.org/examples/color/colormaps_reference.html)
        self.interpolation = 'none' #possible values -> (none, bilinear)



"""
------------------------------------------------------------------------------------
------------------------------------------------------------------------------------
----------------------------------One Dim--------------------------------------
------------------------------------------------------------------------------------
------------------------------------------------------------------------------------
"""

class One_Dim(General_CA):
#---------------------------Generate cells-------------------------------------
    def Generate_Cells(self): #Function to generate cells of state 0
        self.cells = [[0]*self.cell_columns] #Generates list of cells with state 0 for 1 row and n columns
        
    def Generate_Random_Cells(self,percentage): #Function to generate cells of state 0
        try: #to prevent error if percentage variable is not a float
            if percentage >= 0 and percentage <= 1: #make sure percentage is between 0.0 and 1.0
                self.Generate_Cells() #generate list with as many zeroes as columns
                for i in range(self.cell_columns): #for every place in the list
                    if rnd.random() < percentage: #Gives cell on position i value 1 if random number is lower than percentage
                        self.cells[0][i] = 1
            else: 
                print("percentage needs to be a number between 0 - 1") #print error and exit function
                exit
        except:
            print("percentage needs to be a number between 0 - 1") #print error and exit function
            exit
    def Generate_Middle_Cells(self): #Function to generate cells of state 0 and only the middle cell state 1
        self.Generate_Cells() #generate list with 0's
        self.cells[0][self.cell_columns//2] = 1 #middle cell 1
    
    def Generate_Self_Cells(self): #Function to give own cell input
      self.cells = [input().split()] #give input for the cells with entries separated by whitespaces, e.g. 1 0 0 1 1 0
        self.cell_columns = len(self.cells[0]) #number of columns is length of first element of nested list
        for i in range(self.cell_columns):
            self.cells[0][i] = int(self.cells[0][i]) #convert string elements to integers
            
            
#-------------------------------Rule-------------------------------------------
    def Temp_Cells_One(self): #used for evolving to next timestep in the case where we only consider the last timesteps: make an auxiliary list and append the boundary conditions to it
        temp_cells = self.cells[-1].copy() #copy of most recently performed timestep
        
        if self.boundary_conditions == 'periodic': 
            temp_cells.insert(0,temp_cells[-1]) #for periodic boundary conditions, insert last element of the list at the beginning...
            temp_cells.append(temp_cells[1]) #and the first element at the end
        
        elif self.boundary_conditions ==  'dirichlet0': #for dirichlet0, insert zeroes at both ends
            temp_cells.insert(0,0) 
            temp_cells.append(0)
            
        elif self.boundary_conditions ==  'dirichlet1': #for dirichlet1, insert ones at both ends
            temp_cells.insert(0,1)
            temp_cells.append(1)
        else: 
            print("Give correct initial conditions") #appropriate error code in case of unknown initial conditions
            exit
        return temp_cells
    
    
    def Temp_Cells_Two(self): #used for evolving to next timestep in the case of two previous timesteps and two neighbors 
        temp_cells = [[],[]]
        try:
            temp_cells[0] = copy.deepcopy(self.cells[-2]) #does not work if we have not performed the first step yet
        except:
            temp_cells[0] = copy.deepcopy(self.cells[-1]) #in this case, take initial condition and first step to be equal
        temp_cells[1] = copy.deepcopy(self.cells[-1])
        
        if self.boundary_conditions == 'periodic': #insert periodic boundary conditions for both lists
            temp_cells[1].insert(0,temp_cells[1][-1])
            temp_cells[1].insert(0,temp_cells[1][-2])
            temp_cells[1].append(temp_cells[1][2])
            temp_cells[1].append(temp_cells[1][3])
            temp_cells[0].insert(0,temp_cells[0][-1])
            temp_cells[0].insert(0,temp_cells[0][-2])
            temp_cells[0].append(temp_cells[0][2])
            temp_cells[0].append(temp_cells[0][3])
        
        elif self.boundary_conditions ==  'dirichlet0': #insert dirichlet condition with zeroes
            temp_cells[0].insert(0,0)
            temp_cells[0].insert(0,0)
            temp_cells[0].append(0)
            temp_cells[0].append(0)
            temp_cells[1].insert(0,0)
            temp_cells[1].insert(0,0)
            temp_cells[1].append(0)
            temp_cells[1].append(0)
            
        elif self.boundary_conditions == 'dirichlet1': #insert dirichlet with ones
            temp_cells[0].insert(0,1)
            temp_cells[0].insert(0,1)
            temp_cells[0].append(1)
            temp_cells[0].append(1)
            temp_cells[1].insert(0,1)
            temp_cells[1].insert(0,1)
            temp_cells[1].append(1)
            temp_cells[1].append(1)
        
        else: 
            print("Give correct initial conditions") #usual error code
            exit
            
        return temp_cells
    
    
    def Rule_One(self,rule): #used for evolving in case of one previous timestep
        value = format(int(rule),'08b') #converts the rule nnumber to an 8-digit binary representation and formats this string
        
        placing = [[1,1,1],[1,1,0],[1,0,1],[1,0,0],[0,1,1],[0,1,0],[0,0,1],[0,0,0]] #all possible neighbor combinations
        
        temp_cells = self.Temp_Cells_One() #create boundary conditions 
        new_cells = [0]*self.cell_columns #initiate list for the states at the next timestep
        
        
        for i in range(1,self.cell_columns+1): #use rule to decide what the state of each cell is at the next timestep
            for j in range(len(value)):
                if [temp_cells[i-1],temp_cells[i],temp_cells[i+1]] == placing[j]:
                    new_cells[i-1] = int(value[j])
                    
        self.cells.append(new_cells) #add next timestep to the full list
        
        
    def Rule_Two(self,rule): #next timestep in the case of two previous timesteps and two neighbors
        value = format(int(rule),'11b')[::-1] #now make an 11-digit binary string from the rule
        
        
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
            
        
    def Update(self,t,rule): #evolve the automaton up to timestep t according to a given rule (number)
        if self.neighbours == 'one': #for one neighbor, look at one previous timestep
            for i in range(t):
                self.Rule_One(rule)
        elif self.neighbours == 'two': #for two neighbors, look at two previous timesteps
            for i in range(t):
                self.Rule_Two(rule)
        
        
    def Draw(self, t=0): #draws all timesteps at once, i.e. first row is the initial condition, row i is the timestep i configuration
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
      
class Two_Dim(General_CA): #subclass with parent class general 
    def Generate_Cells(self): #initial state is now a matrix, i.e. nested list 
        self.cells[0]=[[0 for i in range(self.cell_columns)] for k in range(self.cell_rows)] #initiate with dead cells only
        
    def Generate_Middle_Cells(self): #middle element of the matrix
        self.Generate_Cells()
        self.cells[0][self.cell_rows//2][self.cell_columns//2] = 1
    
    
    def Generate_Random_Cells(self,percent_fill): #can also take a random initial state with percentage percent_fill of live cells
        self.Generate_Cells()
        for i in range(self.cell_rows):            
            for p in range(self.cell_columns):
                if rnd.random() < percent_fill:
                    self.cells[0][i][p] = 1
                    
    def Generate_Random_Part_Cells(self,percent_fill,colls,rows): #performs the random initial state procedure on a block of given width and length in the center of the matrix
        self.Generate_Cells()
        if colls < self.cell_columns and rows < self.cell_rows:
            r = (self.cell_rows - rows)//2
            c = (self.cell_columns - colls)//2
            for i in range(r,rows+r):            
                for p in range(c,colls+c):
                    if rnd.random() < percent_fill:
                        self.cells[0][i][p] = 1
        else:
            print('filling area must be smaller than total grid') #error code if block is bigger than size of matrix
            
            
    def Generate_Self_Cells(self): #this function allows one to manually put in the initial conditions if needed 
        print('Columns:')
        self.cell_columns = int(input()) #what number of columns?
        print('Rows:')
        self.cell_rows = int(input()) #what number of rows?
        self.cells = [[]]
        for i in range(self.cell_rows): #input is taken row by row where elements of the row are separated by commas
            print('Row ',i+1)
            self.cells[0].append(input().split())
            
        for i in range(self.cell_rows):
            for j in range(self.cell_columns):
                self.cells[0][i][j] = int(self.cells[0][i][j])
                

    def Add_Gun(self): #add a glider gun if the grid is big enough
        if self.cell_columns < 39 and self.cell_rows < 20: #error code if grid is not big enough
            print("grid is to small")
        else: #initial conditions for glider gun
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
            
            
            
    def Temp_Cells(self): #as in 1D case, temp_cells appends boundary conditions to the last element of the entire list of timesteps
        if self.boundary_conditions == 'periodic': #periodic boundary conditions
            
            temp_cells = copy.deepcopy(self.cells[-1]) #deepcopy: we are dealing with a nested list unlike in the 1d case
            copy_cells = copy.deepcopy(self.cells[-1])
            
            x = copy_cells[0].copy() #first row of last configuration
            y = copy_cells[self.cell_rows-1].copy() #last row of last configuration
            
            temp_cells.append(x) #first row of last configuration are neighbors of the last row, so need to append it at the end (on the bottom)
            temp_cells.insert(0,y) #last row of last configuration are neighbors of the first row, so insert at the beginning (at the top)
           
            #below we also append the rightmost column on the left and the leftmost column on the right
            temp_cells[0].append(copy_cells[self.cell_rows-1][0]) 
            temp_cells[0].insert(0,copy_cells[self.cell_rows-1][self.cell_columns-1])
            temp_cells[self.cell_rows+1].append(copy_cells[0][0])
            temp_cells[self.cell_rows+1].insert(0,copy_cells[0][self.cell_columns-1])
            
            for i in range(1,self.cell_rows+1):
                temp_cells[i].append(copy_cells[i-1][0])
                temp_cells[i].insert(0,copy_cells[i-1][self.cell_columns-1])
            
            
        
        elif self.boundary_conditions == 'dirichlet0': #dirichlet0 boundary condition
            
            temp_cells = copy.deepcopy(self.cells[-1])
            
            for i in range(self.cell_rows): #put zeroes at beginning and end of each row
                temp_cells[i].append(0)
                temp_cells[i].insert(0,0)
                
            temp_cells.append([0]*(self.cell_columns+2)) #add a row of zeroes at the end (bottom)
            temp_cells.insert(0,[0]*(self.cell_columns+2)) #add a row of zeroes at the beginning (on top)
            
            
        elif self.boundary_conditions == 'dirichlet1': #completely analogous to dirichlet0
            
            temp_cells = copy.deepcopy(self.cells[-1])
            
            for i in range(self.cell_rows):
                temp_cells[i].append(1)
                temp_cells[i].insert(0,1)
                
            temp_cells.append([1]*(self.cell_columns+2))
            temp_cells.insert(0,[1]*(self.cell_columns+2))
        else: 
            print("Give correct initial conditions")
            exit
        
        return temp_cells


    def Rule(self): #as in 1D case, apply rule to create a new timestep. We distinguish between a few different rules as below
        new_cells = [[0 for j in range(self.cell_columns)] for i in range(self.cell_rows)] #initiate new timestep as dead configuration
        temp = self.Temp_Cells()
        
        
        if self.neighbours == 'hexagon': #hexagonal lattice: works for general number of states per cell
            for i in range(1,self.cell_rows+1):
                for j in range(1,self.cell_columns+1):  #for each cell, count total 'score' of neighboring cells             
                    s = 0
                    s += temp[i-1][j]
                    s += temp[i-1][j+1] 
                    s += temp[i][j-1]
                    s += temp[i][j+1]
                    s += temp[i+1][j-1]
                    s += temp[i+1][j]
    
                    
                    if temp[i][j] == 0 and s in self.born: #if cell dead and s in born, cell becomes alive
                        new_cells[i-1][j-1] = 1
                    elif temp[i][j] > 0 and temp[i][j] < self.states-1 and s in self.upgrade: #if cell alive but not in highest state and s in upgrade, state is incremented by 1
                        new_cells[i-1][j-1] = temp[i][j] + 1
                    elif temp[i][j] > 0 and temp[i][j] < self.states-1 and s in self.lives: 
                        new_cells[i-1][j-1] = temp[i][j]
                    elif temp[i][j] == self.states-1 and s in self.lives:
                        new_cells[i-1][j-1] = temp[i][j]
                    #if cell dead and s not in born, cell remains dead (all if statements are false)
                        
        
        elif self.neighbours == 'square': #rule for a general square lattice
            for i in range(1,self.cell_rows+1):
                for j in range(1,self.cell_columns+1): #count total 'score' of the neighboring cells (number of states is general)             
                    s = 0
                    s += temp[i-1][j-1]
                    s += temp[i-1][j]
                    s += temp[i-1][j+1] 
                    s += temp[i][j-1]
                    s += temp[i][j+1]
                    s += temp[i+1][j-1]
                    s += temp[i+1][j]
                    s += temp[i+1][j+1] 
    
                    
                    if temp[i][j] == 0 and s in self.born: #if cell is dead and s in born, then cell becomes alive
                        new_cells[i-1][j-1] = 1
                    elif temp[i][j] > 0 and temp[i][j] < self.states-1 and s in self.upgrade: #if cell already alive and not equal to largest possible value and s in upgrade, then increment by 1
                        new_cells[i-1][j-1] = temp[i][j] + 1
                    elif temp[i][j] > 0 and temp[i][j] < self.states-1 and s in self.lives: #if as above but s not in upgrade, then cell does not change state
                        new_cells[i-1][j-1] = temp[i][j]
                    elif temp[i][j] == self.states-1 and s in self.lives: 
                        new_cells[i-1][j-1] = temp[i][j]
                    #note: if cell dead and s not in born, then none of the if statements is true and cell remains dead
                        
        elif self.neighbours == 'beehive': #beehive lattice structure
            m = [[0,1,2,1,2,0,0],[0,2,2,2,1,1],[0,0,2,2,0],[0,2,2,0],[0,0,2],[2,0],[0]] #triangle matrix representing the beehive rule
            self.states = 3 #the beehive rule only applies to 3-state automata
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
                    
        elif self.neighbours == 'honeycomb': #honeycomb lattice with rule
            self.states = 2 #this rule only applies to two states

            for j in range(1,self.cell_rows+1):
                for k in range(1, self.cell_columns+1):
                    o = 0 #ortho-neighbours
                    m = 0 #meta-neighbours
                    g = 0 #ortho- or meta-neighbours
                    if temp[j-1][k-1] == 1:
                        o += 1
                        g += 1
                    if temp[j-1][k] == 1:
                        o += 1
                        g += 1
                    if temp[j][k-1] == 1:
                        o += 1
                        m += 1
                        g += 1
                    if temp[j][k+1] == 1:
                        o += 1
                        m += 1
                        g += 1
                    if temp[j+1][k] == 1:
                        m += 1
                        g += 1
                    if temp[j+1][k+1] == 1:
                        m += 1
                        g += 1
                    
                    if (temp[j][k] == 1 and (o == 2 or m == 3 or g == 4)) or (temp[j][k] == 0 and g == 2):
                        new_cells[j-1][k-1] = 1
            
            
        else: 
            print("Give correct neighbourhood") #error code if neighborhood is not recognized
            exit            
                    
        self.cells.append(new_cells) #append the newly created timestep


    
    def Update(self,t):
        for i in range(t):
            self.Rule()
            
        
    def Draw(self, t = -1): #draws the final element of the nested list, i.e. the last computed configuration / timestep
        fig = plt.figure()
        im = plt.imshow(self.cells[t], cmap = self.colormap, interpolation = self.interpolation) #use possible values of the visualization attributes
        plt.show() #show plot as printed output
        
        
    def Animation(self,nfr,fps): #show the evolution for a given number of frames nfr at a given rate fps
        fig = plt.figure()
        data = np.array(self.cells[0]) #initialize data as initial state first
        lsquare = plt.imshow(data,cmap = self.colormap, interpolation = self.interpolation )
        temp = self
        norm = plt.Normalize(vmin=0, vmax=self.states-1) #normalize the color plot
        
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
"""
test = Two_Dim()
test.cell_columns = 200
test.cell_rows = 200
test.Generate_Random_Cells(0.15)
test.neighbours = 'honeycomb'
#test.cells[0][test.cell_rows//2][test.cell_columns//2] = 1
#test.Add_Gun() #GOL
test.Update(500)
x = test.Animation(500,30)
"""




    
