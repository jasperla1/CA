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
import copy


"""
------------------------------------------------------------------------------------
------------------------------------------------------------------------------------
----------------------------------Main class----------------------------------------
------------------------------------------------------------------------------------
------------------------------------------------------------------------------------
"""

class GeneralCA:
    """
    nneighbors -> hexagon(6),square(8),line(2)
    initialconditions -> periodic, Dirichlet, Neumann
    ruleset -> game_of_life, rule_30, rule_34/2
    """
    def __init__(self, n, initialconditions):
        self.n = n
        self.initialconditions = initialconditions 
        self.cells = [[]]
        self.ims = []
        self.rule = ''
        
        
        
    def update(self,t,rule):
        if rule == '':
            rule = 'GOL'
        func = getattr(self,rule)
        for i in range(t):
            func()
    

"""
------------------------------------------------------------------------------------
------------------------------------------------------------------------------------
----------------------------------2 dimensional class-------------------------------
------------------------------------------------------------------------------------
------------------------------------------------------------------------------------
"""    
    


    
class square(GeneralCA):
    
#----------------------------------Generate cells-------------------------------------


    def generate_cells(self):
        self.N = self.n
        #self.N = int(np.sqrt(self.n))
        self.cells[0]=[[0 for i in range(self.N)] for k in range(self.N)]
        
        
    def generate_cells_percentage(self,percent_fill):
        self.generate_cells()
        for i in range(self.N):            
            for p in range(self.N):
                if rnd.random() < percent_fill:
                    self.cells[0][i][p] = 1
     

    def add_gun(self):
        if self.n < 39:
            print("grid is to small")
        else:
            startx = rnd.randint(0,self.n-12)
            starty = rnd.randint(0,self.n-39)
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
            
            
            
    def temp_cells(self):
        if self.initialconditions == 'periodic':
            
            temp_cells = copy.deepcopy(self.cells[-1])
            copy_cells = copy.deepcopy(self.cells[-1])
            
            x = copy_cells[0].copy()
            y = copy_cells[self.N-1].copy()
            
            temp_cells.append(x)
            temp_cells.insert(0,y)
            
            temp_cells[0].append(copy_cells[self.N-1][0])
            temp_cells[0].insert(0,copy_cells[self.N-1][self.N-1])
            temp_cells[self.N+1].append(copy_cells[0][0])
            temp_cells[self.N+1].insert(0,copy_cells[0][self.N-1])
            
            for i in range(1,self.N+1):
                temp_cells[i].append(copy_cells[i-1][0])
                temp_cells[i].insert(0,copy_cells[i-1][self.N-1])
            
            
        
        elif self.initialconditions == 'dirichlet0':
            
            temp_cells = copy.deepcopy(self.cells[-1])
            
            for i in range(self.N):
                temp_cells[i].append(0)
                temp_cells[i].insert(0,0)
                
            temp_cells.append([0]*(self.N+2))
            temp_cells.insert(0,[0]*(self.N+2))
            
            
        elif self.initialconditions == 'dirichlet1':
            
            temp_cells = copy.deepcopy(self.cells[-1])
            
            for i in range(self.N):
                temp_cells[i].append(1)
                temp_cells[i].insert(0,1)
                
            temp_cells.append([1]*(self.N+2))
            temp_cells.insert(0,[1]*(self.N+2))
            
        return temp_cells

        
class hexagonal(square):
    
    
     def temp_cells(self):
        if self.initialconditions == 'periodic':
            
            temp_cells = copy.deepcopy(self.cells[-1])
            copy_cells = copy.deepcopy(self.cells[-1])
            
            x = copy_cells[0].copy()
            y = copy_cells[self.N-1].copy()
            
            temp_cells.append(x)
            temp_cells.insert(0,y)
            
            temp_cells[0].insert(0,copy_cells[self.N-1][self.N-1])
            temp_cells[self.N+1].append(copy_cells[0][0])
            
            
            
            for i in range(1,self.N+1):
                temp_cells[i].append(copy_cells[i-1][0])
                temp_cells[i].insert(0,copy_cells[i-1][self.N-1])
            # Ik begrijp deze even niet meer, dus weet ook niet of ik hem aan moet passen voor deze klasse.
            
        
        elif self.initialconditions == 'dirichlet0':
            
            temp_cells = copy.deepcopy(self.cells[-1])
            
            for i in range(self.N):
                temp_cells[i].append(0)
                temp_cells[i].insert(0,0)
                
            temp_cells.append([0]*(self.N+2))
            temp_cells.insert(0,[0]*(self.N+2))
            
            
        elif self.initialconditions == 'dirichlet1':
            
            temp_cells = copy.deepcopy(self.cells[-1])
            
            for i in range(self.N):
                temp_cells[i].append(1)
                temp_cells[i].insert(0,1)
                
            temp_cells.append([1]*(self.N+2))
            temp_cells.insert(0,[1]*(self.N+2))
            
        return temp_cells
            
