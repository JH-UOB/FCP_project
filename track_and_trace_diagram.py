# -*- coding: utf-8 -*-

from anytree import Node, RenderTree
from anytree.exporter import DotExporter

"""
Created on Tues May 8 20:09:00 2021

Author: Alex Straw
Description:
    This code draws spider diagrams for infection in the office space.
"""
from anytree import Node, RenderTree
from anytree.exporter import DotExporter

def draw_tree(parent,children):
    root = Node("root", lines=parent)
    s0 = Node("sub0B", parent=root, lines=["1", "2", "3"])

    print(RenderTree(root).by_attr("lines"))

infector = 1
parent = ["Infector ID: " + str(infector)]
children = ["1","2","3"]

draw_tree(parent,children)


