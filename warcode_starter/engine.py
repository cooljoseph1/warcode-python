#!/usr/bin/env python3
import json
import fileinput

from map import Map

class Engine:
    def __init__(self):
        pass

    def print_actions(self, actions):
        print(json.dumps(actions))

    def load_map(self):
        new_map = json.loads(fileinput.input())
        return Map(new_map)
