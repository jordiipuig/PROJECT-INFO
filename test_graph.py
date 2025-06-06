import unittest
from graph import Graph, AddNode, CreateGraph_1, FindShortestPath
from node import Node

class TestGraph(unittest.TestCase):
    def test_add_duplicate_node(self):
        g = Graph()
        self.assertTrue(AddNode(g, Node('A', 0, 0)))
        self.assertFalse(AddNode(g, Node('A', 1, 1)))

    def test_shortest_path(self):
        g = CreateGraph_1()
        path = FindShortestPath(g, 'B', 'F')
        self.assertIsNotNone(path)
        self.assertEqual([n.name for n in path.nodes], ['B', 'F'])
        self.assertGreater(path.cost, 0)

if __name__ == '__main__':
    unittest.main()
