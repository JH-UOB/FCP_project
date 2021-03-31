from person import Person
from office import Office
import matplotlib.pyplot as plt

sim_duration = 100
office = Office()  # Initialise office space
params = {'Maximum Age': 65,
          'Minimum Age': 18,
          'Mask Adherence': 0.8,
          'Social Distancing Adherence': 0.5,
          'Number of Floors': 0.5,
          'Number of People': 5}

number_of_people = params['Number of People']
people = []
for ID in range(1, number_of_people + 1):
    people.append(Person(ID, office.desk_locations, params))  # change to desk
    office.people.append(people[ID - 1].current_location)

# used to store events of each time tick, for running through in GUI
display_frames = []
people_frames = []

for time in range(sim_duration):
    # contents could be shifted to person class
    for person in people:  # move people as necessary
        if person.current_location == person.task_location:
            if person.task_progress < person.task_duration:
                person.task_progress += 1

            else:  # task complete, find new task and start moving
                person.task_progress = 0
                person.get_task(office.task_locations)

                office.pathfinding_array[person.current_location[0][0]][person.current_location[0][1]] = 1

                path = person.get_path(office)
                if len(path) > 0:
                    person.move(path)

                office.display_array[person.current_location[0][0]][person.current_location[0][1]] = - person.id
                office.pathfinding_array[person.current_location[0][0]][person.current_location[0][1]] = - person.id

        else:  # between tasks, keep moving
            office.display_array[person.current_location[0][0]][person.current_location[0][1]] = 1
            office.pathfinding_array[person.current_location[0][0]][person.current_location[0][1]] = 1

            path = person.get_path(office)
            if len(path) > 0:
                person.move(path)

            office.display_array[person.current_location[0][0]][person.current_location[0][1]] = - person.id
            office.pathfinding_array[person.current_location[0][0]][person.current_location[0][1]] = - person.id

    # print(office.display_array)
    print(time)
    display_frames.append(office.display_array)
    people_frames.append(people)

    # office.detect_interactions()  # TBC

plt.imshow(office.pathfinding_array.tolist())  # ideas for plotting - doesn't work for letters
plt.show()
