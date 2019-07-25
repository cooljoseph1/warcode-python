#!/usr/bin/bash
from warcode.constants import CONSTANTS

class Map:
    def __init__(self, map_data):
        self.width = len(map_data[0])
        self.height = len(map_data[1])
        self.board = [[Square(data) for data in row] for row in map_data]

class Square:
    def __init__(self, data):
        if data[0] == CONSTANTS["MAP_DATA"]["UNIT_OCCUPIED"]:
            