#----------------------------------Rule sets-----------------------------------------

    def GOL(self):
    
        temp_cells = self.temp_cells()
        
        new_cells = [[0 for i in range(self.N)] for j in range(self.N)]
        for j in range(1,self.N+1):
            for k in range(1,self.N+1):
                s = 0
                if temp_cells[j-1][k-1] == 1:
                    s += 1
                if temp_cells[j-1][k] == 1:
                    s += 1
                if temp_cells[j-1][k+1] == 1:
                    s += 1
                if temp_cells[j][k-1] == 1:
                    s += 1
                if temp_cells[j][k+1] == 1:
                    s += 1
                if temp_cells[j+1][k-1] == 1:
                    s += 1    
                if temp_cells[j+1][k] == 1:
                    s += 1
                if temp_cells[j+1][k+1] == 1:
                    s += 1
                
                if (temp_cells[j][k] == 1 and (s == 2 or s == 3)) or (temp_cells[j][k] == 0 and s == 3):
                    if j < self.N+1 and k < self.N+1:
                        new_cells[j-1][k-1] = 1
                        
        
        self.cells.append(new_cells)

        
    def honeycomb(self):
        
        temp_cells = self.temp_cells()
        
        new_cells = [[0 for i in range(self.N)] for j in range(self.N)] 
        for j in range(1,self.N+1):
            for k in range(1, self.N+1):
                o = 0 #orto-neighbours
                m = 0 #meta-neighbours
                g = 0 #orto- or meta-neighbours
                if temp_cells[j-1][k-1] == 1:
                    o += 1
                    g += 1
                if temp_cells[j-1][k] == 1:
                    o += 1
                    g += 1
                if temp_cells[j][k-1] == 1:
                    o += 1
                    m += 1
                    g += 1
                if temp_cells[j][k+1] == 1:
                    o += 1
                    m += 1
                    g += 1
                if temp_cells[j+1][k] == 1:
                    m += 1
                    g += 1
                if temp_cells[j+1][k+1] == 1:
                    m += 1
                    g += 1
                
                if (temp_cells[j][k] == 1 and (o == 2 or m == 3 or g == 4)) or (temp_cells[j][k] == 0 and g == 2):
                    if j < self.N+1 and k < self.N+1:
                        new_cells[j-1][k-1] = 1
        

        self.cells.append(new_cells)
                
                
        
    

#----------------------------------Afbeelden-----------------------------------------

        
    def draw(self, t = -1):
        fig = plt.figure()
        im = plt.imshow(self.cells[t])
        plt.show()

    
    def live_draw(self):
        fig = plt.figure()
        data = np.array(self.cells[-1])
        lsquare = plt.imshow(data)
        temp = self
        
        def init():
            data = np.array(temp.cells[-1])
            lsquare.set_data(data)
            return [lsquare]
        
        def animate(i):
            temp.update(5,temp.rule)
            data = np.array(temp.cells[-1])
            lsquare.set_array(data)
            return [lsquare]
        
        
        anim = animation.FuncAnimation(fig, animate, frames = 5, init_func=init, repeat=True)
        return anim




    
"""
------------------------------------------------------------------------------------
------------------------------------------------------------------------------------
----------------------------------1 dimensional class-------------------------------
------------------------------------------------------------------------------------
------------------------------------------------------------------------------------
""" 

       

class line(GeneralCA):

#----------------------------------Generate cells-------------------------------------
  
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

    
    def temp_cells(self):
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

#----------------------------------Rule sets + updates---------------------------------
   
    def update(self,t,rule):
        for i in range(t):
            self.evolve(rule)
                
        
    def evolve(self,rule):
        value = format(int(rule),'08b')
        
        placing = [[1,1,1],[1,1,0],[1,0,1],[1,0,0],[0,1,1],[0,1,0],[0,0,1],[0,0,0]]
        
        temp_cells = self.temp_cells()
        new_cells = [0]*self.n
        
        
        for i in range(1,self.n+1):
            for j in range(len(value)):
                if [temp_cells[i-1],temp_cells[i],temp_cells[i+1]] == placing[j]:
                    new_cells[i-1] = int(value[j])
                    
        self.cells.append(new_cells)
        
