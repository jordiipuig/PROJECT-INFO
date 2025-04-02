


from node import Node
from segment import Segment
import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        self.nodes = []  # Lista de nodos
        self.segments = []  # Lista de segmentos

    def AddNode(self, n):

        for node in self.nodes:
            if node.name == n.name:
                return False
        self.nodes.append(n)
        return True

    def AddSegment(self, nameOriginNode, nameDestinationNode):

        origin = None
        destination = None

        for node in self.nodes:
            if node.name == nameOriginNode:
                origin = node
            if node.name == nameDestinationNode:
                destination = node

        if origin is None or destination is None:
            return False

        segment = Segment(f"{nameOriginNode}{nameDestinationNode}", origin, destination)
        self.segments.append(segment)

        origin.AddNeighbor(destination)
        return True

    def GetClosest(self, x, y):

        closest_node = None
        min_distance = float('inf')

        for node in self.nodes:
            distance = node.Distance(Node('', x, y))  # Usamos una "copia" del nodo con las coordenadas (x, y)
            if distance < min_distance:
                min_distance = distance
                closest_node = node

        return closest_node

    def Plot(self):

        for segment in self.segments:
            plt.plot([segment.origin.x, segment.destination.x], [segment.origin.y, segment.destination.y], 'r-')
            mid_x = (segment.origin.x + segment.destination.x) / 2
            mid_y = (segment.origin.y + segment.destination.y) / 2
            plt.text(mid_x, mid_y, f'{segment.cost:.2f}', color='blue', fontsize=8, ha='center', va='center')

        for node in self.nodes:
            plt.scatter(node.x, node.y, color='gray')
            plt.text(node.x, node.y, node.name, color='black', fontsize=10, ha='center', va='center')

        plt.show()

    def PlotNode(self, nameOrigin):

        origin = None
        for node in self.nodes:
            if node.name == nameOrigin:
                origin = node
                break

        if origin is None:
            return False

        for segment in self.segments:
            if segment.origin == origin:
                plt.plot([segment.origin.x, segment.destination.x], [segment.origin.y, segment.destination.y], 'r-')
                mid_x = (segment.origin.x + segment.destination.x) / 2
                mid_y = (segment.origin.y + segment.destination.y) / 2
                plt.text(mid_x, mid_y, f'{segment.cost:.2f}', color='blue', fontsize=8, ha='center', va='center')

        for node in self.nodes:
            if node == origin:
                plt.scatter(node.x, node.y, color='blue')
            elif node in origin.neighbors:
                plt.scatter(node.x, node.y, color='green')
            else:
                plt.scatter(node.x, node.y, color='gray')

            plt.text(node.x, node.y, node.name, color='black', fontsize=10, ha='center', va='center')

        plt.show()
        return True


    def CreateGraphFromFile(filename):

        G = Graph()

        with open(filename, 'r') as f:
            lines = f.readlines()

        # Primero, leemos los nodos
        for line in lines:
            parts = line.strip().split()
            if parts[0] == "NODO":
                name = parts[1]
                x = float(parts[2])
                y = float(parts[3])
                G.AddNode(Node(name, x, y))

        # Luego, leemos los segmentos
        for line in lines:
            parts = line.strip().split()
            if parts[0] == "SEGMENTO":
                G.AddSegment(parts[1], parts[2])

        return G
