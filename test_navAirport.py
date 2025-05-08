import unittest
from navAirport import NavAirport

class TestNavAirport(unittest.TestCase):
    def test_add_sid_and_star(self):
        airport = NavAirport("LEIB")
        airport.add_sid(6063)
        airport.add_star(6070)
        airport.add_sid(6063)  # duplicado
        self.assertEqual(airport.name, "LEIB")
        self.assertIn(6063, airport.sids)
        self.assertIn(6070, airport.stars)
        self.assertEqual(len(airport.sids), 1)  # No duplicados

if __name__ == "__main__":
    unittest.main()
