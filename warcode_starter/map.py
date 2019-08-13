#!/usr/bin/bash
from warcode import constants

class Map:
    def __init__(self, map_data, units=None, gold_mines=None, trees=None):
        """
        Creates a map from given map data, units, gold mines, and trees.  The
        units, gold mines, and trees should be dictionaries of id: value pairs.
        """
        self.width = len(map_data[0])
        self.height = len(map_data[1])
        self.board = map_data

        units = units or {}
        gold_mines = gold_mines or {}
        trees = trees or {}
        for unit in units.items():
            self.set_square(unit.get_x(), unit.get_y(), constants.UNIT_OCCUPIED)
        for gold_mine in gold_mines.items():
            self.set_square(gold_mine.get_x(), gold_mine.get_y(), constants.GOLD_MINE)
        for tree in trees.items():
            self.set_square(tree.get_x(), tree.get_y(), constants.TREE)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_square(self, x, y, value):
        self.board[y][x] = value
