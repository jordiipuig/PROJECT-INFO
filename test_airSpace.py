import unittest
from airSpace import AirSpace
from navPoint import NavPoint
from navSegment import NavSegment
from navAirport import NavAirport

class TestAirSpace(unittest.TestCase):
    def setUp(self):
        self.space = AirSpace()

        # Crear NavPoints
        p1 = NavPoint(1, "A", 0, 0)
        p2 = NavPoint(2, "B", 1, 0)
        p3 = NavPoint(3, "C", 2, 0)

        # Añadir al espacio aéreo
        self.space.navpoints = [p1, p2, p3]
        for p in self.space.navpoints:
            self.space.navpoints_by_number[p.number] = p
            self.space.navpoints_by_name[p.name] = p

        # Crear segmentos
        self.space.navsegments = [
            NavSegment(1, 2, 100.0),
            NavSegment(2, 3, 100.0)
        ]

    def test_get_neighbors(self):
        a = self.space.navpoints_by_name["A"]
        b = self.space.get_neighbors(a)
        self.assertEqual(len(b), 1)
        self.assertEqual(b[0].name, "B")

    def test_reachables(self):
        a = self.space.navpoints_by_name["A"]
        reach = self.space.get_reachables(a)
        names = sorted(p.name for p in reach)
        self.assertEqual(names, ["A", "B", "C"])

    def test_shortest_path(self):
        a = self.space.navpoints_by_name["A"]
        c = self.space.navpoints_by_name["C"]
        path, cost = self.space.shortest_path(a, c)
        self.assertEqual([p.name for p in path], ["A", "B", "C"])
        self.assertAlmostEqual(cost, 200.0)

if __name__ == "__main__":
    unittest.main()
