from node import Node

class Segment:
    def __init__(self, name, origin, destination):
        self.name = name
        self.origin = origin
        self.destination = destination  # <-- ESTA LÍNEA ES CLAVE
        self.cost = origin.Distance(destination)

    def __repr__(self):
        return f"Segment(name={self.name}, origin={self.origin.name}, destination={self.destination.name}, cost={self.cost:.2f})"
