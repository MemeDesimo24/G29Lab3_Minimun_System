# @author Federico Cantani

class User:
    """
    User class
    """
    def __init__(self,username:str,password:str,is_admin:bool = False):
        self.username = username
        self.password = password
        self.is_admin = is_admin
    def print(self):
        return f"Username: {self.username}\tPassword: {"*" * len(self.password)}\t{"Admin" if self.is_admin else "Not admin"}"