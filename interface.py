import tkinter as tk
from tkinter import messagebox

class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.neighbors = []  # Lista de nodos vecinos

    def add_neighbor(self, node):
        """Añade un nodo a la lista de vecinos si no está ya en la lista."""
        if node not in self.neighbors:
            self.neighbors.append(node)


class Graph:
    def __init__(self):
        self.nodes = []  # Lista de nodos
        self.edges = []  # Lista de segmentos

    def add_node(self, node):
        """Añade un nodo al grafo."""
        self.nodes.append(node)

    def add_edge(self, node1, node2):
        """Añade un segmento entre dos nodos."""
        node1.add_neighbor(node2)
        node2.add_neighbor(node1)
        self.edges.append((node1, node2))


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Visualization")

        self.graph = Graph()

        # Crear el lienzo donde dibujaremos el grafo
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack()

        # Crear algunos nodos y segmentos
        self.create_sample_graph()

        # Añadir un botón para mostrar los nodos y sus vecinos
        self.button = tk.Button(self.root, text="Select Node", command=self.select_node)
        self.button.pack()

    def create_sample_graph(self):
        """Crea un grafo de ejemplo."""
        # Crear nodos
        node_a = Node("A", 100, 100)
        node_b = Node("B", 200, 200)
        node_c = Node("C", 300, 300)

        # Añadir nodos al grafo
        self.graph.add_node(node_a)
        self.graph.add_node(node_b)
        self.graph.add_node(node_c)

        # Crear segmentos
        self.graph.add_edge(node_a, node_b)
        self.graph.add_edge(node_b, node_c)

        # Dibujar el grafo
        self.draw_graph()

    def draw_graph(self):
        """Dibuja los nodos y los segmentos en el lienzo."""
        self.canvas.delete("all")  # Limpiar el lienzo

        # Dibujar los segmentos
        for node1, node2 in self.graph.edges:
            self.canvas.create_line(node1.x, node1.y, node2.x, node2.y, fill="black")

        # Dibujar los nodos
        for node in self.graph.nodes:
            self.canvas.create_oval(
                node.x - 10, node.y - 10, node.x + 10, node.y + 10, fill="blue", outline="black"
            )
            self.canvas.create_text(node.x, node.y, text=node.name, fill="white")

    def select_node(self):
        """Permite al usuario seleccionar un nodo para ver sus vecinos."""
        def on_click(event):
            x, y = event.x, event.y
            clicked_node = self.get_node_at_position(x, y)
            if clicked_node:
                self.highlight_node_and_neighbors(clicked_node)

        self.canvas.bind("<Button-1>", on_click)

    def get_node_at_position(self, x, y):
        """Devuelve el nodo que se encuentra en la posición clickeada."""
        for node in self.graph.nodes:
            if (x - node.x) ** 2 + (y - node.y) ** 2 <= 10 ** 2:  # Radio de 10px
                return node
        return None

    def highlight_node_and_neighbors(self, node):
        """Resalta el nodo seleccionado y sus vecinos."""
        self.canvas.delete("all")  # Limpiar el lienzo

        # Dibujar los segmentos
        for node1, node2 in self.graph.edges:
            color = "black"
            if node == node1 or node == node2:
                color = "red"  # Resaltar los segmentos relacionados con el nodo
            self.canvas.create_line(node1.x, node1.y, node2.x, node2.y, fill=color)

        # Dibujar los nodos y resaltar los vecinos
        for n in self.graph.nodes:
            color = "blue"
            if n == node:
                color = "green"  # Resaltar el nodo seleccionado
            elif n in node.neighbors:
                color = "yellow"  # Resaltar los vecinos

            self.canvas.create_oval(
                n.x - 10, n.y - 10, n.x + 10, n.y + 10, fill=color, outline="black"
            )
            self.canvas.create_text(n.x, n.y, text=n.name, fill="white")


def run():
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()


if __name__ == "__main__":
    run()



