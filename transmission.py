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
            contagious_interaction_IDs = [person_1_ID,person_2_ID]
            contagious_interactions.append(contagious_interaction_IDs) #Create a list of lists for contagious interactions

    return(contagious_interactions)

def do_something(people,person,interactions):

    if len(interactions) > 0:
        contagious_interactions = get_contagious_interactions(people,interactions)
        print(len(contagious_interactions))

    else:
        pass




