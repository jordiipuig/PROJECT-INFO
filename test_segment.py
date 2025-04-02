

from node import Node  # Importamos la clase Node
from segment import Segment  # Importamos la clase Segment


n1 = Node('aaa', 0, 0)
n2 = Node('bbb', 3, 4)
n3 = Node('ccc', 6, 8)


s1 = Segment('Segment 1', n1, n2)  # Segmento entre n1 y n2
s2 = Segment('Segment 2', n2, n3)  # Segmento entre n2 y n3


print(s1)
print(s2)
