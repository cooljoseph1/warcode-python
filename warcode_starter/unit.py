#!/usr/bin/env python3
from warcode import constants

class Unit:
    def __init__(self, id, data, player):
        self.id = id
        self.unit_type = getattr(constants, data["type"])
        self.health = data["health"]
        self.team = data["team"]
        self.x = x
        self.y = y

        self.player = player

    def get_id(self):
        return self.id

    def get_health(self):
        return self.health

    def get_team(self):
        return self.team

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        """
        Returns a tuple of our (x, y) location
        """
        return (self.x, self.y)

    def damage(self, amount):
        """
        Damage ourself by an amount
        """
        self.health -= amount
        if self.health <= 0:
            self.player.remove_unit(self)

    def add_gold(self, amount):
        """
        Add gold to our supply
        """
        self.gold += amount

    def subtract_gold(self, amount):
        """
        Subtract gold from our supply
        """
        self.gold -= amount

    def add_wood(self, amount):
        """
        Add wood to our supply
        """
        self.wood += amount

    def subtract_wood(self, amount):
        """
        Subtract wood from our supply
        """
        self.wood -= amount

    def move(self, x, y):
        self.player.move(self, x, y)

    def attack(self, x, y):
        self.player.attack(self, x, y)

    def build(self, unit_type, x, y):
        self.player.build(self, unit_type, x, y)

    def give(self, other, gold, wood):
        self.player.give(self, other, gold, wood)

    def cut(self, x, y):
        self.player.cut(self, x, y)

    def mine(self, x, y):
        self.player.mine(self, x, y)

    def distance_to(self, x, y):
        """
        Returns the squared distance from ourself to a position
        """
        return (self.x - x)**2 + (self.y - y)**2
