import unittest
from navPoint import NavPoint

class TestNavPoint(unittest.TestCase):
    def test_creation(self):
        p = NavPoint(100, "GODUX", 41.0, 2.0)
        self.assertEqual(p.number, 100)
        self.assertEqual(p.name, "GODUX")
        self.assertEqual(p.latitude, 41.0)
        self.assertEqual(p.longitude, 2.0)

    def test_equality_and_hash(self):
        p1 = NavPoint(1, "A", 0, 0)
        p2 = NavPoint(1, "A", 0, 0)
        p3 = NavPoint(2, "B", 1, 1)
        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)
        self.assertEqual(hash(p1), hash(p2))

if __name__ == "__main__":
    unittest.main()
