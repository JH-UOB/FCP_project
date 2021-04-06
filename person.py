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

    def __init__(self, ID, desks, params):
        """

        Parameters
        ----------
        params : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # Personal properties
        self.ID = ID
        self.age = random.randint(params['Minimum Age'], params['Maximum Age'])
        if random.random() > 0.5:
            self.gender = 'Male'
        else:
            self.gender = 'Female'
        if random.random() < params['Mask Adherence']:
            self.mask = True
        else:
            self.mask = False
        if random.random() < params['Social Distancing Adherence']:
            self.social_distancing = True
        else:
            self.social_distancing = False
        if random.random() < 0.4:
            self.infected = True
            self.infected_time = 0
        else:
            self.infected = False

        # Position properties
        self.desk_location = desks[ID-1]  # assign desk coordinates by ID COULD RANDOMISE MOVE TO SIMULATION
        self.task_location = self.desk_location  # Initialise person at their desk
        self.current_location = self.desk_location

        # Task properties
        self.task_duration = random.randint(1, 50) # How long person should stay at desk initially
        self.task_progress = 0
        # self.doing_task = True  # unused

    def get_task(self, locations):

        if self.current_location == self.desk_location:
            self.task_location = locations[random.randint(0, len(locations)-1)]
            self.task_duration = random.randint(1, 10)
        else:
            self.task_location = self.desk_location
            self.task_duration = random.randint(50, 100)

    def get_path(self, array):
        grid = Grid(matrix=array)

        start = grid.node(self.current_location[1], self.current_location[0])
        end = grid.node(self.task_location[1], self.task_location[0])  # variable task location, untested
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

        path, runs = finder.find_path(start, end, grid)
        # print('operations:', runs, 'path length:', len(path), 'path coordinates:', path)  # path metadata
        # print(grid.grid_str(path=path, start=start, end=end))  # show pathfinding
        return path

    def move(self, path):
        self.current_location = (path[1][1], path[1][0])

