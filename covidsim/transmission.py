# -*- coding: utf-8 -*-
"""
Created on Tues Apr 6 12:25:03 2021

Author: Alex Straw
Description:
    This piece of code receives the 'people' object and interactions for a given step.
    Contagious interactions where one individual has COVID-19 and the other does not are
    extracted from this data.  Transmission chance is found from mask adherence, distance for
    a given interaction, and virality (acquired via GUI). Where an infection has taken
    place, a person's infection state is set to True.
"""

import random


def get_type(boolean_array):
    """Determine the 'type' of individual --> further explanation within get_contagious_interactions"""
    if boolean_array[0] == boolean_array[1]:
        if boolean_array[0]:
            person_type = 1
        else:
            person_type = 3
    else:
        person_type = 2

    return person_type


def get_contagious_interactions(people, interactions):
    """
    This function determines contagious interactions from the full list of interactions
    (plural) for a step
    """
    contagious_interactions = []

    for i in range(0, len(interactions)):
        person_1_ID = abs(int(interactions[i][0]))  # Acquiring IDs for people involved in interaction 'i' of step
        person_2_ID = abs(int(interactions[i][1]))  # Question this -1 as unsure if mistake - 06.04.2021 - Alex
        distance = interactions[i][2]

        person_1_type = get_type([people[person_1_ID].infected, people[person_1_ID].contagious])
        person_2_type = get_type([people[person_2_ID].infected, people[person_2_ID].contagious])

        #  3 types of individuals:
        #  Type 1: [infected = True, contagious = True]     --> All initial infected
        #  Type 2: [infected = True, contagious = False]    --> Those infected during simulation.py
        #  Type 3: [infected = False, contagious = False]   --> Those not infected
        #  A contagious interaction is an interaction be    tween a Type 1 and Type 3

        # Room for optimisation here

        if person_1_type == 1 and person_2_type == 3:
            contagious_interaction_IDs = [person_1_ID, person_2_ID, distance]
            contagious_interactions.append(contagious_interaction_IDs)

        elif person_1_type == 3 and person_2_type == 1:
            contagious_interaction_IDs = [person_2_ID, person_1_ID, distance]
            contagious_interactions.append(contagious_interaction_IDs)

    return contagious_interactions


def get_transmission_chance(interaction, people, virality):
    """
    get_transmission_chance calculates the transmission chance for an interaction (singular)
    based on: mask adherence and the distance between two individuals.

    :param interaction: An array of IDs for two individuals involved in an interaction
    :param people: People is the full list of individuals in the simulation (Person Class)
    :param virality: A factor associated with the 'contagiousness' of the virus (set in GUI)
    :return: returns A transmission chance --> this is a number between 0 and 1.
    """
    person_1_number = interaction[0]
    person_2_number = interaction[1]
    distance = interaction[2]

    if people[person_1_number].mask and people[person_2_number].mask:  # AND GATE (2 MASKS)
        mask_transmission_chance = 0.5
    elif people[person_1_number].mask != people[person_2_number].mask:  # XOR GATE (1 MASK)
        mask_transmission_chance = 0.75
    else:  # (0 MASKS)
        mask_transmission_chance = 1

    #  Infection rate is inversely proportional the square of the distance separating two individuals

    if distance < 1:
        distance_transmission_chance = 1
    elif distance > 2:
        distance_transmission_chance = 0.25
    else:
        distance_transmission_chance = 1 / (distance ** 2)  # Inverse square law

    transmission_chance = mask_transmission_chance * distance_transmission_chance * virality * 0.01

    return transmission_chance


def get_total_infected(people):
    """"Iterate through people (person objects) and calculate total number of infected people"""
    infected = 0
    for person in people:
        if people[person].infected:
            infected += 1
        else:
            pass
    return infected


def get_total_contagious(people):
    """"Iterate through people (person objects) and calculate total number of contagious people"""
    contagious = 0
    for person in people:
        if people[person].contagious:
            contagious += 1
        else:
            pass
    return contagious


def determine_infection(contagious_interactions, people,virality):
    """determine_infection calculates whether an infection has taken place and updates the people class"""
    infection_occurred_step = False
    for n in range(0, len(contagious_interactions)):
        transmission_random_number = random.uniform(0, 1)
        non_infected_id = abs(int(contagious_interactions[n][1]))

        interaction_transmission_chance = get_transmission_chance(contagious_interactions[n], people,virality)

        if transmission_random_number < interaction_transmission_chance:
            people[non_infected_id].infected = True
            people[non_infected_id].infector_ID = contagious_interactions[n][0]  # Infector ID for tree building
            infection_occurred_step = True
    return infection_occurred_step


def step_transmission(people, interactions, virality):
    """step_transmission checks if interactions have happened in the given step --> equiv to main"""
    if len(interactions) > 0:  # Checking if any general interactions have happened in the step
        contagious_interactions = get_contagious_interactions(people, interactions)
        if len(contagious_interactions) > 0:  # Checking if any contagious interactions have happened in the step
            infection_occurred_step = determine_infection(contagious_interactions, people,virality)

            if infection_occurred_step:
                infected = get_total_infected(people)
                infected_fraction = str(infected) + ' / ' + str(len(people))
                # print("Infected: " + infected_fraction)
