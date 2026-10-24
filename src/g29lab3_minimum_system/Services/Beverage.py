# @author Federico Cantani

class Beverage:
    """
    Beverage class
    Methods:
        - match_filter: Checks if beverage matches browsing filters
    """
    def __init__(self, name:str, price:float, ingredients:list, flag:list):
        self.name = name
        self.price = price
        self.ingredients = ingredients
        self.flags = flag if flag is not None else []

    def match_filter(self, prompt):
        """
        Checks if beverage matches browsing filters
        :param prompt:
        :return True if the beverage matches browsing filters, False otherwise:
        """
        if not prompt:
            return False
        prompt = prompt.lower()
        return (prompt in self.name.lower() or
                any(prompt in flag.lower() for flag in self.flags) or
                any(prompt in ingredient.lower() for ingredient in self.ingredients))
    def print(self):
        return f"Name: {self.name}\tPrice: {self.price} kr\tIngredients: {self.ingredients}"

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "ingredients": self.ingredients,
            "flags": self.flags
        }