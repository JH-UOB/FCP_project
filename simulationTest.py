import itertools
import timeit
import random
import matplotlib.pyplot as plt
from scipy.spatial import distance
#from joblib import Parallel, delayed
from person import Person
from office import Office
import transmission

def main():
    parameters = {'Maximum Age': 65,
                  'Minimum Age': 18,
                  'Mask Adherence': 0.8,
                  'Social Distancing Adherence': 1, #This is broke, leave at 0
                  'Number of Floors': 0.5,
                  'Number of People': 26,
                  'Simulation Duration': 200}

    selected_office = Office()  # Initialise office space
    selected_people = instantiate_people(parameters, selected_office)  # Initialise office space
    run_simulation(parameters, selected_office, selected_people)
    return selected_office

    """ Used for testing, true will print data to log """
    infection_debug = True

def instantiate_people(params, office):
    number_of_people = params['Number of People']
    people = []
    for ID in range(1, number_of_people + 1):
        people.append(Person(ID, office.desk_locations, params))  # change to desk
        office.people_locations[ID] = (people[ID - 1].current_location)
        set_array_value(people[ID-1].current_location[0], people[ID-1].current_location[1], office.pathfinding_array, - ID)

    office.people = people
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
    set_array_value(person.current_location[0], person.current_location[1], office.pathfinding_array, - person.ID)
    office.people_locations[person.ID] = person.current_location

def set_array_value(x, y, array, value):
    array[x][y] = value

def start_moving(people, person, office):
    person.task_progress = 0
    person.get_task(office.task_locations)
    update_location(people, person, office)

def keep_moving(people, person, office):
    set_array_value(person.current_location[0], person.current_location[1], office.display_array, 1)
    update_location(people, person, office)

def move_somewhere(person, office):
    avail_cells = office.adj_finder(office.pathfinding_array, person.current_location)
    set_array_value(person.current_location[0], person.current_location[1], office.display_array, 1)
    person.current_location = avail_cells[random.randint(0,len(avail_cells)-1)]

def record_interactions(office, people):
    interactions = []
    for person in people:
        interactions.extend(office.find_interactions(office.pathfinding_array, person.current_location))
    interactions.sort()
    interactions = list(interactions for interactions,_ in itertools.groupby(interactions))
    return interactions

def plot_figure(time, office):
    plt.figure(time)
    plt.title(str(time))
    plt.imshow(office.pathfinding_array.tolist())
    plt.show()

""" ALEX TRANSMISSION """

def updated_infected(people,person,interactions,infection_debug):
    if infection_debug:
        transmission.do_something(people,person,interactions)
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
                keep_moving(people, person, office)

        print(time)
        office.interactions = record_interactions(office, people)
        office.interaction_frames.append(office.interactions)

        """ Used for testing, true will print data to log, false will pass function """
        infection_debug = False
        """ update who is infected, found using office interactions """
        updated_infected(people,person,office.interactions,infection_debug)

        display_frames.append(office.display_array)
        people_frames.append(people)
        plot_figure(time, office)


if __name__ == "__main__":
    start = timeit.default_timer()
    office = main()
    stop = timeit.default_timer()
    print('Time: ', stop - start)
