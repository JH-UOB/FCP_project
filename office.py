"""

office.py
Designed and written by Adam Honnywill and James Hawke, predominantly through "pair coding"
April 2021

This script contains a class that defines an office space and processes it for movement purposes.

Used by simulation.py.
"""

# External modules
import pandas as pd
import numpy as np
from scipy.spatial import distance


class Office:
    """This class is used to generate arrays that track the locations of tasks, desks and people as the latter move
    through the simulation. It:

        1. Generates pathfinding arrays

            Pathfinding arrays are processed from an .xls floorplan and input into the simulation by the office class.
            They need to be formatted such that any traversable cell has a value greater than 0: wall cells have a value
            of 0; floor, task and desk sitting cells have a value of 1, and people occupied cells have a value that is
            equal to their negative ID number, to simultaneously track their position and make their location not
            traversable to others.

            It repeats this process for those who abide social distancing, making the adjacent cells to people not
            traversable. This social distancing pathfinding array is only obeyed if the route is available: if they
            cannot social distance, the person will revert to the normal pathfinding array.

        2. Detecting interactions

            As the pathfinding array stores the locations of people, these can be analysed at each time step to detect
            interactions that might lead to transmission.

    """

    def __init__(self, floor_no):
        """
        Generate an office object with desk and task locations dictated by an
        excel input file.

        """
        # Create an array using the excel input file
        self.input_array = pd.read_excel('office_array.xls', floor_no).values.transpose()
        # Create pathfinding array denoting which cells are traversable
        self.pathfinding_array = np.where(self.input_array != 0, 1, self.input_array)
        # Create array for displaying infection status
        self.display_array = self.pathfinding_array.copy()
        # Find locations of tasks (T in excel) and desks (D in excel)
        self.desk_locations = list(zip(list(np.where(self.input_array == 'D'))[0],
                                       list(np.where(self.input_array == 'D'))[1]))
        self.task_locations = list(zip(list(np.where(self.input_array == 'T'))[0],
                                       list(np.where(self.input_array == 'T'))[1]))
        # Create social distancing array from pathfinding array which will be
        # used for people who have the social distancing attribute.
        self.social_dist_array = self.pathfinding_array.copy()
        # Create people locations dictionary to be populated and updated as
        # people move.
        self.people_locations = {}

    def adj_finder(self, matrix, position, interactions=False):
        """Used to detect if cells adjacent to the one occupied are available for moving into. The optional
        interactions flag enables social distancing"""
        adj = []

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                rangeX = range(0, matrix.shape[0])  # X bounds
                rangeY = range(0, matrix.shape[1])  # Y bounds

                (newX, newY) = (position[0] + dx, position[1] + dy)  # adjacent cell

                if (newX in rangeX) and (newY in rangeY) and (dx, dy) != (0, 0):
                    # If within office walls and not itself...
                    if interactions:
                        # ... and not a wall, select cells as adjacent
                        if matrix[newX, newY] != 0:
                            adj.append((newX, newY))
                    else:
                        # ... and not a person or a wall, select cells as adjacent
                        # NOTE: cells occupied by people are represented by a value equal to their negative id
                        if matrix[newX, newY] > 0:
                            adj.append((newX, newY))
        return adj

    def find_interactions(self, matrix, person_loc):
        """Return a list of interactions that includes the people interacting and the distance between them"""
        # Find person adjacent cells that are unoccupied by walls
        adj_cells = self.adj_finder(matrix, person_loc, True)
        extra_cells = []
        for cell in adj_cells:
            # Find cells adjacent to person adjacent cells i.e. to detect wall unoccupied cells within 2 cells of the
            # person
            extra_cells.extend(self.adj_finder(matrix, cell, True))
        adj_cells.extend(extra_cells)
        adj_cells = [x for x in adj_cells if x != person_loc]  # filters cell to remove person location
        interactions = []
        for cell in adj_cells:
            if matrix[cell] < 0:
                # Checks if adjacent cells are occupied by people and records their relative distance in an interaction
                # if so
                interactions.append([max(matrix[person_loc], matrix[cell]),
                                     min(matrix[person_loc], matrix[cell]),
                                     distance.euclidean(person_loc, cell)])
        return interactions

    def fill_social_distancing_array(self, current_person_ID, people_locations):
        """Returns a modified pathfinding array that enlarges the not traversable space around other people"""
        people = list(people_locations.keys())
        people.remove(current_person_ID)
        social_dist_array = self.pathfinding_array.copy()
        for person in people:
            bubble = self.adj_finder(self.pathfinding_array, people_locations[person])
            for location in bubble:
                # Modifies pathfinding array to have 'walls' in cells adjacent to other people, so socially distant
                # pathfinding keeps distant
                social_dist_array[location] = 0

        return social_dist_array
