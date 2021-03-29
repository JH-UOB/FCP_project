# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 16:31:32 2021

@author: james
"""

import numpy as np
import random
# from task import get_task

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
        if random.random() < params['Social distancing likelihood']:
            self.social_distancing = True
        else:
            self.social_distancing = False
    
        self.desk_location = (4,10)
        self.task_location = self.desk_location.copy()
        self.current_location = self.desk_location.copy()
        self.task_duration = random.randint(1, 10)
        self.task_progress = 0
        self.doing_task = True


params = {'Maximum Age' : 65,
          'Minimum Age' : 18,
          'Mask adherance' : 0.8,
          'Social distancing likelihood' : 0.5}
jim = person(params)
