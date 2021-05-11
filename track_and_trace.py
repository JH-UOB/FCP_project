# -*- coding: utf-8 -*-

from anytree import Node, RenderTree

"""
Created on Tues May 8 20:09:00 2021

Author: Alex Straw
Description:
    This code prints a terminal based tree diagram showing COVID transfer between
    people inside the office.  A chance of death has been calculated for each infected
    individual and also printed in the terminal.  Display also shows if an 'infector'
    is wearing a mask or not
"""


def chance_of_death(people, ID):
    age = people[ID].age
    death_rate = min(round(base_death_rate * age**2 * 100,2),100)

    death_string = " - Chance of death: " + str(death_rate) + "% (age:" + str(age) + ")"
    return death_string


def mask_behaviour_string(people,ID):
    """Creates a mask string for terminal output"""
    mask_string = " - "
    if people[ID].mask:
        mask_string += "Mask: Yes, "
    else:
        mask_string += "Mask: No, "
    return mask_string


def string_formatter(ID,death_string):
    """Formats the terminal output string for an infected individual"""
    string = " ID: " + str(ID) + death_string
    return(string)


def draw_tree(infector_ID_tree, infected_ID_tree,people):
    """
    This function draws the track and trace infection tree

    Parameters
    ----------
    infector_ID_tree : a list of IDs corresponding to individuals who were
                    infected on initialisation of the program (contagious)
                    Format: [3, 5, 1, 12] ... size dependent on GUI input
    infected_ID_tree : a list of lists: IDs corresponding to those infected
                    during simulation.  These people are not contagious.
                    Each list is grouped by the contagious person who infected
                    them.
                    Format: [[2,4,6],[9],[13,14],[]]
                    The position of the list in the list corresponds to the
                    index of the corresponding infector in the infector_ID_tree.
                    For example: [2,4,6] are the IDs of those infected by
                    the person with ID 3.

    prints full tree to terminal

    """
    # Track and trace diagram works with root directory syntax
    root = Node("root", parent=None, lines="Track and Trace")

    # Loop for as many people were initially infected
    for n in range(0, len(infector_ID_tree)):
        # Check if an infector was wearing a mask
        mask_string = mask_behaviour_string(people, infector_ID_tree[n])
        # Creates an output string for the infector as displayed in the terminal (more extensive than infected_str)
        infector_str = string_formatter(infector_ID_tree[n],chance_of_death(people, infector_ID_tree[n]))
        infector_str += mask_string

        # Create a node for the infector, a level below that of the root directory
        infected_ID_node = Node(infector_ID_tree[n], parent=root, lines="Infector" + infector_str)
        # Check if this person infected anyone
        if len(infected_ID_tree[n]) > 0:
            length = len(infected_ID_tree[n])
            for p in range(0, length):
                # Create an infected string output as displayed in the terminal (less extensive than infector_str above)
                infected_str = string_formatter(infected_ID_tree[n][p], chance_of_death(people, infected_ID_tree[n][p]))
                # Append a node to the structure a level below the infector
                Node(infected_ID_tree[n][p], parent=infected_ID_node,lines="Infected " + infected_str)

    # Print terminal display
    line_separator = "_"
    print(line_separator*60)
    print(RenderTree(root).by_attr("lines"))
    print(line_separator * 60)


def get_tree_data(people):
    """

    This function fills the two arrays: infector_ID_tree, and infected_ID_tree as described in draw_tree()

    This happens after the full simulation has been loaded.

    """
    infector_ID_tree = []
    infected_ID_tree = []

    # Only those initially infected are contagious so this is used to find the 'infectors'
    for person in people:
        if people[person].contagious:
            infector_ID_tree.append(people[person].ID)
        else:
            pass

    # Create an empty list of lists for the infected tree
    for i in range(0, len(infector_ID_tree)):
        infected_ID_tree.append([])

    # Fill the infected tree - these are individuals who were infected during the sim
    for person in people:
        # Individuals infected during the sim are not contagious so this statement can be used to find them
        if people[person].infected is True and people[person].contagious is False:
            index = infector_ID_tree.index(people[person].infector_ID)
            infected_ID_tree[index].append(people[person].ID)
        else:
            pass

    return infector_ID_tree, infected_ID_tree


def track_and_trace(people):
    """ Fill infected/infector lists and print tree to terminal"""
    infector_ID_tree, infected_ID_tree = get_tree_data(people)
    draw_tree(infector_ID_tree, infected_ID_tree,people)
