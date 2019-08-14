#!/usr/bin/env python3
from warcode import constants

class GoldMine:
    """
    A gold mine.
    """
    def __init__(self, id, x, y, engine):
        self.id = id
        self.x = x
        self.y = y
        self.engine = engine
        self.gold = constants.GOLD_MINE_HEALTH

    def get_id(self):
        """
        Returns our id
        """
        return self.id

    def get_x(self):
        """
        Returns our x coordinate
        """
        return self.x

    def get_y(self):
        """
        Returns our y coordinate
        """
        return self.y

    def get_gold(self):
        """
        Returns the gold we have left
        """
        return self.gold

    def subtract_gold(self, amount):
        """
        Subtracts gold from our supply, removing us from the game if we run out
        of gold
        """
        self.gold -= amount
        if self.gold <= 0:
            self.engine.remove_gold_mine(self)

    def damage(self, amount):
        """
        Damage ourself
        """
        self.subtract_gold(amount)

    def distance_to(self, x, y):
        """
        Returns the distance squared from this gold mine to a location
        """
        return (self.x - x)**2 + (self.y - y)**2

    def to_dict(self):
        return {
            "id": self.get_id(),
            "gold": self.get_gold(),
            "x": self.get_x(),
            "y": self.get_y()
        }
