# @author Federico Cantani
class IngredientOutOfStock(BaseException):
    """
    exception raised when the given ingredient is out of stock
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)