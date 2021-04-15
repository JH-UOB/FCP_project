# -*- coding: utf-8 -*-
"""
Created on Tues Apr 6 12:25:03 2021

Author: Alex Straw
Description:
    This piece of code receives the 'people' object and interactions for a given step.
    Contagious interactions where one individual has COVID-19 and the other does not are
    extracted from this data.  An infection chance is calculated based off specific person
    qualities such as 'mask adherence'.  A random number is used to see if the infection has occurred from
    the transmission chance. Where an infection has taken place, a person's infection state is set to True.
"""

import random

# TO DO
# When someone is infected they are not immediately infectious --> build this in
# Tree diagram showing infection from one individual to the end
# Once everyone is infected there is no need to continue the simulation
# Modify how we access the class --> i.e Jane.age is better than people[number].age

# Only initial infected are infectious --> build this in

"""
    get_contagious_interactions looks at all the interactions for the step.  It checks if individuals
    involved in interactions are infected with COVID-19.  If one person has COVID-19 and the other does
    not, it is added to a new 'list of lists' named 'contagious_interactions'.  The format for this
    array is: 
                contagious_interactions --> [Infected Person,Non-Infected Person,Distance]
"""


def get_contagious_interactions(people, person, interactions):
    contagious_interactions = []

    for i in range(0, len(interactions)):
        person_1_ID = abs(int(interactions[i][0])) - 1  # Acquiring IDs for people involved in interaction 'i' of step
        person_2_ID = abs(int(interactions[i][1])) - 1  # Question this -1 as unsure if mistake - 06.04.2021 - Alex
        distance = interactions[i][2]

        if people[person_1_ID].infected != people[person_2_ID].infected:  # XOR GATE for contagious interaction
            if people[person_1_ID].infected is True:
                contagious_interaction_IDs = [person_1_ID, person_2_ID, distance]
            else:
                contagious_interaction_IDs = [person_2_ID, person_1_ID, distance]

            contagious_interactions.append(contagious_interaction_IDs)

    return contagious_interactions


"""     determine_infection calculates whether an infection has taken place and updates the people class   """


def determine_infection(contagious_interactions, people):
    for n in range(0, len(contagious_interactions)):
        transmission_random_number = random.uniform(0, 1)
        non_infected_id = abs(int(contagious_interactions[n][1]))

        interaction_transmission_chance = people[non_infected_id].transmission_chance

        if transmission_random_number < interaction_transmission_chance:
            people[non_infected_id].infected = True


"""     get_total_infected is used to loop through the people class and find the number of infected   """


def get_total_infected(people):
    infected = 0
    for person in people:
        if person.infected:
            infected += 1
        else:
            pass
    return infected


"""     update_transmission_chance should only be run once     """


def update_transmission_chance(people, default_transmission_chance):
    for ID in range(0, len(people)):
        transmission_factor = 1
        if people[ID].mask is False:
            transmission_factor = transmission_factor * 2  # Found from literature (effect of wearing a mask)
        else:
            pass
        if people[ID].social_distancing is False:  # Social Distancing adherence is broken (see simulationTest.py)
            transmission_factor = transmission_factor * 1.34  # Found from literature (impact of social distancing)
        else:
            pass

        people[ID].transmission_chance = default_transmission_chance * transmission_factor
        people[ID].transmission_chance_initialised = True  # Every person must have their infection chance set


"""     step_transmission checks if interactions have happened in the given step --> equiv to main   """


def step_transmission(people, person, interactions):
    if len(interactions) > 0:  # Checking if any general interactions have happened in the step
        contagious_interactions = get_contagious_interactions(people, person, interactions)
        if len(contagious_interactions) > 0:  # Checking if any contagious interactions have happened in the step
            determine_infection(contagious_interactions, people)
            infected = get_total_infected(people)

            infected_fraction = str(infected) + ' / ' + str(len(people))
            print("Infected: " + infected_fraction)
