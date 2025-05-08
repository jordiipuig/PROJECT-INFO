

import math

class Node:
    def __init__(self, name, x=0, y=0):
        self.name = name
        self.x = x
        self.y = y
        self.neighbors = []

    def Distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def __eq__(self, other):
        return isinstance(other, Node) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):  # ✅ necesario para heapq si hay empate de costes
        return self.name < other.name

    def AddNeighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)





    def __repr__(self):
        return f"Node({self.name})"
