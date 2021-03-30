# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 16:31:32 2021

Authors: James Hawke, Adam Honnywill
Description:
    Defines a person with constant and variable attributes used to model movement, interactions and Covid-19
    transmission.
"""

import random
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class Person:
    
    def __init__(self, id, desks, params):
        """


        Parameters
        ----------
        params : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.id = id

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

        # Position variables
        self.desk_location = [desks[1][id-1], desks[0][id-1]]  # Desk coordinates
        self.task_location = self.desk_location.copy()  # Initialise person at their desk
        self.current_location = self.desk_location.copy()

        # Task variables
        self.task_duration = random.randint(1, 10) # How long person should stay at desk initially
        self.task_progress = 0
        self.doing_task = True

        # self.desk_location = [4,1]
        # self.task = get_task()
        self.current_location = self.desk_location.copy()

    def get_task(self, locations):
    
        if self.current_location == self.desk_location:
            self.task_location = locations[random.randint(0,len(locations))]
            self.task_duration = random.randint(1, 10)
        else:
            self.task_location = self.desk_location
            self.task_duration = random.randint(1, 10)

    def get_path(self, office):
        grid = Grid(matrix=office.get_pathfinding_array())
        start = grid.node(self.current_location[0], self.current_location[1])
        end = grid.node(office.microwave[1][0], office.microwave[0][0]) # can change location manually for now
        # end = grid.node(self.task_location[0], self.task_location[1]) # variable task location, untested
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(start, end, grid)
        print('operations:', runs, 'path length:', len(path), 'path coordinates:', path)
        print(grid.grid_str(path=path, start=start, end=end))
        return path

    def move(self, path):
        self.current_location = path[1]

    # def update(self): to be used potentially to move simulation functionality here

