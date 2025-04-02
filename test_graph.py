# test_graph.py

from graph import *  # Importar la clase Graph
from node import Node  # Importar la clase Node

def CreateGraph_1():
    G = Graph()  # Crear una instancia de Graph

    # Añadir nodos al grafo
    G.AddNode(Node("A", 1, 20))
    G.AddNode(Node("B", 8, 17))
    G.AddNode(Node("C", 15, 20))
    G.AddNode(Node("D", 18, 15))
    G.AddNode(Node("E", 2, 4))
    G.AddNode(Node("F", 6, 5))
    G.AddNode(Node("G", 12, 12))
    G.AddNode(Node("H", 10, 3))
    G.AddNode(Node("I", 19, 1))
    G.AddNode(Node("J", 13, 5))
    G.AddNode(Node("K", 3, 15))
    G.AddNode(Node("L", 4, 10))

    # Añadir segmentos entre los nodos (usando sus nombres)
    G.AddSegment("A", "B")
    G.AddSegment("A", "E")
    G.AddSegment("A", "K")
    G.AddSegment("B", "A")
    G.AddSegment("B", "C")
    G.AddSegment("B", "F")
    G.AddSegment("C", "D")
    G.AddSegment("C", "G")
    G.AddSegment("D", "G")
    G.AddSegment("D", "H")
    G.AddSegment("D", "I")
    G.AddSegment("E", "F")
    G.AddSegment("F", "L")
    G.AddSegment("G", "B")
    G.AddSegment("G", "F")
    G.AddSegment("G", "H")
    G.AddSegment("I", "D")
    G.AddSegment("I", "J")
    G.AddSegment("J", "I")
    G.AddSegment("K", "A")
    G.AddSegment("K", "L")
    G.AddSegment("L", "K")
    G.AddSegment("L", "F")

    return G

# Crear un grafo desde un archivo
print("Probando la creación de un grafo desde un archivo de texto...")

# Asegúrate de que el archivo 'graph_data.txt' exista y tenga el formato correcto
G_from_file = Graph.CreateGraphFromFile('graph_data.txt')

# Imprimir los nodos y sus vecinos
print("\nLista de nodos y sus vecinos desde archivo:")
for node in G_from_file.nodes:
    print(f"{node.name}: {[neighbor.name for neighbor in node.neighbors]}")

# Probar la función de obtener el nodo más cercano
print("\nProbando GetClosest con las coordenadas (15, 5):")
closest_node = G_from_file.GetClosest(15, 5)
if closest_node:
    print(f"El nodo más cercano es: {closest_node.name}")
else:
    print("No se encontró el nodo más cercano.")

# Probar la función de obtener el nodo más cercano con otro conjunto de coordenadas
print("\nProbando GetClosest con las coordenadas (8, 19):")
closest_node = G_from_file.GetClosest(8, 19)
if closest_node:
    print(f"El nodo más cercano es: {closest_node.name}")
else:
    print("No se encontró el nodo más cercano.")

# Probar la función de dibujar el grafo
print("\nDibujando el grafo completo...")
G_from_file.Plot()

