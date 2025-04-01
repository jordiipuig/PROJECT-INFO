# node.py

import math

class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x        # X
        self.y = y        #  Y
        self.neighbors = []  # nodos vecinos

    def AddNeighbor(self, n2):

        if n2 not in self.neighbors:
            self.neighbors.append(n2)
            return True
        return False

    def Distance(self, n2):

        return math.sqrt((self.x - n2.x) ** 2 + (self.y - n2.y) ** 2)
