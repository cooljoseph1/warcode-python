#!/usr/bin/env python3
import json

from warcode import constants

class Player:
    def __init__(self, name="Default"):
        """
        Construction of a player.  Pass your name in the super construct.
        """
        self.name = name
        self.turn = 0
        self._first_turn()
        while True:
            self._turn()


    def first_turn(self):
        """
        You implement this function in your own code!
        """
        pass

    def turn(self):
        """
        You implement this function in your own code!
        """
        pass

    def move(self, unit, x, y):
        """
        Add a move action to our actions and update ourself to represent the
        change
        """
        self.map.set_square(unit.get_x(), unit.get_y(), constants.EMPTY)
        self.map.set_square(x, y, unit.get_id())
        unit.set_position(x, y)

        self.actions.append({
            "move": {
                "unit": unit.get_id(),
                "x": x,
                "y": y
            }
        })

    def attack(self, unit, x, y):
        """
        Add an attack action to our actions and update ourself to represent the
        change
        """

        for other in self.units + self.trees + self.gold_mines:
            if other.distance_to(x, y) <= unit.get_unit_type().get_splash_radius():
                other.damage(unit.get_unit_type().get_attackdamage())

        self.actions.append({
            "attack": {
                "unit": unit.get_id(),
                "x": x,
                "y": y
            }
        })

    def build(self, unit, unit_type, x, y):
        """
        Add a build action to our actions and update ourself to represent the
        change
        """

        new_unit = Unit(unit_type, x, y, -1)
        self.gold -= unit_type.get_gold_cost()
        self.wood -= unit_type.get_wood_cost()
        self.units.append(new_unit)

        self.actions.append({
            "build": {
                "unit": unit.get_id(),
                "unit_type": unit_type,
                "x": x,
                "y": y
            }
        })

    def give(self, unit, other, gold, wood):
        """
        Add a give action to our actions an update ourself to represent the
        change
        """
        unit.subtract_gold(gold)
        unit.subtract_wood(wood)

        if other.get_unit_type() in (constants.CASTLE, constants.FORTRESS):
            self.gold += gold
            self.wood += wood
        else:
            other.add_gold(gold)
            other.add_wood(wood)

        self.actions.append({
            "give": {
                "unit": unit.get_id(),
                "other": other.get_id(),
                "gold": gold,
                "wood": wood
            }
        })

    def cut(self, unit, x, y):
        """
        Add a cut action to our actions and update ourself to represent the
        change
        """
        tree = self.get_tree_at(x, y)
        tree.subtract_wood(constants.CUT_AMOUNT)
        unit.add_wood(constants.CUT_AMOUNT)

        if tree.get_wood() <= 0:
            map.set_square(x, y, constants.EMPTY)
            self.trees.remove(tree)

        self.actions.append({
            "cut": {
                "unit": unit.get_id(),
                "x": x,
                "y": y
            }
        })

    def mine(self, unit, x, y):
        """
        Add a mine action to our actions and update ourself to represent the
        change
        """
        gold_mine = self.get_gold_mine_at(x, y)
        gold_mine.subtract_gold(constants.MINE_AMOUNT)
        unit.add_gold(constants.MINE_AMOUNT)

        if gold_mine.get_gold() <= 0:
            map.set_square(x, y, constants.BLOCK)
            self.gold_mines.remove(gold_mine)

        self.actions.append({
            "mine": {
                "unit": unit.get_id(),
                "x": x,
                "y": y
            }

    def _first_turn(self):
        """
        Prepare self for the first turn and then run the first turn
        """
        self.turn += 1
        input_data = json.loads(self.input())
        self.id = input_data["id"]
        self.num_players = input_data["all_num_players"]
        self.all_starting_locations = input_data["all_starting_locations"]
        self.starting_locations = input_data["starting_locations"]
        self.map = Map(input_data["map"])

        self.first_turn()

        self.output(self.name)

    def _turn(self):
        """
        Prepare self for a turn and then run the turn
        """
        self.turn += 1
        input_data = json.loads(self.input())
        self.units = [Unit(unit) for unit in input_data["units"]]
        self.map = Map(input_data["map"], gold_mines=input_data["gold_mines"],
            trees=input_data["trees"], units=self.units)
        self.actions = []

        self.turn()

        self.output(json.dumps(self.actions))

    def output(self, string):
        """
        Outputs data to stdout, which the warcode engine uses
        """
        print(string)

    def input(self):
        """
        Reads data from stdin, where the warcode engine gives us data
        """
        return input()
