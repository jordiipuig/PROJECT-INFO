from node import Node
import matplotlib.pyplot as plt

class Path:
    def __init__(self, nodes=None, cost=0.0):
        self.nodes = nodes if nodes is not None else []
        self.cost = cost


def AddNodeToPath(path: Path, node: Node, cost: float = 0.0) -> None:
    path.nodes.append(node)
    path.cost += cost

def ContainsNode(path: Path, node: Node) -> bool:
    return any(n.name == node.name for n in path.nodes)

def CostToNode(path: Path, node: Node) -> float:
    if not ContainsNode(path, node):
        return -1
    total = 0.0
    for i in range(len(path.nodes) - 1):
        total += path.nodes[i].Distance(path.nodes[i + 1])
        if path.nodes[i + 1].name == node.name:
            break
    return total

def PlotPath(graph, path: Path) -> None:
    fig, ax = plt.subplots()
    ax.set_title(f"Camino más corto: {' → '.join(n.name for n in path.nodes)}")
    ax.grid(True, color='red', linestyle='--')

    for node in graph.nodes:
        color = 'green' if any(n.name == node.name for n in path.nodes) else 'gray'
        ax.plot(node.x, node.y, 'o', color=color)
        ax.text(node.x + 0.2, node.y + 0.2, node.name)

    for segment in graph.segments:
        x = [segment.origin.x, segment.destination.x]
        y = [segment.origin.y, segment.destination.y]
        if any(n.name == segment.origin.name for n in path.nodes) and any(n.name == segment.destination.name for n in path.nodes):
            ax.plot(x, y, 'green', linewidth=2.5)
            mx = (x[0] + x[1]) / 2
            my = (y[0] + y[1]) / 2
            ax.text(mx, my, f"{segment.cost:.2f}", color='green', fontsize=8)
        else:
            ax.plot(x, y, 'lightgray', alpha=0.3)

    plt.show()
