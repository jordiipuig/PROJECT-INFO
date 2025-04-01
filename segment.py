

from node import Node  # Importamos la clase Node de node.py

class Segment:
    def __init__(self, name, origin, destination):
        self.name = name  # Nombre del segmento
        self.origin = origin  # Nodo de origen (instancia de Node)
        self.destination = destination  # Nodo de destino (instancia de Node)
        self.cost = origin.Distance(destination)  # Calcula el costo como la distancia entre los nodos

    def __repr__(self):
        # Representación legible del objeto
        return f"Segment(name={self.name}, origin={self.origin.name}, destination={self.destination.name}, cost={self.cost})"
