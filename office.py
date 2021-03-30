import pandas as pd
import numpy as np


class Office:

    def __init__(self):
        self.grid = pd.read_excel('office_array.xls').values
        self.desks = np.where(self.grid == 'D')
        self.printer = np.where(self.grid == 'P')
        self.coffee = np.where(self.grid == 'C')
        self.microwave = np.where(self.grid == 'M')
        self.water = np.where(self.grid == 'W')
        self.toilets = np.where(self.grid == 'T')
        self.people = []  # to be populated

    def get_pathfinding_array(self):
        pathfinding_array = self.grid
        pathfinding_array = np.where(pathfinding_array != 0, 1, pathfinding_array)
        return pathfinding_array

    # def get_task_locations(self):
    #     task_locations = [self.printer[0], self.printer[0]]  # needs to concatenate more places
    #     return task_locations

    # def detect_interactions(self):
        # run through array and check for touching/near ids
        # for interacting ids, run the transmission function
