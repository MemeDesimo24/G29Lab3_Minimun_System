import unittest
from g29lab3_minimum_system.Services.Beverage import Beverage

class TestBeverage(unittest.TestCase):

    def setUp(self):
        self.beverage = Beverage("Latte", 3.50, ["coffee", "milk"], ["hot", "morning"])

    def test_init(self):
        self.assertEqual(self.beverage.name, "Latte")
        self.assertEqual(self.beverage.price, 3.50)
        self.assertEqual(self.beverage.ingredients, ["coffee", "milk"])
        self.assertEqual(self.beverage.flags, ["hot", "morning"])

    def test_match_filter_name(self):
        self.assertTrue(self.beverage.match_filter("latte"))
        self.assertTrue(self.beverage.match_filter("LAT"))

    def test_match_filter_flag(self):
        self.assertTrue(self.beverage.match_filter("hot"))

    def test_match_filter_ingredient(self):
        self.assertTrue(self.beverage.match_filter("milk"))

    def test_match_filter_false(self):
        self.assertFalse(self.beverage.match_filter("espresso"))
        
    def test_match_filter_empty(self):
        self.assertFalse(self.beverage.match_filter(""))

    def test_to_dict(self):
        expected_dict = {
            "name": "Latte",
            "price": 3.50,
            "ingredients": ["coffee", "milk"],
            "flags": ["hot", "morning"]
        }
        self.assertEqual(self.beverage.to_dict(), expected_dict)

if __name__ == '__main__':
    unittest.main()
