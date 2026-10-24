# @author Federico Cantani
import json
from g29lab3_minimum_system.Models.ExistingUserError import ExistingUserError
from resources import get_file
from g29lab3_minimum_system.Services.User import User

def psw_control(password:str):
    """
    Controls the password
    :param password (str):
    :return True if the password is valid:
    :raises ValueError: if the password is an empty string:
    :raises ValueError: if the password is not at least 8 characters long:
    :raises ValueError: if the password does not contain at least one digit:
    """
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not any (char.isdigit() for char in password):
        raise ValueError("Password must contain at least one digit")
    return True

def create_account(username:str, password:str, is_admin:bool = False):
    """
    Creates a new user account
    :param username:
    :param password:
    :param is_admin:
    :return True if the user account is created:
    :raises ExistingUserError: if the user account already exists:
    :raises ValueError: if the username is an empty string:

    """
    if not username:
        raise ValueError("Username cannot be an empty string")
    psw_control(password)

    new_user = {"username": username, "password": password, "is_admin" : is_admin}

    with open(get_file("accounts.json"), "r") as file:
        accounts = json.load(file)
    for user in accounts:
        if user["username"] == username:
            raise ExistingUserError("User already exists")

    accounts.append(new_user)
    with open(get_file("accounts.json"), "w") as file:
        json.dump(accounts, file, indent=4)
    return True

def login(username:str, password:str):
    """
    Logs in the user with his password
    :param username (str):
    :param password (str):
    :return User object if the user is logged in, False otherwise:
    :raises ValueError if no username is given:
    """
    if not username:
        raise ValueError("Username cannot be an empty string")
    if not password:
        return False
    with open(get_file("accounts.json"), "r") as file:
        accounts = json.load(file)

    for user in accounts:
        if user["username"] == username and user["password"] == password:
            return User(user["username"], user["password"], user["is_admin"])
    return False