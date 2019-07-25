#!/usr/bin/env python3
from warcode import constants

class Unit:
    def __init__(self, data):
        self.unit_type = constants.unit_from_int(data[0])
