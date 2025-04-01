


from node import *

n1 = Node('aaa', 0, 0)
n2 = Node('bbb', 3, 4)


print(n1.Distance(n2))


print(n1.AddNeighbor(n2))


print(n1.AddNeighbor(n2))


print(n1.__dict__)


for n in n1.neighbors:
    print(n.__dict__)
