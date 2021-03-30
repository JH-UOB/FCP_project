# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 16:31:32 2021

Authors: James Hawke, Adam Honnywill
Description:
    Defines a person with constant and variable attributes used to model movement, interactions and Covid-19
    transmission.
"""

import numpy as np
import random
import itertools
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class person():
    
    def __init__(self, params):
        self.age = random.randint(params['Minimum Age'], params['Maximum Age'])

        if random.random() > 0.5:
            self.gender = 'Male'
        else:
            self.gender = 'Female'

        if random.random() < params['Mask adherance']:
            self.mask = True
        else:
            self.mask = False

        if random.random() < params['Social distancing adherance']:
            self.social_distancing = True
        else:
            self.social_distancing = False

        self.desk_location = [4,8]
        self.task_location = self.desk_location


        # Position variables
        self.desk_location = (4,10)
        self.task_location = self.desk_location.copy()

        self.current_location = self.desk_location.copy()

        # Task variables
        self.task_duration = random.randint(1, 10)
        self.task_progress = 0
        self.doing_task = True

        self.desk_location = [4,1]
        self.task = get_task()
        self.current_location = self.desk_location.copy()
        
        
        
    def get_task(self,locations):
    
        if self.current_location == self.desk_location:
            task_location = locations[random.randint(0,len(locations))]
            self.task_duration = random.randint(1, 10)
        else:
            task_location = self.desk_location
            self.task_duration = random.randint(1, 10)
            
        return(task_location)
        

    def get_path(self, office):
        grid = Grid(matrix=office.grid)
        start = grid.node(self.current_location[0], self.current_location[1])
        end = grid.node(office.printer[0], office.printer[1])
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(start, end, grid)
        print('operations:', runs, 'path length:', len(path))
        print(grid.grid_str(path=path, start=start, end=end))

        
class office():
    
     def __init__(self):
         self.grid = [[1 for i in range(0,10)] for i in range (0,10)]
         self.coffee = [3,8]
         self.printer = [1,6]
        


office = office()


        # Test
        # self.task = get_task()

params = {'Maximum Age' : 65,
          'Minimum Age' : 18,
          'Mask adherance' : 0.8,
          'Social distancing adherance' : 0.5}    
jim = person(params)
jim.get_path(office)


