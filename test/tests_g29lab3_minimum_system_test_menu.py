import unittest
from unittest.mock import patch, mock_open
import json

from g29lab3_minimum_system.Services import menu
from g29lab3_minimum_system.Services.Beverage import Beverage

class TestMenu(unittest.TestCase):

    def setUp(self):
        self.mock_menu_data = json.dumps([
            {"name": "Espresso", "price": 1.5, "ingredients": ["coffee"], "flags": ["hot", "caffeine"]},
            {"name": "Iced Tea", "price": 2.0, "ingredients": ["tea", "ice"], "flags": ["cold", "caffeine free"]}
        ])

    @patch('g29lab3_minimum_system.Services.menu.get_file')
    def test_load_menu_success(self, mock_get_file):
        mock_get_file.return_value = 'dummy_menu.json'
        m = mock_open(read_data=self.mock_menu_data)
        with patch('builtins.open', m):
            beverages = menu.load_menu()
            self.assertEqual(len(beverages), 2)
            self.assertIsInstance(beverages[0], Beverage)
            self.assertEqual(beverages[0].name, "Espresso")

    @patch('g29lab3_minimum_system.Services.menu.get_file')
    def test_load_menu_file_not_found(self, mock_get_file):
        mock_get_file.return_value = 'dummy_menu.json'
        with patch('builtins.open', side_effect=FileNotFoundError):
            with self.assertRaisesRegex(FileNotFoundError, "No menu found"):
                menu.load_menu()

    @patch('g29lab3_minimum_system.Services.menu.load_menu')
    def test_search_success(self, mock_load):
        mock_load.return_value = [
            Beverage("Espresso", 1.5, ["coffee"], ["hot"]),
            Beverage("Iced Tea", 2.0, ["tea"], ["cold"])
        ]
        results = menu.search("Espresso")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Espresso")
        
        results_flag = menu.search("cold")
        self.assertEqual(len(results_flag), 1)
        self.assertEqual(results_flag[0].name, "Iced Tea")

    def test_search_empty_prompt(self):
        self.assertEqual(menu.search(""), [])

if __name__ == '__main__':
    unittest.main()
