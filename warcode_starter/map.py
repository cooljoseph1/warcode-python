#!/usr/bin/bash
from warcode import constants

class Map:
    def __init__(self, map_data):
        """
        Creates a map from given map data, units, gold mines, and trees.  The
        units, gold mines, and trees should be dictionaries of id: value pairs.
        """
        self.width = len(map_data[0])
        self.height = len(map_data[1])
        self.board = map_data

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_square(self, x, y, value):
        self.board[y][x] = value
