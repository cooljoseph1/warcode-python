#!/usr/bin/env python3
from warcode import constants

class Team:
    """
    A team. It represents the resources a player has.
    """
    def __init__(self, id):
        self.id = id
        self.gold = constants.INITIAL_GOLD
        self.wood = constants.INITIAL_WOOD

        self.units = {}

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

    def get_units(self):
        """
        Returns the units a team has
        """
        return self.units

    def add_unit(self, unit):
        """
        Adds a unit to our team
        """
        self.units[unit.get_id()] = unit

    def remove_unit(self, unit):
        """
        Removes a unit from our team
        """
        del self.units[unit.get_id()]
