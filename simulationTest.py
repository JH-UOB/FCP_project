#!/usr/bin/env python3
"""

simulationTest.py
Adam Honnywill
James Hawke
April 2021

This script runs simulations of coronavirus transmission in an office to investigate the effects of various
parameters, such as wearing or social distancing. The script may be used to:

    1. Show an animation of the simulation on screen
    2. Create a video of a simulation
    3. Show a plot of different stages of the epidemic
    4. Save a plot to a file

This is done using code in this script, which uses uses classes in other scripts:

    1. office.py            # to track the movement of people at any given time in the office space
    2. person.py            # to instantiate people in the office
    3. GUI.py               # to perform GUI based parameter input
    4. transmission.py      # to update the infection status of people upon interaction

The command line interface to the script makes allows for user input parameters to be input either from a GUI or a
text file:

    $ python simulationTest.py               # run simulation with with text file input parameters
    $ python simulationTest.py --GUI         # run simulation with with GUI input parameters
    $ python simulationTest.py --help        # show all command line options

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
from scipy.spatial import distance
# from joblib import Parallel, delayed
from person import Person
from office import Office
import transmission


def main():
    """Command line entry point."""
    #
    # Load parameters from the argument specified source (the GUI or text file)
    #   https://docs.python.org/3/library/argparse.html
    #
    parameters = {'Maximum Age': 65,
                  'Minimum Age': 18,
                  'Mask Adherence': 0.8,
                  'Social Distancing Adherence': 1,
                  'Number of Floors': 0.5,
                  'Number of People': 10,
                  'Simulation Duration': 200,
                  'default_transmission_chance': 0.02
                  }

    selected_office = Office()  # Initialise office space
    selected_people = instantiate_people(parameters, selected_office)  # Initialise people in office space
    run_simulation(parameters, selected_office, selected_people)
    return selected_office


def instantiate_people(params, office):
    """Create people objects according to input parameters"""
    number_of_people = params['Number of People']
    # Populate a list of people with Person objects each with a unique desk 
    # location
    people = []
    for ID in range(1, number_of_people + 1):
        people.append(Person(ID, office.desk_locations, params))
        # Update dictionary of people locations stored in Office object
        office.people_locations[ID] = (people[ID - 1].current_location)
        # Set person location in pathfinding array to be untraversable
        set_array_value(people[ID - 1].current_location[0], 
                        people[ID - 1].current_location[1],
                        office.pathfinding_array, - ID)
    # Save list of people to office object
    office.people = people.copy()
    return people


def update_location(people, person, office):
    set_array_value(person.current_location[0], person.current_location[1], office.pathfinding_array, 1)

    if person.social_distancing:
        social_dist_array = office.fill_social_distancing_array(person.ID, office.people_locations)
        path = person.get_path(social_dist_array)
        if len(path) > 0:
            person.move(path)
        else:
            path = person.get_path(office.pathfinding_array)
            if len(path) > 0:
                person.move(path)
            else:
                move_somewhere(person, office)
    else:
        path = person.get_path(office.pathfinding_array)
    if len(path) > 0:
        person.move(path)
        set_array_value(person.current_location[0], person.current_location[1], office.pathfinding_array, - person.ID)
    else:
        move_somewhere(person, office)
    set_array_value(person.current_location[0], 
                    person.current_location[1], 
                    office.pathfinding_array, - person.ID)
    office.people_locations[person.ID] = person.current_location


def set_array_value(x, y, array, value):
    array[x][y] = value


def start_moving(people, person, office):
    """Assign a task to a person and start moving"""
    person.task_progress = 0
    # Assign a task
    person.get_task(office.task_locations)
    # Begin movement along path
    update_location(people, person, office)


def move_somewhere(person, office):
    """Move person somewhere to avoid blockages in narrow spaces"""
    # Get available cells that can be moved into i.e. not a wall or another person
    avail_cells = office.adj_finder(office.pathfinding_array, 
                                    person.current_location)
    # Set previous person location in pathfinding array to be traversable
    set_array_value(person.current_location[0], 
                    person.current_location[1], 
                    office.display_array, 1)
    # Move person to an available cell
    person.current_location = avail_cells[random.randint(0, len(avail_cells) - 1)]


def record_interactions(office, people):
    interactions = []
    for person in people:
        interactions.extend(office.find_interactions(office.pathfinding_array, person.current_location))
    interactions.sort()
    interactions = list(interactions for interactions, _ in itertools.groupby(interactions))
    return interactions


def plot_figure(time, office):
    plt.figure(time)
    plt.title(str(time))
    plt.imshow(office.pathfinding_array.tolist())
    plt.show()


""" ALEX TRANSMISSION """


def updated_infected(params, people, person, interactions, infection_debug):
    if people[1].transmission_chance_initialised is False:  # Checks if transmission rates have been assigned
        default_transmission_chance = params['default_transmission_chance']
        transmission.update_transmission_chance(people, default_transmission_chance)  # Individual transmission rate
    else:
        if infection_debug:  # Temporary whilst several people are working on the code
            transmission.step_transmission(people, person, interactions)  # Calls on transmission.py to update infected
        else:
            pass


def run_simulation(params, office, people):
    sim_duration = params['Simulation Duration']
    display_frames = []  # used to store locations for each time tick, for running through in GUI
    people_frames = []  # used to store people states for each time tick, for running through in GUI
    office.interaction_frames = []
    for time in range(sim_duration):
        # contents could be shifted to person class
        for person in people:  # move people as necessary
            if person.current_location == person.task_location:
                if person.task_progress < person.task_duration:
                    person.task_progress += 1

                else:  # task complete, find new task and start moving
                    start_moving(people, person, office)

            else:  # between tasks, keep moving
                update_location(people, person, office)

        print(time)
        office.interactions = record_interactions(office, people)
        office.interaction_frames.append(office.interactions)

        """     Infection & transmissibility    """

        infection_debug = True  # Used for testing, True will print data to log, False will pass function
        updated_infected(params, people, person, office.interactions, infection_debug)  # Update who is infected



        display_frames.append(office.display_array)
        people_frames.append(people)
        plot_figure(time, office)


if __name__ == "__main__":
    start = timeit.default_timer()
    office = main()
    stop = timeit.default_timer()
    print('Time: ', stop - start)
