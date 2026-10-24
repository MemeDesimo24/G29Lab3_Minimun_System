# @author Federico Cantani
from datetime import datetime
from g29lab3_minimum_system.Services.User import User
from g29lab3_minimum_system.Services.Beverage import Beverage

class Order:
    def __init__(self, user:User, beverage:Beverage):
        self.beverage = beverage
        self.user = user
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "username": self.user.username,
            "beverage": self.beverage.to_dict(),
            "timestamp": self.timestamp
        }