#----------------------------------Afbeelden-------------------------------------
        
    def draw(self, t=0):
        if t == 0:
            t = len(self.cells)
        fig = plt.figure()
        im = plt.imshow(self.cells[0:t])
        plt.show()




"""
------------------------------------------------------------------------------------
------------------------------------------------------------------------------------
----------------------------------Test cases--------------------------------------
------------------------------------------------------------------------------------
------------------------------------------------------------------------------------
"""
    
        
    
      

#test = line(100,'periodic')
#test.generate_middle()
#test.update(100,'110')
#test.draw()

#for i in range(20):
#    test.rule30()
#plt.imshow(test.cells)


               




#test = square(60,'periodic')
#test.generate_cells()
#test.add_gun()
#test.generate_cells_percentage(0.4)
#test.cells = [[[0, 1, 0, 0, 0],
#               [1, 0, 0, 1, 1],
#               [1, 0, 1, 0, 1],
#               [1, 0, 1, 1, 0],
#               [1, 1, 0, 1, 1]]]

#test.update(10,'GOL')






"""
------------------------------------------------------------------------------------
------------------------------------------------------------------------------------
----------------------------------Run the file--------------------------------------
------------------------------------------------------------------------------------
------------------------------------------------------------------------------------
"""

def run2():
    def step1():
        print("How many cells? (give an integer), or c for exit")
        n = input()
        if n == 'c':
            exit
        try: 
            n = int(n)
        except: 
            print("This needs to be a integer" )
            n = step1()
        return step2(n)
    
    def step2(n):
        print("What kind of grid? (line, square, hexagon, triangle, 3dsquare), or c for exit")
        grid = input()
        if grid == 'line' or grid == 'square' or grid == 'hexagon' or grid == 'triangle' or grid == '3dsquare':
            return step3(n,grid)
        elif grid == 'c' :
            exit
        else:
            print("Choose one of the options")
            return step2(n)
        
    def step3(n,grid):
        print("Which initial conditions? (periodic, dirichlet1, dirichlet0), or c for exit")
        con = input()
        if con == 'periodic' or con == 'dirichlet1' or con == 'dirichlet0':
            CA = eval(grid)(n,con)
            if grid == 'line':
                return step8(CA,grid)
            elif grid == 'square':
                return step10(CA,grid)
        elif con == 'c' :
            exit
        else:
            print("Choose one of the options")
            return step3(n,grid)
        
    def step4(CA,grid):
        print("what percentage of the grid filled? (0 for 0%, 1 for 100%), or c for exit")
        percent = input()
        if percent == 'c':
            exit
        try: 
            percent = float(percent)
        except: 
            print("This needs to be a number" )
            percent = step4(CA,grid)
        if percent < 0 or percent > 1:
            print("The value must be between 0-1")
            return step4(CA,grid)
        if grid == 'square': 
            CA.generate_cells_percentage(percent)
            return step5(CA)
        elif grid == 'line':
            CA.generate_cells(percent)
            return step6(CA)
    
    def step5(CA):
        print("What ruleset? (GOL), or c for exit")
        rule = input()
        if rule == 'c':
            exit
        elif rule == 'GOL':
            return step5b(CA)
        else:
            print("Choose one of the options")
            return step5(CA)
    
    def step5b(CA):
        print("type animate or timestep or c for exit")
        x = input()
        if x == 'c':
            exit
        elif x == 'timestep':
            return step6(CA)
        elif x == 'animate':
            return CA.live_draw()
            exit
        else:
            print('choose one')
            return step5b(CA)
    
    def step6(CA):
        print("What ruleset? (1-164), or c for exit")
        rule = input()
        if rule == 'c':
            exit
        try: 
            rule = int(rule)
        except: 
            print("This needs to be a integer" )
            rule = step6(CA)
        if rule < 1 or rule > 164:
            print("Must be between 1-164")
            return step6(CA)
        return step7(CA,rule)
    
    def step7(CA,rule):
        print("How many timesteps? (give an integer), or c for exit")
        t = input()
        if t == 'c':
            exit
        try: 
            t = int(t)
        except: 
            print("This needs to be a integer" )
            t = step7(CA,rule)
        CA.update(t,rule)
        return step9(CA,t)
    
    def step8(CA,grid):
        print('Generate random cells(random) or 1 positive in the middle of the chain(middle)?, or c for exit')
        x = input() 
        if x == 'c':
            exit
        elif x == 'random':
            return step4(CA,grid)
        elif x == 'middle':
            CA.generate_middle()
            return step6(CA)
        else:
            print('choose one')
            
            return step8(CA,grid)
    
    def step9(CA,t):
        print('Which timestep would you like to see?, integer between 1 and ',t,', or c for exit')
        tstep = input()
        if tstep == 'c':
            exit

        try:
            tstep = int(tstep)
        except:
            print("This needs to be a integer")
            tstep = step9(CA,t)
        if tstep < 1 or tstep > t:
            print("Between 1 and",t)
            return step9(CA,t)
        return CA.draw(tstep)
        
    def step10(CA,grid):
        print("Random cells (random), or a gun (only if n > 38) ?, or c for exit")
        cells = input()
        if cells == 'c':
            exit
        elif cells == 'random':
            return step4(CA,grid)
        elif cells == 'gun':
            if CA.n > 38:                
                CA.generate_cells()
                CA.add_gun()
                return step5(CA)
            else: 
                return step1()
        else:
            return step10(CA,grid)
                
    
    
    
    return step1()
    
    
