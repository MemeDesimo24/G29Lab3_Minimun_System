# @author Federico Cantani

import json
from resources import get_file
from g29lab3_minimum_system.Services.Order import Order
from g29lab3_minimum_system.Services.Ingredient import Ingredient

def load_ingredients():
    """
    Loads the ingredients file
    :return a dictionary of Ingredient objects:
    """
    try:
        with open(get_file("inventory.json"), "r") as f:
            ingredients = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("Inventory problem")
    inventory = {}
    for ingredient, values in ingredients.items():
        inventory[ingredient] = Ingredient(ingredient, values[0], values[1])
    return inventory

def save_inventory(inventory):
    data = {}
    for ingredient, values in inventory.items():
        data[ingredient] = [values.max_capacity, values.current_level]
    with open(get_file("inventory.json"), "w") as f:
        json.dump(data, f)

def save_transaction(order: Order):
    try:
        with open(get_file("order_history.json"), "r") as f:
            order_history = json.load(f)
    except FileNotFoundError:
        order_history = []

    order_history.append(order.to_dict())
    with open(get_file("order_history.json"), "w") as f:
        json.dump(order_history, f)

def place_order(user, beverage):
    inventory = load_ingredients()
    for ing_name in beverage.ingredients:
        if ing_name not in inventory:
            raise ValueError(f"Invalid ingredient: {ing_name}")
        if not inventory[ing_name].is_available(1):
            raise ValueError(f"Quantità insufficiente per: {ing_name}")

    for ing_name in beverage.ingredients:
        inventory[ing_name].decrease(1)
    save_inventory(inventory)
    new_order = Order(user, beverage)
    save_transaction(new_order)
    return new_order