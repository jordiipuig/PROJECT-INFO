import unittest
from navSegment import NavSegment

class TestNavSegment(unittest.TestCase):
    def test_creation(self):
        s = NavSegment(100, 200, 57.3)
        self.assertEqual(s.origin_number, 100)
        self.assertEqual(s.destination_number, 200)
        self.assertAlmostEqual(s.distance, 57.3)

if __name__ == "__main__":
    unittest.main()
