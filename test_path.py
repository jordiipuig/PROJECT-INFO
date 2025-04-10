
from node import Node
from path import *

n1 = Node("A", 0, 0)
n2 = Node("B", 3, 4)
n3 = Node("C", 6, 8)

print("Test: Crear camino y añadir nodos")
p = Path()
AddNodeToPath(p, n1)
AddNodeToPath(p, n2, n1.Distance(n2))
AddNodeToPath(p, n3, n2.Distance(n3))

print("Nodos en camino:", [n.name for n in p.nodes])
print("Coste total:", p.cost)
print("Contiene B:", ContainsNode(p, n2))  # True
print("Coste hasta B:", CostToNode(p, n2))  # 5.0
print("Coste hasta C:", CostToNode(p, n3))  # 10.0