# @author Federico Cantani
from g29lab3_minimum_system.Services import order_service

def reset_all_ingredients():
    """
    Reset all ingredient counters to maximum capacity.
    :return: True if the counters are resetted
    :raises FileNotFoundError: if the file does not exist
    """
    inventory = order_service.load_ingredients()
    for ingredient in inventory:
        inventory[ingredient].reset_to_max()
    order_service.save_inventory(inventory)

    return True