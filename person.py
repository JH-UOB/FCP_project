# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 16:31:32 2021

@author: james
"""

import numpy as np
import random

class person(params):
    
    def __init__(self):
        self.age = random.randint(params['Maximum Age'], params['Minimum Age'])
        if random.random() > 0.5:
            self.gender = 'Male'
        else:
            self.gender = 'Female'
            
        if random.random < params['Mask likelihood']:
            self.mask = True
        else:
            self.mask = False
            
        if random.random < params['Social distancing likelihood']:
            self.social_distancing = True
        else:
            self.social_distancing = False
        
    
        