from node import Node
from segment import Segment
from path import Path, AddNodeToPath, ContainsNode

class Graph:
    def __init__(self):
        self.nodes = []
        self.segments = []

def AddNode(g: Graph, n: Node) -> bool:
    if any(node.name == n.name for node in g.nodes):
        return False
    g.nodes.append(n)
    return True

def AddSegment(g: Graph, name: str, nameOrigin: str, nameDestination: str) -> bool:
    origin = next((n for n in g.nodes if n.name == nameOrigin), None)
    destination = next((n for n in g.nodes if n.name == nameDestination), None)
    if origin is None or destination is None:
        return False


    segment = Segment(name, origin, destination)
    g.segments.append(segment)


    if destination not in origin.neighbors:
        origin.neighbors.append(destination)

    return True

def RemoveNode(g: Graph, node_name: str) -> bool:
    node_to_remove = next((n for n in g.nodes if n.name == node_name), None)
    if not node_to_remove:
        return False
    g.nodes.remove(node_to_remove)
    g.segments = [s for s in g.segments if s.origin != node_to_remove and s.destination != node_to_remove]
    for node in g.nodes:
        node.neighbors = [nb for nb in node.neighbors if nb != node_to_remove]
    return True

def SaveGraphToFile(g: Graph, path: str) -> None:
    with open(path, 'w') as f:
        f.write("NODES\n")
        for node in g.nodes:
            f.write(f"{node.name} {node.x} {node.y}\n")
        f.write("\nSEGMENTS\n")
        for segment in g.segments:
            f.write(f"{segment.name} {segment.origin.name} {segment.destination.name}\n")

def LoadGraphFromFile(path: str) -> Graph:
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

def FindShortestPath(G: Graph, origin: str, destination: str) -> Path | None:
    start = next((n for n in G.nodes if n.name == origin), None)
    end = next((n for n in G.nodes if n.name == destination), None)
    if not start or not end:
        return None

    current_paths = []
    initial_path = Path()
    AddNodeToPath(initial_path, start)
    current_paths.append(initial_path)

    while current_paths:
        best_path = min(current_paths, key=lambda p: p.cost + p.nodes[-1].Distance(end))
        current_paths.remove(best_path)
        last_node = best_path.nodes[-1]

        for neighbor in last_node.neighbors:
            if ContainsNode(best_path, neighbor):
                continue
            cost = last_node.Distance(neighbor)
            new_path = Path()
            new_path.nodes = best_path.nodes.copy()
            new_path.cost = best_path.cost
            AddNodeToPath(new_path, neighbor, cost)

            if neighbor == end:
                return new_path
            current_paths.append(new_path)

    return None

def CreateGraph_1() -> Graph:
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

    segments = [
        ("AB", "A", "B"), ("AE", "A", "E"), ("AK", "A", "K"), ("BA", "B", "A"),
        ("BC", "B", "C"), ("BF", "B", "F"), ("BK", "B", "K"), ("BG", "B", "G"),
        ("CD", "C", "D"), ("CG", "C", "G"), ("DG", "D", "G"), ("DH", "D", "H"),
        ("DI", "D", "I"), ("EF", "E", "F"), ("FL", "F", "L"), ("GB", "G", "B"),
        ("GF", "G", "F"), ("GH", "G", "H"), ("ID", "I", "D"), ("IJ", "I", "J"),
        ("JI", "J", "I"), ("KA", "K", "A"), ("KL", "K", "L"), ("LK", "L", "K"), ("LF", "L", "F")
    ]
    for name, o, d in segments:
        AddSegment(G, name, o, d)
    return G

def CreateGraph_2() -> Graph:
    return LoadGraphFromFile("graph_data.txt")
