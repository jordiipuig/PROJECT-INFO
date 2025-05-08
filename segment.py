from node import Node

class Segment:
    def __init__(self, name, origin, destination, cost=1.0):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.cost = cost


    def __repr__(self):
        return f"Segment(name={self.name}, origin={self.origin.name}, destination={self.destination.name}, cost={self.cost:.2f})"
