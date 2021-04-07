# -*- coding: utf-8 -*-
"""
Created on Tues Apr 6 12:25:03 2021

Author: Alex Straw
Description:
    This piece of code receives the 'people' object and interactions for a given step.
    Contagious interactions where one individual has COVID-19 and the other does not are
    extracted from this data.  An infection chance is calculated based off specific person
    qualities such as 'mask adherence'.  A random number to see if the infection has occurred
    from this calculated chance. Where an infection has taken place, a person's infection state is set to True.
"""

import random

def get_contagious_interactions(people,person,interactions):
    contagious_interactions = []
    """     contagious_interactions is a list of lists              """
    """     Format: [Infected Person,Non-Infected Person,Distance]  """

    for i in range(0, len(interactions)):
        person_1_ID = abs(int(interactions[i][0])) -1 #Acquiring IDs for people involved in interaction 'i' of step
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

        non_infected_id = abs(int(contagious_interactions[n][1]))
        if infection_chance > default_chance:
            people[non_infected_id].infected = True

def get_total_infected(people):
    infected = 0
    for person in people:
        if person.infected:
            infected += 1
        else:
            pass
    return(infected)

def do_something(people,person,interactions):

    if len(interactions) > 0:
        contagious_interactions = get_contagious_interactions(people,person,interactions)
        if len(contagious_interactions) > 0:
            determine_infection(contagious_interactions, people)
            infected = get_total_infected(people)
            print("total number of people: " + str(len(people)))
            print("total number infected: " + str(infected))






