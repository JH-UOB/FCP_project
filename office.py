import pandas as pd
import numpy as np


class Office:

    def __init__(self):
        self.display_array = pd.read_excel('office_array.xls').values.transpose()
        self.pathfinding_array = np.where(self.display_array != 0, 1, self.display_array)
        self.desk_locations = list(zip(list(np.where(self.display_array == 'D'))[0], list(np.where(self.display_array == 'D'))[1]))
        self.task_locations = list(zip(list(np.where(self.display_array == 'T'))[0], list(np.where(self.display_array == 'T'))[1]))
        self.people = []  # to be populated

    # def detect_interactions(self):
        # run through array and check for touching/near ids
        # for interacting ids, run the transmission function
