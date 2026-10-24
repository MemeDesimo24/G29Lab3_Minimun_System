import unittest
from unittest.mock import patch, mock_open
import json

from g29lab3_minimum_system.Services import authentication
from g29lab3_minimum_system.Models.ExistingUserError import ExistingUserError

class TestAuthentication(unittest.TestCase):

    def test_psw_control_valid(self):
        self.assertTrue(authentication.psw_control("Valid123"))

    def test_psw_control_too_short(self):
        with self.assertRaisesRegex(ValueError, "Password must be at least 8 characters long"):
            authentication.psw_control("1234567")

    def test_psw_control_empty(self):
        with self.assertRaisesRegex(ValueError, "Password must be at least 8 characters long"):
            authentication.psw_control("")

    def test_psw_control_no_digits(self):
        with self.assertRaisesRegex(ValueError, "Password must contain at least one digit"):
            authentication.psw_control("Password")

    @patch('g29lab3_minimum_system.Services.authentication.get_file')
    def test_create_account_success(self, mock_get_file):
        mock_get_file.return_value = 'dummy_path.json'
        # Mock empty file content
        m = mock_open(read_data='[]')
        with patch('builtins.open', m):
            result = authentication.create_account("newuser", "Password123")
            self.assertTrue(result)

    @patch('g29lab3_minimum_system.Services.authentication.get_file')
    def test_create_account_existing_user(self, mock_get_file):
        mock_get_file.return_value = 'dummy_path.json'
        mock_data = json.dumps([{"username": "existinguser", "password": "Password123", "is_admin": False}])
        m = mock_open(read_data=mock_data)
        with patch('builtins.open', m):
            with self.assertRaisesRegex(ExistingUserError, "User already exists"):
                authentication.create_account("existinguser", "Password123")

    def test_create_account_empty_username(self):
        with self.assertRaisesRegex(ValueError, "Username cannot be an empty string"):
            authentication.create_account("", "Password123")

    @patch('g29lab3_minimum_system.Services.authentication.get_file')
    def test_login_success(self, mock_get_file):
        mock_get_file.return_value = 'dummy_path.json'
        mock_data = json.dumps([{"username": "testuser", "password": "Password123", "is_admin": True}])
        m = mock_open(read_data=mock_data)
        with patch('builtins.open', m):
            user = authentication.login("testuser", "Password123")
            self.assertIsNotNone(user)
            self.assertEqual(user.username, "testuser")
            self.assertTrue(user.is_admin)

    @patch('g29lab3_minimum_system.Services.authentication.get_file')
    def test_login_failure_wrong_password(self, mock_get_file):
        mock_get_file.return_value = 'dummy_path.json'
        mock_data = json.dumps([{"username": "testuser", "password": "Password123", "is_admin": False}])
        m = mock_open(read_data=mock_data)
        with patch('builtins.open', m):
            result = authentication.login("testuser", "Wrong123")
            self.assertFalse(result)

    def test_login_empty_username(self):
        with self.assertRaisesRegex(ValueError, "Username cannot be an empty string"):
            authentication.login("", "Password123")
            
    def test_login_empty_password(self):
        self.assertFalse(authentication.login("testuser", ""))

if __name__ == '__main__':
    unittest.main()
