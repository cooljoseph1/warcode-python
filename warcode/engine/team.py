#!/usr/bin/env python3
form warcode import constants

class Team:
    """
    A team. It represents the resources a player has.
    """
    def __init__(self, id, engine):
        self.id = id
        self.engine = engine
        self.gold = constants.INITIAL_GOLD
        self.wood = constants.INITIAL_WOOD

    def get_id(self):
        """
        Returns our id
        """
        return self.id

    def get_gold(self):
        """
        Returns the gold in our supply
        """
        return self.gold

    def add_gold(self, amount):
        """
        Adds gold to our supply
        """
        self.gold += amount

    def subtract_gold(self, amount):
        """
        Subtracts gold from our supply
        """
        self.gold -= amount

    def get_wood(self):
        """
        Returns the wood in our supply
        """
        return self.wood

    def add_wood(self, amount):
        """
        Adds wood to our supply
        """
        self.wood += amount

    def subtract_wood(self, amount):
        """
        Subtracts wood from our supply
        """
        self.wood -= amount