"""
def run():
    def step1():
        print("How many cells? (give an integer), or c for exit")
        n = input()
        if n == 'c':
            exit
        try: 
            n = int(n)
        except: 
            print("This needs to be a integer" )
            n = step1()
        return n
    
    def step2():
        print("What kind of grid? (line, square, hexagon, triangle, 3dsquare), or c for exit")
        grid = input()
        if grid == 'line' or grid == 'square' or grid == 'hexagon' or grid == 'triangle' or grid == '3dsquare':
            return grid
        elif grid == 'c' :
            exit
        else:
            print("Choose one of the options")
            return step2()
        
    def step3():
        print("Which initial conditions? (periodic, dirichlet1, dirichlet0), or c for exit")
        con = input()
        if con == 'periodic' or con == 'dirichlet1' or con == 'dirichlet0':
            return con
        elif con == 'c' :
            exit
        else:
            print("Choose one of the options")
            return step3()
        
    def step4():
        print("what percentage of the grid filled? (0 for 0%, 1 for 100%), or c for exit")
        percent = input()
        if percent == 'c':
            exit
        try: 
            percent = float(percent)
        except: 
            print("This needs to be a number" )
            percent = step4()
        if percent < 0 or percent > 1:
            print("The value must be between 0-1")
            return step4()
        return percent
    
    def step5():
        print("What ruleset? (GOL), or c for exit")
        rule = input()
        if rule == 'c':
            exit
        elif rule == 'GOL':
            return rule
        else:
            print("Choose one of the options")
            return step5()
    
    def step6():
        print("What ruleset? (1-164), or c for exit")
        rule = input()
        if rule == 'c':
            exit
        try: 
            rule = int(rule)
        except: 
            print("This needs to be a integer" )
            rule = step6()
        if rule < 1 or rule > 164:
            print("Must be between 1-164")
            return step6()
        return rule
    
    def step7():
        print("How many timesteps? (give an integer), or c for exit")
        t = input()
        if t == 'c':
            exit
        try: 
            t = int(t)
        except: 
            print("This needs to be a integer" )
            t = step7()
        return t
    
    def step8():
        print('Generate random cells(random) or 1 positive in the middle of the chain(middle)?, or c for exit')
        x = input() 
        if x == 'c':
            exit
        elif x == 'random':
            return x
        elif x == 'middle':
            return x
        else:
            print('choose one')
            return step8()
    
    def step9(t):
        print('Which timestep would you like to see?, integer between 1 and ',t,', or c for exit')
        tstep = input()
        if tstep == 'c':
            exit
        try:
            tstep = int(tstep)
        except:
            print("This needs to be a integer")
            tstep = step9(t)
        if tstep < 1 or tstep > t:
            print("Between 1 and",t)
            return step9()
        return tstep
    
            
    n = step1()
    grid = step2()
    con = step3()
    
    CA = eval(grid)(n,con)
    
    if grid == 'line':
        x = step8()
        if x == 'random':
            percent = step4()
            CA.generate_cells(percent)
        elif x == 'middle':
            CA.generate_middle()
        rule = step6()
        
        
        
    elif grid == 'square':
        percent = step4()
        CA.generate_cells_percentage(percent)
        rule = step5()
        
        
    t = step7()
    CA.update(t,rule)
    tstep = step9(t)
    CA.draw(tstep)
            
"""            
