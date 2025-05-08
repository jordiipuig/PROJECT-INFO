from node import Node
from segment import Segment
from path import Path
import heapq

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

    cost = origin.Distance(destination)
    segment = Segment(name, origin, destination, cost)
    g.segments.append(segment)

    # Conexión bidireccional
    if destination not in origin.neighbors:
        origin.neighbors.append(destination)
    if origin not in destination.neighbors:
        destination.neighbors.append(origin)

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

    dist = {n: float('inf') for n in G.nodes}
    prev = {n: None for n in G.nodes}
    dist[start] = 0

    queue = [(0, start)]

    while queue:
        current_dist, current = heapq.heappop(queue)
        if current == end:
            break
        for seg in G.segments:
            if seg.origin == current:
                neighbor = seg.destination
                alt = current_dist + seg.cost
                if alt < dist[neighbor]:
                    dist[neighbor] = alt
                    prev[neighbor] = current
                    heapq.heappush(queue, (alt, neighbor))

    if dist[end] == float('inf'):
        return None

    path_nodes = []
    current = end
    while current:
        path_nodes.insert(0, current)
        current = prev[current]

    return Path(path_nodes, dist[end])

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
        ("AB", "A", "B"), ("AE", "A", "E"), ("AK", "A", "K"),
        ("BC", "B", "C"), ("BF", "B", "F"), ("BK", "B", "K"), ("BG", "B", "G"),
        ("CD", "C", "D"), ("CG", "C", "G"),
        ("DG", "D", "G"), ("DH", "D", "H"), ("DI", "D", "I"),
        ("EF", "E", "F"),
        ("FL", "F", "L"),
        ("GF", "G", "F"), ("GH", "G", "H"),
        ("IJ", "I", "J"),
        ("KA", "K", "A"), ("KL", "K", "L"), ("LF", "L", "F")
    ]
    for name, o, d in segments:
        AddSegment(G, name, o, d)
    return G

def CreateGraph_2() -> Graph:
    return LoadGraphFromFile("graph_data.txt")
