# -*- coding: utf-8 -*-

from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import graphviz
import os

"""
Created on Tues May 8 20:09:00 2021

Author: Alex Straw
Description:
    This code draws spider diagrams for infection in the office space.
"""


def chance_of_death(people, ID):
    base_death_rate = 1 / 1000
    age = people[ID].age
    death_rate = base_death_rate * age
    return death_rate

def string_formatter(ID,death_rate):
    string = "Infector ID: " + str(ID) + " - Chance of death: " + str(death_rate)
    return(string)

def draw_tree(infector_ID_tree, infected_ID_tree,people):
    root = Node("root", parent=None, lines="Track and Trace Tree")

    for n in range(0, len(infector_ID_tree)):
        infector_str = string_formatter(infector_ID_tree[n],chance_of_death(people, infector_ID_tree[n]))
        infected_ID_node = Node(infector_ID_tree[n], parent=root, lines=infector_str)
        if len(infected_ID_tree[n]) > 0:
            length = len(infected_ID_tree[n])
            for p in range(0, length):
                # print(infected_ID_tree[n][p])
                Node(infected_ID_tree[n][p], parent=infected_ID_node,
                     lines="infected person ID: " + str(infected_ID_tree[n][p]))

    print(RenderTree(root).by_attr("lines"))


def get_tree_data(people):
    infector_ID_tree = []
    infected_ID_tree = []
    for person in people:
        if people[person].contagious:
            infector_ID_tree.append(people[person].ID)
        else:
            pass

    for i in range(0, len(infector_ID_tree)):
        infected_ID_tree.append([])

    for person in people:
        if people[person].infected is True and people[person].contagious is False:
            index = infector_ID_tree.index(people[person].infector_ID)
            infected_ID_tree[index].append(people[person].ID)
        else:
            pass

    return infector_ID_tree, infected_ID_tree


def track_and_trace(people):
    infector_ID_tree, infected_ID_tree = get_tree_data(people)
    draw_tree(infector_ID_tree, infected_ID_tree,people)
