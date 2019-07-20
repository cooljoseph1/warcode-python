#!/usr/bin/env python3
import json
import os
__my_directory__ = os.path.realpath(os.path.dirname(__file__))

with open(os.path.join(__my_directory__, "constants.json")) as f:
    CONSTANTS = json.load(f)
