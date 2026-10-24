# @author Federico Cantani
class ExistingUserError(BaseException):
    """
    exception raised when the user account already exists
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)