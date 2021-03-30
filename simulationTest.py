from person import Person
from office import Office

# time = 0
# sim_duration = 10
office = Office()  #Initialise office space
params = {'Maximum Age': 65,
          'Minimum Age': 18,
          'Mask adherance': 0.8,
          'Social distancing adherance': 0.5}

number_of_people = 5
people = []
for id in range(1, number_of_people+1):
    people.append(Person(id, office.desks, params))
    office.people.append(people[id-1].current_location)

people[1].get_path(office)  # example for pathfinding from desk to printer

# WIP - untested
# for time in sim_duration
#     # contents could be shifted to person class
#     for person in people:  # move people as necessary
#         if person.current_location == person.task_location:
#             if person.task_progress < person.task_duration:
#                 person.task_progress += 1
#             else:  # task complete, find new task and start moving
#                 person.get_task(office.get_task_locations())
#                 person.get_path(office)
#                 person.move()
#                 office.grid[person.current_location] = - person.id
#         else:  # between tasks, keep moving
#             person.get_path()
#             person.move()
#             office.grid[person.current_location] = - person.id
#
#     office.detect_interactions()  # TBC
#     time += 1