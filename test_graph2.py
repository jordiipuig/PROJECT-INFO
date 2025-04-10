from graph import *
from path import PlotPath

# Crear grafo de prueba
G = CreateGraph_1()

# Buscar camino entre dos nodos
origin = "B"
destination = "F"
path = FindShortestPath(G, origin, destination)

if path:
    print("Camino encontrado:")
    for node in path.nodes:
        print(node.name, end=" -> ")
    print(f"\nCoste total: {path.cost}")
    PlotPath(G, path)
else:
    print("No hay camino entre los nodos.")
