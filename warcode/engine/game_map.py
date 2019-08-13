#!/usr/bin/env python3
import os
import json
from warcode import constants

my_dir = os.path.dirname(os.path.realpath(__file__))

class Map:
    def __init__(self, map_name):
        with open(os.path.join(my_dir, os.pardir, "maps", map_name)) as f:
            map_data = json.load(f)

        self.name = map_data["name"]
        self.starting_units = map_data["starting_units"]
        self.num_teams = map_data["players"]
        self.width = map_data["width"]
        self.height = map_data["height"]
        self.board = map_data["board"]

    def get_name(self):
        return self.name

    def get_starting_units(self):
        return self.starting_units

    def get_num_teams(self):
        return self.num_teams

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_board(self):
        return self.board

    def get_square_at(x, y):
        return self.board[y][x]

    def set_square_at(x, y, value):
        self.board[y][x] = value

    def get_gold_mine_locations(self):
        for y, row in enumerate(self.board):
            for x, value in enumerate(row):
                if value == constants.GOLD_MINE:
                    yield (x, y)

    def get_tree_locations(self):
        for y, row in enumerate(self.board):
            for x, value in enumerate(row):
                if value == constants.TREE:
                    yield (x, y)
