#!/usr/bin/env python3
"""

simulation.py
Designed and written by Adam Honnywill and James Hawke, predominantly through "pair coding"
April 2021

This script runs simulations of coronavirus transmission in an office to investigate the effects of various
parameters, such as wearing or social distancing. The script may be used to:

    1. Show an animation of the simulation on screen
    2. Create a video of a simulation
    3. Show a plot of different stages of the epidemic
    4. Save a plot to a file

This is done using code in this script, which in turn uses uses classes in other scripts:

    1. office.py            # to track the movement of people at any given time in the office space
    2. person.py            # to instantiate people in the office
    3. GUI.py               # to perform GUI based parameter input
    4. transmission.py      # to update the infection status of people upon interaction

The command line interface to the script allows for user input parameters to be input either from a GUI or a
text file, such that no code needs changing between simulations:

    $ python simulation.py               # run simulation with with text file input parameters
    $ python simulation.py --GUI         # run simulation with with GUI input parameters
    $ python simulation.py --help        # show all command line options

In order to run this script, one or two input files must be present in the directory:

    1. office_array.xls     # always
    2. input_parameters.txt # if the --GUI flag is not called

It is also possible to create a video of the animation (if you install
ffmpeg):

    $ python simulator.py --file=simulation.mp4

NOTE: You need to install ffmpeg for the above to work. The ffmpeg program
must also be on PATH.
"""

import itertools
import timeit
import random
import matplotlib.pyplot as plt
from person import Person
from office import Office
import transmission
import random


def main(parameters):
    """Command line entry point."""
    #
    # Load parameters from the argument specified source (the GUI or text file)
    #   https://docs.python.org/3/library/argparse.html
    #
    # parameters = {'Maximum Age': 65,
    #               'Minimum Age': 18,
    #               'Mask Adherence': 0.8,
    #               'Social Distancing Adherence': 1,
    #               'Number of Floors': 0.5,
    #               'Number of People': 10,
    #               'Simulation Duration': 50,
    #               }

    selected_office = Office(parameters['Office Plan'][0])  # initialise office space
    selected_people = instantiate_people(parameters, selected_office)  # initialise people in office space
    display_frames = run_simulation(parameters, selected_office, selected_people)  # run the simulation
    return display_frames


def instantiate_people(params, office):
    """Create people objects according to input parameters"""
    number_of_people = params['Number of People']
    # Populate a list of people with Person objects each with a unique desk 
    # location
    people = {}
    for ID in range(1, number_of_people + 1):
        people[ID] = Person(ID, office.desk_locations, params)
        # Update dictionary of people locations stored in Office object
        office.people_locations[ID] = people[ID].current_location
        # Set person location in pathfinding array to be not traversable
        set_array_value(people[ID].current_location[0],
                        people[ID].current_location[1],
                        office.pathfinding_array, - ID)
    infected_IDs = random.sample(range(1, number_of_people + 1), params['Number of infected'])
    for ID in infected_IDs:
        people[ID].infected = True
        people[ID].contagious = True
    
    # Save dict of people to office object
    office.people = people.copy()
    return people


def update_location(person, office):
    """Moves people that are moving between their desk and their next task, attempting to socially distance only if
    possible """
    set_array_value(person.current_location[0], person.current_location[1], office.pathfinding_array, 1)

    if person.social_distancing:
        # Generate array for pathfinding whilst socially distancing
        social_dist_array = office.fill_social_distancing_array(person.ID, office.people_locations)
        # Generate path through array
        # NOTE: when path generation fails, it returns an empty list
        path = person.get_path(social_dist_array)
        if len(path) > 0:
            # Socially distanced path generation successful, move along path
            person.move(path)
        else:
            # Find path without socially distancing
            path = person.get_path(office.pathfinding_array)
            if len(path) > 0:
                # Path without socially distancing generation successful, move along path
                person.move(path)
            else:
                # No path available, move avoid blockages
                move_somewhere(person, office)
    else:
        # Generate path through array
        # NOTE: when path generation fails, it returns an empty list
        path = person.get_path(office.pathfinding_array)
    if len(path) > 0:
        # Path without socially distancing generation successful, move along path and
        person.move(path)
    else:
        # No path available, move to avoid blockages
        move_somewhere(person, office)

    # Update pathfinding array with person location for other people to navigate
    set_array_value(person.current_location[0],
                    person.current_location[1],
                    office.pathfinding_array, - person.ID)
    office.people_locations[person.ID] = person.current_location  # Question - why do we record people locations?


def set_array_value(x, y, array, value):
    """Updates an array"""
    array[x][y] = value


def start_moving(person, office):
    """Assign a task to a person and start moving"""
    person.task_progress = 0
    # Assign a task
    person.get_task(office.task_locations)
    # Begin movement along path
    update_location(person, office)


def move_somewhere(person, office):
    """Move person somewhere adjacent to avoid blockages in narrow spaces"""
    # Get available, adjacent cells that can be moved into i.e. not a wall or another person
    avail_cells = office.adj_finder(office.pathfinding_array,
                                    person.current_location)
    # Set current person location in pathfinding array to be traversable
    set_array_value(person.current_location[0],
                    person.current_location[1],
                    office.display_array, 1)
    # Move person to an available cell
    person.current_location = avail_cells[random.randint(0, len(avail_cells) - 1)]


def record_interactions(office, people):
    """Checks for interactions in the office and stores them to simulate transmissions"""
    interactions = []
    # Detect interactions between people
    for person in people:
        interactions.extend(office.find_interactions(office.pathfinding_array, people[person].current_location))
    # Remove duplicate interactions
    interactions.sort()
    interactions = list(interactions for interactions, _ in itertools.groupby(interactions))
    return interactions


def plot_figure(time, office):
    """Plots the locations of people in the office as their locations are updated"""
    # plt.figure(time)
    # plt.title(str(time))
    # plt.imshow(office.pathfinding_array.tolist())
    # plt.show()


def run_simulation(params, office, people):
    """Core sequence of logic of the simulation. Formatted to record results in 'frames' for each time step.

    In each time step, everyone will progress a task, finish a task and move towards another task, or carry on moving
    between tasks. If they come into contact with each other they will potentially transmit coronavirus.

    """

    # Initialise lists to record results
    sim_duration = params['Simulation Duration']
    # office.floor_switcher(0)
    # print(params['Office Plan'][0])
    display_frames = []  # used to store locations for each time tick, for running through in GUI
    people_frames = []  # used to store people states for each time tick, for running through in GUI
    office.interaction_frames = []

    # For each time step, perform actions for each person in office
    for time in range(sim_duration):
        for person in people:  # move people as necessary
            if people[person].current_location == people[person].task_location:
                if people[person].task_progress < people[person].task_duration:  # task incomplete, keep doing task
                    people[person].task_progress += 1

                else:  # task complete, find new task and start moving
                    start_moving(people[person], office)

            else:  # between tasks, keep moving
                update_location(people[person], office)

        print('Time: ', time)  # for tracking progress
        office.interactions = record_interactions(office, people)
        office.interaction_frames.append(office.interactions)  # record interactions

        transmission.step_transmission(people, people[person], office.interactions)  # TRANSMISSION - ALEX

        display_frames.append(office.pathfinding_array.copy().tolist())  # record people locations in office
        # plot_figure(time, office)
        # people_frames.append(people)  # record status of people (included infection status)
        # plt.close()
        # plot_figure(time, office)

    return display_frames


if __name__ == "__main__":
    start = timeit.default_timer()
    office = main(parameters)
    stop = timeit.default_timer()
    print('Time: ', stop - start)
