#!/usr/bin/env python3
from warcode import constants
from warcode.exceptions import (
    IllegalAttackException,
    IllegalBuildException,
    IllegalCutException,
    IllegalGiveException,
    IllegalMineException,
    IllegalMoveException
)

class Unit:
    """
    A unit.
    """
    def __int__(self, id, x, y, unit_type, team, engine):
        self.id = id
        self.x = x
        self.y = y
        self.unit_type = unit_type
        self.team = team

        self.health = self.unit_type.get_initial_health()
        self.gold = 0
        self.wood = 0

        self.action_taken = True # Units can't take an action their first turn

        self.engine = engine
        self.game_map = self.engine.get_game_map()

    def get_id(self):
        """
        Returns our id
        """
        return self.id

    def get_x(self):
        """
        Returns our x position
        """
        return self.x

    def get_y(self):
        """
        Returns our y position
        """
        return self.y

    def get_location(self):
        """
        Returns a tuple (x, y) of our position.
        """
        return (x, y)

    def get_unit_type(self):
        """
        Returns our unit type
        """
        return self.unit_type

    def get_team(self):
        """
        Returns our team
        """
        return self.team

    def get_health(self):
        """
        Returns the health we have
        """
        return self.health

    def get_gold(self):
        """
        Returns the gold we have
        """
        return self.gold

    def add_gold(self, amount):
        """
        Adds gold to the amount of gold we are carrying
        """
        self.gold += amount

    def subtract_gold(self, amount):
        """
        Subtracts gold from the amount we are carrying
        """
        self.gold -= amount

    def get_wood(self):
        """
        Returns the wood we have
        """
        return self.wood

    def add_wood(self, amount):
        """
        Adds wood to the amount of wood we are carrying
        """
        self.wood += amount

    def subtract_wood(self, amount):
        """
        Subtracts wood from the amount we are carrying
        """
        self.wood -= amount

    def get_action_taken(self):
        """
        Returns whether we have taken an action this turn
        """
        return self.action_taken

    def set_action_taken(self, boolean):
        self.action_taken = boolean

    def reset(self):
        """
        Things we do to prepare ourself for the next turn
        """
        self.set_action_taken(False)

    def damage(self, amount):
        """
        Damage a unit by an amount, removing it if it dies
        """
        self.health -= amount
        if self.health <= 0:
            self.engine.remove_unit(self)

    def attack(self, x, y):
        """
        Attacks a location, throwing an exception if it is an illegal attack
        """

        # Throw  an error if we have already taken an action
        if self.get_action_taken():
            raise IllegalAttackException("You can't take two actions in one turn.")

        # Throw error if we are trying to attack outside our range
        distance = self.distance_to(x, y)
        if (distance < self.unit_type.get_min_attack_distance() or
                distance > self.unit_type.get_max_attack_distance()):
            raise IllegalAttackException("You can't attack that far.")

        for thing in self.engine.get_all_things():
            if thing.distance_to(location) <= self.unit_type.get_attack_splash():
                thing.damage(self.unit_type.get_attack_damage)

        self.set_action_taken(True)

    def move(self, x, y):
        """
        Move the unit to a new location
        """
        if self.get_action_taken():
            raise IllegalMoveException("You can't take two actions in one turn.")

        if self.distance_to(x, y) > self.unit_type.get_movement_speed():
            raise IllegalMoveException("You can't move that fast.")
        if self.game_map.get_square_at(x, y) != constants.EMPTY:
            raise IllegalMoveException("You can only move onto an empty square.")

        self.game_map.set_square_at(self.get_x(), self.get_y(), constants.EMPTY)
        self.game_map.set_square_at(x, y, self.get_id())
        self.x = x
        self.y = y

        self.set_action_taken(True)

    def build(self, unit_type, x, y):
        """
        Creates a new unit of type unit_type at location, throwing an error if
        it is an illegal move
        """
        if self.get_action_taken():
            raise IllegalBuildException("You can only take one action per turn.")
        if self.team.get_gold() < self.unit_type.get_gold_cost():
            raise IllegalBuildException("A {} costs too much gold for you to make.".format(unit_type))
        if self.team.get_wood() < self.unit_type.get_wood_cost():
            raise IllegalBuildException("A {} costs too much wood for you to make.".format(unit_type))
        if self.distance_to(x, y) > 2:
            raise IllegalBuildException("You can only build next to yourself")
        if unit_type not in constants.ALLOWED_CREATIONS[self.unit_type]:
            raise IllegalBuildException("You can't make a {}.".format(unit_type))
        if self.game_map.get_square_at(x, y) != constants.EMPTY:
            raise IllegalBuildException("You can only build on an empty square.")

        self.team.subtract_gold(unit_type.get_gold_cost())
        self.team.subtract_wood(unit_type.get_wood_cost())
        self.engine.create_unit(x, y, unit_type, self.team)

        self.set_action_taken(True)

    def mine(self, x, y):
        """
        Mines gold from a location (if that location is a gold mine)
        """
        if self.get_action_taken():
            raise IllegalMineException("You can only take one action per turn.")
        if self.distance_to(x, y) > 2:
            raise IllegalMineException("You can only mine next to yourself.")
        if self.unit_type != constants.PEASANT:
            raise IllegalMineException("Only peasants can mine gold.")
        if self.game_map.get_square_at(x, y) != constants.GOLD_MINE:
            raise Exception("You can only mine gold from gold mines.")

        self.add_gold(constants.MINE_AMOUNT)
        gold_mine = self.engine.get_gold_mine_at(x, y)
        gold_mine.subtract_gold(constants.MINE_AMOUNT)

        self.set_action_taken(True)

    def cut(self, x, y):
        """
        Cuts wood from a location (if that location is a tree)
        """
        if self.get_action_taken():
            raise IllegalCutException("You can only take one action per turn.")
        if self.distance_to(x, y) > 2:
            raise IllegalCutException("You can only cut wood next to yourself.")
        if self.unit_type != constants.PEASANT:
            raise IllegalCutException("Only peasants can cut wood.")
        if self.game_map.get_square_at(x, y) != constants.TREE:
            raise IllegalCutException("You can only cut wood from trees.")

        self.add_wood(constants.CUT_AMOUNT)
        tree = self.engine.get_tree_at(x, y)
        tree.subtract_wood(constants.CUT_AMOUNT)

        self.set_action_taken(True)

    def give(self, x, y, gold, wood):
        """
        Give wood from yourself to another unit.  If that unit is a castle or
        fortress, add the amount to your team's gold/wood supply
        """
        if self.get_action_taken():
            raise IllegalGiveException("You can only take one action per turn.")
        if self.distance_to(x, y) > 2:
            raise Exception("You can only give materials to a neighbor.")
        if self.get_gold() < gold:
            raise Exception("You can't give away gold you don't own. That's called stealing!")
        if self.get_wood() < wood:
            raise Exception("You don't have enough wood to share.")

        unit = self.engine.get_unit_at(x, y)
        self.subtract_gold(gold)
        self.subtract_wood(wood)

        if unit.get_unit_type() in (constants.CASTLE, constants.FORTRESS):
            self.team.add_gold(gold)
            self.team.add_wood(wood)
        else:
            unit.add_gold(gold)
            unit.add_wood(wood)

        self.set_action_taken(True)

    def distance_to(self, x, y):
        """
        Returns the distance squared from this unit to a location
        """
        return (self.x - x)**2 + (self.y - y)**2
