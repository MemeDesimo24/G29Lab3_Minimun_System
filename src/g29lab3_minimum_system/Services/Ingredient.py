# @author Federico Cantani
import g29lab3_minimum_system.Models.IngredientOutOfStock as IngredientOutOfStock

class Ingredient:
    """
    Ingredient class
    Methods:
        - is_available(): checks if the ingredient is available
        - decrease(): decreases the ingredient by a given amount
        - reset_to_max(): resets the ingredient counter to maximum capacity
    """
    def __init__(self, name:str, max_capacity:float|int, current_level:float|int):
        self.name = name
        self.max_capacity = max_capacity
        self.current_level = current_level

    def is_available(self, required_amount:float|int):
        """
        Checks if the ingredient is available
        :param required_amount (float or int): the amount required to be available:
        :return True if the ingredient is available, False otherwise:
        :raises ValueError if the amount is not given:
        """
        if not required_amount:
            raise TypeError("The amount cannot be inexistent")
        return self.current_level >= required_amount

    def decrease(self, amount:float|int):
        """
        Decreases the ingredient by a given amount
        :param amount (float or int): the amount to be decreased:
        :return void:
        :raises IngredientOutOfStock:
                ValueError if the amount is not given:
        """
        if not amount:
            raise ValueError("The amount cannot be inexistent")
        if not self.is_available(amount):
            raise IngredientOutOfStock(f"Ingredient out-of-stock: {self.name}")
        self.current_level -= amount

    def reset_to_max(self):
        """
        Resets the ingredient counter to maximum capacity
        :return void:
        """
        self.current_level = self.max_capacity