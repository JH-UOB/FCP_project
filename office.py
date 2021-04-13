import pandas as pd
import numpy as np
from scipy.spatial import distance

class Office:

    def __init__(self):
        """
        Generate an office object with desk and task locations dictated by an
        excel input file.

        """
        # Create an array using the excel input file
        self.display_array = pd.read_excel('office_array.xls').values.transpose()
        # Create pathfinding array denoting which cells are transversible.
        self.pathfinding_array = np.where(self.display_array != 0, 1, self.display_array)
        # Find locations of tasks and desks
        self.desk_locations = list(zip(list(np.where(self.display_array == 'D'))[0],
                                       list(np.where(self.display_array == 'D'))[1]))
        self.task_locations = list(zip(list(np.where(self.display_array == 'T'))[0],
                                       list(np.where(self.display_array == 'T'))[1]))
        # Create social distancing array from pathfinding array which will be
        # used for people who have the social distancing attribute.
        self.social_dist_array = self.pathfinding_array.copy()
        # Create people locations dictionary to be populated and updated as 
        # people move.
        self.people_locations = {}
        
        
    def adj_finder(self, matrix, position, interactions=False):
        adj = []

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                rangeX = range(0, matrix.shape[0])  # X bounds
                rangeY = range(0, matrix.shape[1])  # Y bounds

                (newX, newY) = (position[0]+dx, position[1]+dy)  # adjacent cell

                if (newX in rangeX) and (newY in rangeY) and (dx, dy) != (0, 0):
                    if interactions:
                        if matrix[newX, newY] != 0:
                            adj.append((newX, newY))
                    else:
                        if matrix[newX, newY] > 0:
                            adj.append((newX, newY))
        return adj

    def find_interactions(self, matrix, person_loc):
        adj_cells = self.adj_finder(matrix, person_loc, True)
        extra_cells = []
        for cell in adj_cells:
            extra_cells.extend(self.adj_finder(matrix, cell, True))
        adj_cells.extend(extra_cells)
        adj_cells = [x for x in adj_cells if x != person_loc]
        interactions = []
        for cell in adj_cells:
            if matrix[cell] < 0:
                interactions.append([max(matrix[person_loc], matrix[cell]),
                                         min(matrix[person_loc], matrix[cell]),
                                              distance.euclidean(person_loc, cell)])
        return interactions

    def fill_social_distancing_array(self, current_person_ID, people_locations):
        people = list(people_locations.keys())
        people.remove(current_person_ID)
        social_dist_array = self.pathfinding_array.copy()
        for person in people:
            bubble = self.adj_finder(self.pathfinding_array, people_locations[person])
            for location in bubble:
                social_dist_array[location] = 0
                
        return social_dist_array











