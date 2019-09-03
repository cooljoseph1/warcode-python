#!/usr/bin/env python3
import os
import json

from warcode import constants

my_dir = os.path.realpath(os.path.dirname(__file__))


class Replay:
    def __init__(self, replay_name):
        with open(os.path.join(my_dir, os.pardir, "replays", replay_name)) as f:
            data = json.load(f)

        self.map = data["map"]
        self.teams = data["teams"]
        self.units = {unit[0]: Unit(unit) for unit in data["units"]}
        self.gold_mines = {gold_mine[0]: GoldMine(gold_mine) for gold_mine in data["gold_mines"]}
        self.trees = {tree[0]: Tree(tree) for tree in data["trees"]}
        self.turns = [[Action(action) for action in turn] for turn in data["turns"]]
        self.current_action = 0 # Current action overall
        self.current_turn_action = 0 # Current action in the turn
        self.current_turn = 0

    def get_gold_mine_at(self, x, y):
        """
        Returns the gold mine at a position
        """
        for gold_mine in self.gold_mines.values():
            if gold_mine.x == x and gold_mine.y == y:
                return gold_mine

    def get_tree_at(self, x, y):
        """
        Returns the tree at a position
        """
        for tree in self.trees.values():
            if tree.x == x and tree.y == y:
                return tree

    def take_action(self):
        """
        Take an action
        """
        self.current_action += 1
        self.current_turn_action += 1
        if self.current_turn_action >= len(self.turns[self.current_turn]):
            self.current_turn += 1
            self.current_turn_action = 0

        action = self.turns[self.current_turn][self.current_turn_action]
        if action.type == constanst.ATTACK:
            unit_type = self.units[action.unit].type
            for unit in list(self.units.values()) + list(self.trees.values()) + list(self.gold_mines.values()):
                if (unit.x - action.x)**2 + (unit.y - action.y)**2 <= unit_type.attack_splash:
                    unit.health -= unit_type.attack_damage

        elif action.type == constants.BUILD:
            self.units[action.other] = Unit([
                action.other,
                action.x,
                action.y,
                action.unit_type,
                self.units[action.unit].team,
                action.unit_type.initial_health,
                0,
                0
            ])

        elif action.type == constants.GIVE:
            self.units[action.unit] -= action.gold
            self.units[action.unit] -= action.wood
            self.units[action.other] += action.gold
            self.units[action.other] += action.wood

        elif action.type == constants.CUT:
            self.units[action.unit].wood += constants.CUT_AMOUNT
            tree = self.get_tree_at(action.x, action.y)
            tree.wood -= constants.CUT_AMOUNT
            if tree.wood <= 0:
                self.map[tree.y][tree.x] = constants.EMPTY

        elif action.type == constants.MINE:
            self.units[action.unit].gold += constants.MINE_AMOUNT
            gold_mine = self.get_gold_mine_at(action.x, action.y)
            gold_mine.gold -= constants.MINE_AMOUNT
            if gold_mine.gold <= 0:
                self.map[gold_mine.y][gold_mine.x] = constants.BLOCK

        elif action.type == constants.LOG:
            pass

    def undo_action(self):
        """
        Undo an action
        """
        self.current_action -= 1
        self.current_turn_action -= 1
        if self.current_turn_action < 0:
            self.current_turn -= 1
            self.current_turn_action = len(self.turns[self.current_turn]) - 1

        action = self.turns[self.current_turn][self.current_turn_action]
        if action.type == constanst.ATTACK:
            unit_type = self.units[action.unit].type
            for unit in list(self.units.values()) + list(self.trees.values()) + list(self.gold_mines.values()):
                if (unit.x - action.x)**2 + (unit.y - action.y)**2 <= unit_type.attack_splash:
                    unit.health += unit_type.attack_damage

        elif action.type == constants.BUILD:
            del self.units[action.other]

        elif action.type == constants.GIVE:
            self.units[action.unit] += action.gold
            self.units[action.unit] += action.wood
            self.units[action.other] -= action.gold
            self.units[action.other] -= action.wood

        elif action.type == constants.CUT:
            self.units[action.unit].wood -= constants.CUT_AMOUNT
            tree = self.get_tree_at(action.x, action.y)
            tree.wood += constants.CUT_AMOUNT
            if tree.wood > 0:
                self.map[tree.y][tree.x] = constants.TREE

        elif action.type == constants.MINE:
            self.units[action.unit].gold -= constants.MINE_AMOUNT
            gold_mine = self.get_gold_mine_at(action.x, action.y)
            gold_mine.gold -= constants.MINE_AMOUNT
            if gold_mine.gold > 0:
                self.map[gold_mine.y][gold_mine.x] = constants.GOLD_MINE

        elif action.type == constants.LOG:
            pass




class Unit:
    """
    Barebones unit to help run our viewer engine.
    """
    def __init__(self, data):
        # Unpack the data
        self.id, self.x, self.y, self.type, self.team, self.health, self.gold, self.wood = data
        self.type = getattr(constants, self.type)
        self.message = ""

    def harm(self, amount):
        self.health -= amount

    def move(self, x, y):
        self.x, self.y = x, y

    def mine(self, mine):
        self.gold += constants.MINE_AMOUNT
        mine.gold -= constants.MINE_AMOUNT

    def cut(self, tree):
        self.wood += constants.CUT_AMOUNT
        tree.wood -= constants.TREE_AMOUNT

    def give(self, other, gold, wood):
        self.gold -= gold
        self.wood -= wood
        other.gold += gold
        other.wood += wood


class GoldMine:
    """
    Barebones gold mine to help run our viewer engine
    """
    def __init__(self, data):
        self.id, self.x, self.y, self.gold = data


class Tree:
    """
    Barebones tree to help run our viewer engine
    """
    def __init__(self, data):
        self.id, self.x, self.y, self.wood = data


class Action:
    """
    Barebone action to help run our viewer engine.
    """
    def __init__(self, data):
        self.type = getattr(constants, data[0])
        if self.type == constants.ATTACK:
            self.unit = action[1]
            self.x = data[2]
            self.y = data[3]
        elif self.type == constants.BUILD:
            self.unit = data[1]
            self.unit_type = getattr(constants, data[2])
            self.other = data[3]
            self.x = data[4]
            self.y = data[5]
        elif self.type == constants.GIVE:
            self.unit = data[1]
            self.other = data[2]
            self.gold = data[3]
            self.wood = data[4]
        elif self.type == constants.CUT:
            self.unit = data[1]
            self.x = data[2]
            self.y = data[3]
        elif self.type == constants.MINE:
            self.unit = data[1]
            self.x = data[2]
            self.y = data[3]
        elif self.type == constants.LOG:
            self.message = data[1]
