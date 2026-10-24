import unittest
from unittest.mock import patch, mock_open, MagicMock
import json

from g29lab3_minimum_system.Services import order_service
from g29lab3_minimum_system.Services.Order import Order
from g29lab3_minimum_system.Services.User import User
from g29lab3_minimum_system.Services.Beverage import Beverage
from g29lab3_minimum_system.Services.Ingredient import Ingredient

class TestOrderService(unittest.TestCase):

    def setUp(self):
        self.user = User("testuser", "pass", False)
        self.beverage = Beverage("Espresso", 1.5, ["coffee", "water"], ["hot"])
        self.mock_inventory_data = json.dumps({
            "coffee": [100, 50],
            "water": [200, 150]
        })

    @patch('g29lab3_minimum_system.Services.order_service.get_file')
    def test_load_ingredients_success(self, mock_get_file):
        mock_get_file.return_value = 'dummy_inventory.json'
        m = mock_open(read_data=self.mock_inventory_data)
        with patch('builtins.open', m):
            inventory = order_service.load_ingredients()
            self.assertIn("coffee", inventory)
            self.assertEqual(inventory["coffee"].current_level, 50)

    @patch('g29lab3_minimum_system.Services.order_service.get_file')
    def test_load_ingredients_file_not_found(self, mock_get_file):
        mock_get_file.return_value = 'dummy_inventory.json'
        with patch('builtins.open', side_effect=FileNotFoundError):
            with self.assertRaisesRegex(FileNotFoundError, "Inventory problem"):
                order_service.load_ingredients()

    @patch('g29lab3_minimum_system.Services.order_service.save_transaction')
    @patch('g29lab3_minimum_system.Services.order_service.save_inventory')
    @patch('g29lab3_minimum_system.Services.order_service.load_ingredients')
    def test_place_order_success(self, mock_load, mock_save_inv, mock_save_trans):
        # Mocking the loaded inventory
        mock_inv = {
            "coffee": Ingredient("coffee", 100, 50),
            "water": Ingredient("water", 100, 50)
        }
        mock_load.return_value = mock_inv
        
        result = order_service.place_order(self.user, self.beverage)
        
        self.assertIsInstance(result, Order)
        self.assertEqual(mock_inv["coffee"].current_level, 49)
        mock_save_inv.assert_called_once()
        mock_save_trans.assert_called_once()

    @patch('g29lab3_minimum_system.Services.order_service.load_ingredients')
    def test_place_order_insufficient_quantity(self, mock_load):
        # Mocking insufficient inventory
        mock_inv = {
            "coffee": Ingredient("coffee", 100, 0),
            "water": Ingredient("water", 100, 50)
        }
        mock_load.return_value = mock_inv
        
        with self.assertRaisesRegex(ValueError, "Quantità insufficiente per: coffee"):
            order_service.place_order(self.user, self.beverage)

    @patch('g29lab3_minimum_system.Services.order_service.load_ingredients')
    def test_place_order_invalid_ingredient(self, mock_load):
        # Missing "coffee" in inventory
        mock_inv = {
            "water": Ingredient("water", 100, 50)
        }
        mock_load.return_value = mock_inv
        
        with self.assertRaisesRegex(ValueError, "Invalid ingredient: coffee"):
            order_service.place_order(self.user, self.beverage)

if __name__ == '__main__':
    unittest.main()
