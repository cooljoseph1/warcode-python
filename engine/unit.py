#!/usr/bin/env python3
from constants import CONSTANTS
import game_map


class Unit:
    """
    Basic unit class
    """

    def __int__(self, unit_type, location, player):
        self.unit_type = unit_type
        self.location = location[:]
        self.player = player
        self.engine = self.player.get_engine()
        self.game_map = self.player.get_game_map()
        self.id = self.engine.create_id()
        self.health = CONSTANTS[self.unit_type]["INITIAL_HEALTH"]
        self.gold = 0
        self.wood = 0
        self.action_taken = False

    def get_id(self):
        return self.id

    def get_health(self):
        return self.health

    def get_unit_type(self):
        return self.unit_type

    def get_location(self):
        return self.location

    def get_gold(self):
        return self.gold

    def get_wood(self):
        return self.wood

    def reset(self):
        """
        Actions taken at the beginning of a player's turn to prepare the unit
        for anything it might want to do
        """
        self.action_taken = False

    def set_action_taken(self):
        if self.action_taken:
            raise Exception("Unit {} cannot take two actions in one turn".format(self.get_id()))
        self.action_taken = True

    def hurt(self, amount):
        """
        Damage a unit by an amount, removing it if it dies
        """
        self.set_action_taken()
        self.health -= amount
        if self.health <= 0:
            self.player.remove_unit(self)

    def attack(self, location):
        """
        Attacks a location, throwing an exception if it is an illegal move
        """
        self.set_action_taken()
        if self.distance_to(location) > CONSTANTS[self.unit_type]["ATTACK_DISTANCE"]:
            raise Exception("You can't attack that far.".)

        for unit in self.game_map.get_units():
            if unit.distance_to(location) <= CONSTANTS[unit_type]["SPLASH_RADIUS"]:
                unit.hurt(CONSTANTS[unit_type]["ATTACK_DAMAGE"])

    def move(self, location):
        """
        Move the unit to a new location
        """
        self.set_action_taken()
        if self.distance_to(location) > CONSTANTS[self.unit_type]["SPEED"]:
            raise Exception("You can't move that fast.")
        if not instanceof(self.game_map.get_square_at_location(location), game_map.Empty):
            raise Exception("Location {} is not empty!".format(location))

        self.game_map.set_empty(self.location)
        self.game_map.set_occupied(location, self)
        self.location = location[:]

    def create(self, unit_type, location):
        """
        Creates a new unit of type unit_type at location, throwing an error if
        it is an illegal move
        """
        self.set_action_taken()
        if self.player.get_gold() < CONSTANTS[unit_type]["GOLD_COST"]:
            raise Exception("Unit type {} costs too much gold for you to make".format(unit_type))
        if self.player.get_wood() < CONSTANTS[unit_type]["WOOD_COST"]:
            raise Exception("Unit type {} costs too much wood for you to make".format(unit_type))
        if self.distance_to(location) > 2:
            raise Exception("You can only build next to yourself".format(self.get_id()))
        if (self.unit_type, unit_type) not in CONSTANTS["ALLOWED_CREATIONS"]:
            raise Exception("A {} can't make a {}!".format(self.unit_type, unit_type))
        if not instanceof(self.game_map.get_square_at_location(location), game_map.Empty):
            raise Exception("Location {} is not empty!".format(location))

        self.player.add_gold(-CONSTANTS[unit_type]["GOLD_COST"])
        self.player.add_wood(-CONSTANTS[unit_type]["WOOD_COST"])
        self.player.add_unit(Unit(unit_type, location, player))

    def mine(self, location):
        """
        Mines gold from a location (if that location is a gold mine)
        """
        self.set_action_taken()
        if self.distance_to(location) > 2:
            raise Exception("You can only mine next to yourself.")
        if not CONSTANTS[self.unit_type]["CAN_MINE"]:
            raise Exception("A {} can't mine!".format(self.unit_type))
        if not instanceof(self.game_map.get_square_at_location(location), game_map.GoldMine):
            raise Exception("You can only mine from gold mines.")

        self.add_gold(CONSTANTS[unit_type]["MINE_AMOUNT"])
        self.game_map.remove_gold(CONSTANTS[unit_type]["MINE_AMOUNT"], location)

    def cut(self, location):
        """
        Cuts wood from a location (if that location is a tree)
        """
        self.set_action_taken()
        if self.distance_to(location) > 2:
            raise Exception("You can only cut wood next to yourself.")
        if not CONSTANTS[self.unit_type]["CAN_CUT"]:
            raise Exception("A {} can't cut wood!".format(self.unit_type))
        if not instanceof(self.game_map.get_square_at_location(location), game_map.Tree):
            raise Exception("You can only cut wood from trees.")

        self.add_wood(CONSTANTS[unit_type]["CUT_AMOUNT"])
        self.game_map.remove_wood(CONSTANTS[unit_type]["CUT_AMOUNT"], location)

    def give(self, location, gold, wood):
        """
        Give wood from yourself to another unit.  If that unit is a castle or
        fortress, add the amount to your team's gold/wood supply
        """
        self.set_action_taken()
        if self.distance_to(location) > 2:
            raise Exception("You can only give materials to a neighbor.")
        if self.gold < gold:
            raise Exception("You can't give gold you don't own.  That's stealing!")
        if self.wood < wood:
            raise Exception("Not enough wood to share.")

        unit = self.game_map.get_unit_at_location(location)
        self.add_gold(-gold)
        self.add_wood(-wood)
        if unit.get_unit_type() in ("CASTLE", "FORTRESS"):
            self.player.add_gold(gold)
            self.player.add_wood(wood)
        else:
            unit.add_gold(gold)
            unit.add_wood(wood)

    def distance_to(self, location):
        """
        Returns distance squared from this unit to a location
        """
        return (self.location[0] - location[0])**2 + (self.location[1] - location[1])**2

    def represent(self):
        """
        Representation of self, not including its location
        """
        return {
            "id": self.get_id(),
            "health": self.get_health(),
            "unit_type": self.get_unit_type()
        }
