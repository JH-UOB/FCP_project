from person import Person
from office import Office
import matplotlib.pyplot as plt
from scipy.spatial import distance
import itertools
import timeit
import random

def main():
    parameters = {'Maximum Age': 65,
                  'Minimum Age': 18,
                  'Mask Adherence': 0.8,
                  'Social Distancing Adherence': 0, #This is broke, leave at 0
                  'Number of Floors': 0.5,
                  'Number of People': 20,
                  'Simulation Duration': 100}

    selected_office = Office()  # Initialise office space
    selected_people = instantiate_people(parameters, selected_office)  # Initialise office space
    run_simulation(parameters, selected_office, selected_people)
    return selected_office
    # plt.imshow(selected_office.pathfinding_array.tolist())  # ideas for plotting - doesn't work for letters
    # plt.show()


def instantiate_people(params, office):
    number_of_people = params['Number of People']
    people = []
    for ID in range(1, number_of_people + 1):
        people.append(Person(ID, office.desk_locations, params))  # change to desk
        office.people_locations.append(people[ID - 1].current_location)
    return people


def update_location(people, person, office):

    x_coord_old = person.current_location[0]
    y_coord_old = person.current_location[1]
    office.pathfinding_array[x_coord_old][y_coord_old] = 1
    
    if person.social_distancing:
        print(person.current_location)
        office.fill_social_distancing_array(person.current_location, people)
        path = person.get_path(office.social_dist_array)
        if len(path) > 0:
            person.move(path)
        else:
            path = person.get_path(office.pathfinding_array)
            if len(path) > 0:
                person.move(path)
            else:
                avail_cells = office.adj_finder(office.pathfinding_array, person.current_location)
                person.current_location = avail_cells[random.randint(0,len(avail_cells)-1)]
        
    else:
        path = person.get_path(office.pathfinding_array)
    if len(path) > 0:
        person.move(path)

    else:
        
        avail_cells = office.adj_finder(office.pathfinding_array, person.current_location)
        # print(person.current_location)
        # print(avail_cells)
        person.current_location = avail_cells[random.randint(0,len(avail_cells)-1)]

    x_coord_new = person.current_location[0]
    y_coord_new = person.current_location[1]
    office.display_array[x_coord_new][y_coord_new] = - person.ID
    office.pathfinding_array[x_coord_new][y_coord_new] = - person.ID


def start_moving(people, person, office):
    person.task_progress = 0
    person.get_task(office.task_locations)
    update_location(people, person, office)


def keep_moving(people, person, office):
    x_coord = person.current_location[0]
    y_coord = person.current_location[1]
    office.display_array[x_coord][y_coord] = 1
    update_location(people, person, office)

def record_interactions(office, people):
    interactions = []
    for person in people:
        interactions.extend(office.find_interactions(office.pathfinding_array, person.current_location))
    
    interactions.sort()
    interactions = list(interactions for interactions,_ in itertools.groupby(interactions))
    return interactions

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

        # print(office.display_array)
        print(time)
        office.interactions = record_interactions(office, people)
        office.interaction_frames.append(office.interactions)
        display_frames.append(office.display_array)
        people_frames.append(people)
        

        # office.detect_interactions()  # TBC
        plt.figure(time)
        plt.title(str(time))
        plt.imshow(office.pathfinding_array.tolist())  # ideas for plotting - doesn't work for letters
        plt.show()
        


if __name__ == "__main__":
    start = timeit.default_timer()
    office = main()
    stop = timeit.default_timer()

    print('Time: ', stop - start) 
