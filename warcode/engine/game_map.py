#!/usr/bin/env python3
import os
import json
import random
from warcode.constants import CONSTANTS


class Map:
    def __init__(self, map_name):
        with open(os.path.join(CURRENT_DIR, "maps", map_name)) as f:
            map_data = json.load(f)

        self.name = map_data["name"]
        self.starting_locations = map_data["starting_locations"]
        self.available_starting_locations = self.starting_locations[:]
        self.board = [[convert(item) for item in line] for line in map_data["board"]]
        self.width = map_data["width"]
        self.height = map_data["height"]
        self.units = []
        self.unit_id_dict = dict()

    def get_starting_location(self):
        if len(self.available_starting_locations) == 0:
            raise Exception("No positions available")

        choice = random.choice(self.available_starting_locations)
        self.available_starting_locations.remove(choice)
        return choice

    def get_all_locations(self):
        """
        Returns all locations as a list
        """
        return [(x, y) for x in range(self.width) for y in range(self.height)]

    def get_square_at_location(self, location):
        """
        Returns the square at a location
        """
        return self.board[location[1]][location[0]]

    def get_unit_at_location(self, location):
        """
        Returns the unit at the location if there is a unit there, otherwise
        throws an error
        """
        square = self.get_square_at_location(location)
        if not instanceof(square, UnitOccupied):
            raise Exception("No unit at {}".format(location))
        return square.unit

    def set_location(self, location, square):
        """
        Changes the square at a location
        """
        self.board[location[1]][location[0]] = square

    def set_occupied(self, location, unit):
        """
        Sets the square at location to be occupied by unit
        """
        self.set_location(location, UnitOccupied(unit))

    def set_empty(self, location):
        """
        Sets the square at location to be empty
        """
        self.set_location(location, Empty())

    def add_unit(self, unit):
        """
        Adds a unit to the list of overall units
        """
        self.units.append(unit)
        self.unit_id_dict[unit.get_id()] = unit

    def remove_unit(self, unit):
        """
        Removes a unit from the game
        """
        self.units.remove(unit)
        del self.unit_id_dict[unit.get_id()]
        self.set_empty(unit.get_location())

    def remove_gold(self, amount, location):
        """
        Removes gold from a location, destroying the gold mine if it is depleted
        """
        square = self.get_square_at_location(location)
        square.subtract_gold(amount)
        if square.health <= 0:
            self.set_location(location, Block())

    def remove_wood(self, amount, location):
        """
        Removes wood from a location, destroying the tree if it is depleted
        """
        square = self.get_square_at_location(location)
        square.subtract_wood(amount)
        if square.health <= 0:
            self.set_location(location, Empty())

    def get_units(self):
        """
        Returns all units
        """
        return self.units

    def get_unit_from_id(self, id):
        """
        Returns a unit from its id
        """
        return self.unit_id_dict[id]

    def to_string(self, visible_locations="all"):
        """
        Returns a json string representing self

        Keyword arguments:
        visible_locations -- the visible squares (default: "all")

        """
        if visible_locations == "all":
            return json.dumps([[convert_to_json(square) for square in row]
                               for row in self.board])
        else:
            return json.dumps([[convert_to_json(square) if (x, y) in
                                visible_locations else convert_to_json(Invisible()) for x, square in enumerate(row)]
                               for y, row in enumerate(self.board)])


def convert_from_number(item):
    """
    Returns a class corresponding to the
    type of a square on a board.
    """

    if item == CONSTANTS["MAP_DATA"]["TREE"]:
        return Tree(item[1])
    elif item == CONSTANTS["MAP_DATA"]["GOLD_MINE"]:
        return GoldMine(item[1])
    elif item == CONSTANTS["MAP_DATA"]["BLOCK"]:
        return Block()
    elif item == CONSTANTS["MAP_DATA"]["EMPTY"]:
        return Empty()

def convert_to_json(square):
    """
    Converts a square (i.e. Tree, GoldMine, etc.) into a json
    serializable object
    """
    return square.represent()


class Square:
    """
    Represents a square on the map.  Must implement a method represent()
    """
    pass


class Tree(Square):
    """
    Represents a tree
    """
    def __init__(self, health=150):
        self.health = health

    def subtract_wood(self, amount):
        """
        Cuts off an amount from the tree's health
        """
        actual_amount = min(self.health, amount)
        self.health -= actual_amount
        return actual_amount

    def represent(self):
        return [CONSTANTS["MAP_DATA"]["TREE"], self.health]


class GoldMine(Square):
    """
    Represents a gold mine
    """
    def __init__(self, health=500):
        self.health = health

    def subtract_gold(self, amount):
        """
        Removes an amount of gold from the goldmine
        """
        actual_amount = min(self.health, amount)
        self.health -= actual_amount
        return actual_amount

    def represent(self):
        return [CONSTANTS["MAP_DATA"]["GOLD_MINE"], self.health]


class Block(Square):
    """
    Represents a square that is impassable
    """
    def represent(self):
        return [CONSTANTS["MAP_DATA"]["BLOCK"]]


class Empty(Square):
    """
    Represents an empty square
    """
    def represent(self):
        return [CONSTANTS["MAP_DATA"]["EMPTY"]]

class Invisible(Square):
    """
    Represents a square that cannot be seen by the player
    """
    def represent(self):
        return [CONSTANTS["MAP_DATA"]["INVISIBLE"]]


class UnitOccupied(Square):
    def __init__(self, unit):
        self.unit = unit

    def represent(self):
        return [CONSTANTS["MAP_DATA"]["UNIT_OCCUPIED"], self.unit.represent()]
