#!/usr/bin/env python3
from warcode import constants

class Tree:
    def __init__(self, id, x, y, engine):
        self.id = id
        self.x = x
        self.y = y
        self.engine = engine
        self.wood = constants.TREE_HEALTH

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

    def get_wood(self):
        """
        Returns the amount of wood left in our supply
        """
        return self.wood

    def subtract_wood(self, amount):
        """
        Subtract wood from our supply, removing ourself from the game if we run
        out of wood
        """
        self.wood -= amount
        if self.wood <= 0:
            self.engine.remove_tree(self)

    def damage(self, amount):
        """
        Damage ourself
        """
        self.subtract_wood(amount)

    def distance_to(self, x, y):
        """
        Returns the distance from this tree to a location
        """
        return (self.x - x)**2 + (self.y - y)**2

    def to_dict(self):
        return {
            "id": self.get_id(),
            "wood": self.get_wood(),
            "x": self.get_x(),
            "y": self.get_y()
        }
