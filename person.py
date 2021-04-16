# -*- coding: utf-8 -*-
"""

person.py
Designed and written by Adam Honnywill and James Hawke, predominantly through "pair coding"
April 2021

This script contains a class that defines a person with constant and variable attributes used to model movement,
interactions and Covid-19 transmission.

Used by simulation.py.
"""

import random
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class Person:
    """A person will sit at their desk for a random duration, randomly allocate themselves a task across the room
    e.g. go to the printer, and then find a path and move to that task. After the task they will return to their desk
    and repeat for the duration of the simulation. The properties assigned to a person modifies their behaviour e.g.
    how they will move around other people, and their likelihood of catching coronavirus e.g. if they are wearing a
    mask.

    """
    def __init__(self, ID, desks, params):
        """Initialise person properties based on simulation inputs"""
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
        if random.random() < 0.1:  # should be parameterised
            self.infected = True
            self.infected_time = 0
        else:
            self.infected = False

        # Transmission Properties
        self.contagious = False  # Needs to be implemented

        # Position properties
        self.desk_location = desks[ID-1]  # assign desk coordinates by ID COULD RANDOMISE MOVE TO SIMULATION
        self.task_location = self.desk_location  # Initialise person at their desk
        self.current_location = self.desk_location

        # Task properties
        self.task_duration = random.randint(1, 50) # How long person should stay at desk initially
        self.task_progress = 0
        # self.doing_task = True  # unused

    def get_task(self, locations):
        """Assign a random task location and task duration. Possible task 
            locations are determined by the selected office floorplan. If a 
            person has just completed a task, they will return to their desk 
            for a random duration. If they are at their desk, they will move 
            to a task location.
        """
        if self.current_location == self.desk_location:
            self.task_location = locations[random.randint(0, len(locations)-1)]
            self.task_duration = random.randint(1, 10)
        else:
            self.task_location = self.desk_location
            self.task_duration = random.randint(50, 100)

    def get_path(self, array):
        """Generates a path between the current location and destination location of the person, through the
        populated office space, using imported pathfinding."""

        # Load the office space to be navigated and add start (current) and end locations
        grid = Grid(matrix=array)
        start = grid.node(self.current_location[1], self.current_location[0])
        end = grid.node(self.task_location[1], self.task_location[0])
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)  # allow for diagonal movement

        # Generate the path
        path, runs = finder.find_path(start, end, grid)
        return path

    def move(self, path):
        """"Move person along their path"""
        self.current_location = (path[1][1], path[1][0])

