#!/usr/bin/env python3
import json
import os

_my_dir_ = os.path.realpath(os.path.dirname(__file__))

with open(os.path.join(_my_dir_, "constants.json")) as f:
    _data = json.load(f)

EMPTY = _data["EMPTY"]
BLOCK = _data["BLOCK"]
TREE = _data["TREE"]
GOLD_MINE = _data["GOLD_MINE"]
UNIT_OCCUPIED = _data["UNIT_OCCUPIED"]
INVISIBLE = _data["INVISIBLE"]

class _Unit:
    def __init__(self, initial_health, movement_speed, min_attack_distance,
            max_attack_distance, attack_damage, attack_splash, visiblity_distance,
            gold_cost, wood_cost):

        self.initial_health = initial_health
        self.movement_speed = movement_speed
        self.min_attack_distance = min_attack_distance
        self.max_attack_distance = max_attack_distance
        self.attack_damage = attack_damage
        self.attack_splash = attack_splash
        self.visiblity_distance = visiblity_distance
        self.gold_cost = gold_cost
        self.wood_cost = wood_cost


PEASANT = _Unit(**_data["PEASANT"])
ARCHER = _Unit(**_data["ARCHER"])
MAGE = _Unit(**_data["MAGE"])
KNIGHT = _Unit(**_data["KNIGHT"])
CASTLE = _Unit(**_data["CASTLE"])
FORTRESS = _Unit(**_data["FORTRESS"])
TOWER = _Unit(**_data["TOWER"])
LANDMINE = _Unit(**_data["MINE"])
TOTEM = _Unit(**_data["TOTEM"])
