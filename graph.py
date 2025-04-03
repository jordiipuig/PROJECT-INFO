from node import Node
from segment import Segment
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.nodes = []
        self.segments = []

def AddNode(g, n):
    for node in g.nodes:
        if node.name == n.name:
            return False
    g.nodes.append(n)
    return True

def AddSegment(g, name, nameOrigin, nameDestination):
    origin = next((n for n in g.nodes if n.name == nameOrigin), None)
    destination = next((n for n in g.nodes if n.name == nameDestination), None)
    if origin is None or destination is None:
        return False
    segment = Segment(name, origin, destination)
    g.segments.append(segment)
    origin.AddNeighbor(destination)
    return True

def RemoveNode(g, node_name):
    g.nodes = [n for n in g.nodes if n.name != node_name]
    g.segments = [s for s in g.segments if s.origin.name != node_name and s.destination.name != node_name]
    return True

def SaveGraphToFile(g, path):
    with open(path, 'w') as f:
        f.write("NODES\n")
        for node in g.nodes:
            f.write(f"{node.name} {node.x} {node.y}\n")
        f.write("\nSEGMENTS\n")
        for segment in g.segments:
            f.write(f"{segment.name} {segment.origin.name} {segment.destination.name}\n")

def LoadGraphFromFile(path):
    g = Graph()
    section = None
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line == "" or line.startswith("#"):
                continue
            if line.upper() == "NODES":
                section = "nodes"
                continue
            elif line.upper() == "SEGMENTS":
                section = "segments"
                continue
            parts = line.split()
            if section == "nodes":
                name, x, y = parts[0], float(parts[1]), float(parts[2])
                AddNode(g, Node(name, x, y))
            elif section == "segments":
                name, origin, destination = parts
                AddSegment(g, name, origin, destination)
    return g

def GetClosest(g, x, y):
    temp = Node("temp", x, y)
    return min(g.nodes, key=lambda n: n.Distance(temp))

def CreateGraph_1():
    G = Graph()
    AddNode(G, Node("A", 1, 20))
    AddNode(G, Node("B", 8, 17))
    AddNode(G, Node("C", 15, 20))
    AddNode(G, Node("D", 18, 15))
    AddNode(G, Node("E", 2, 4))
    AddNode(G, Node("F", 6, 5))
    AddNode(G, Node("G", 12, 12))
    AddNode(G, Node("H", 10, 3))
    AddNode(G, Node("I", 19, 1))
    AddNode(G, Node("J", 13, 5))
    AddNode(G, Node("K", 3, 15))
    AddNode(G, Node("L", 4, 10))

    AddSegment(G, "AB", "A", "B")
    AddSegment(G, "AE", "A", "E")
    AddSegment(G, "AK", "A", "K")
    AddSegment(G, "BA", "B", "A")
    AddSegment(G, "BC", "B", "C")
    AddSegment(G, "BF", "B", "F")
    AddSegment(G, "BK", "B", "K")
    AddSegment(G, "BG", "B", "G")
    AddSegment(G, "CD", "C", "D")
    AddSegment(G, "CG", "C", "G")
    AddSegment(G, "DG", "D", "G")
    AddSegment(G, "DH", "D", "H")
    AddSegment(G, "DI", "D", "I")
    AddSegment(G, "EF", "E", "F")
    AddSegment(G, "FL", "F", "L")
    AddSegment(G, "GB", "G", "B")
    AddSegment(G, "GF", "G", "F")
    AddSegment(G, "GH", "G", "H")
    AddSegment(G, "ID", "I", "D")
    AddSegment(G, "IJ", "I", "J")
    AddSegment(G, "JI", "J", "I")
    AddSegment(G, "KA", "K", "A")
    AddSegment(G, "KL", "K", "L")
    AddSegment(G, "LK", "L", "K")
    AddSegment(G, "LF", "L", "F")
    return G

def CreateGraph_2():
    return LoadGraphFromFile("graph_data.txt")
