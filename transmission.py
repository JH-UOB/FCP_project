# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 16:31:32 2021

Author: Alex Straw
Description:
    Takes all relevant office interactions and determines if an infection of COVID-19 has taken place.
    The person class is updated to reflect any changes made.
"""

import random

def get_contagious_interactions(people,person,interactions):
    contagious_interactions = []
    """     contagious_interactions is a list of lists              """
    """     Format: [Infected Person,Non-Infected Person,Distance]  """

    for i in range(0, len(interactions)):
        person_1_ID = abs(int(interactions[i][0])) -1 #Acquiring IDs for people involved in interaction i of current step
        person_2_ID = abs(int(interactions[i][1])) -1 #Question this -1 as unsure if mistake - 06.04.2021 - Alex
        distance = interactions[i][2]

        if people[person_1_ID].infected != people[person_2_ID].infected: #XOR GATE for contagious interaction
            if people[person_1_ID].infected is True:
                contagious_interaction_IDs = [person_1_ID,person_2_ID,distance]
            else:
                contagious_interaction_IDs = [person_2_ID, person_1_ID,distance]

            contagious_interactions.append(contagious_interaction_IDs)

    return(contagious_interactions)

def determine_infection(contagious_interactions, people):
    default_chance = 0.5

    for n in range(0, len(contagious_interactions)):
        infection_chance = random.randint(0, 1)

        if infection_chance > default_chance:
            print("Person: " + str(contagious_interactions[n][1]) + " is now infected")

def do_something(people,person,interactions):

    if len(interactions) > 0:
        contagious_interactions = get_contagious_interactions(people,person,interactions)
        if len(contagious_interactions) > 0:
            determine_infection(contagious_interactions, people)





