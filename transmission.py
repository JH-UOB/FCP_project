# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 16:31:32 2021

Author: Alex Straw
Description:
    Takes all relevant office interactions and determines if an infection of COVID-19 has taken place.
    The person class is updated to reflect any changes made.
"""
def get_contagious_interactions(people,interactions):
    contagious_interactions = []

    for i in range(0, len(interactions)):
        person_1_ID = abs(int(interactions[i][0])) - 1  #Acquiring IDs for people involved in interaction i of current step
        person_2_ID = abs(int(interactions[i][1])) - 1

        if people[person_1_ID].infected != people[person_2_ID].infected:
            distance = interactions[i][2] #find distance apart if interaction is relevant
            contagious_interactions.extend((person_1_ID,person_2_ID,distance))

    return(contagious_interactions)

def do_something(people,person,interactions):

    if len(interactions) > 0:
        contagious_interactions = get_contagious_interactions(people,interactions)
        print(contagious_interactions)
    else:
        pass

    """
    if len(interactions) > 0:
        person_1_ID = abs(int(interactions[0][0]))
        print(people[person_1_ID].infected)
    else:
        pass

    for i in range(0, len(interactions)):
        person_1_ID = abs(int(interactions[i][0]))
        person_2_ID = interactions[i][1]
        distance = interactions[i][2]


        print(person_1_ID)
        print(person_2_ID)
        print(distance)
        print("")
    """




