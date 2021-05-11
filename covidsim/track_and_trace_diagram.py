# -*- coding: utf-8 -*-

from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import pydot
import graphviz
import os

"""
Created on Tues May 8 20:09:00 2021

Author: Alex Straw
Description:
    This code draws spider diagrams for infection in the office space.
"""

def draw_tree(infected):

    root = Node("root",parent=None,lines="Track and Trace Tree")

    for tree in range(0, len(infected)):
        infected_ID_node = Node(infected[tree][0], parent =root, lines ="Infector ID: " + str(infected[tree][0]))
        for person in range (1,len(infected[tree])):
            Node(infected[tree][person], parent= infected_ID_node, lines= "infected person ID: " + str(infected[tree][person]))

    print(RenderTree(root).by_attr("lines"))

# Get into format:

# Parent --> Child 1, Child 2, Child 3

infected = []

infected.append(["1","2","3","4"])
infected.append(["5","6","7","8"])

draw_tree(infected)
