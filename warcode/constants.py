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

MINE_AMOUNT = _data["MINE_AMOUNT"]
CUT_AMOUNT = _data["CUT_AMOUNT"]
GOLD_MINE_HEALTH = _data["GOLD_MINE_HEALTH"]
TREE_HEALTH = _data["TREE_HEALTH"]
INITIAL_GOLD = _data["INITIAL_GOLD"]
INITIAL_WOOD = _data["INITIAL_WOOD"]

class _Unit:
    def __init__(self, name, initial_health, movement_speed, min_attack_distance,
            max_attack_distance, attack_damage, attack_splash, visiblity_distance,
            gold_cost, wood_cost):
        self.name = name
        self.initial_health = initial_health
        self.movement_speed = movement_speed
        self.min_attack_distance = min_attack_distance
        self.max_attack_distance = max_attack_distance
        self.attack_damage = attack_damage
        self.attack_splash = attack_splash
        self.visiblity_distance = visiblity_distance
        self.gold_cost = gold_cost
        self.wood_cost = wood_cost

    def get_name(self):
        return self.name

    def get_initial_health(self):
        return self.initial_health

    def get_movement_speed(self):
        return self.movement_speed

    def get_min_attack_distance(self):
        return self.min_attack_distance

    def get_max_attack_distance(self):
        return self.max_attack_distance

    def get_attack_damage(self):
        return self.attack_damage

    def get_attack_splash(self):
        return self.attack_splash

    def get_visibility_distance(self):
        return self.visibility_distance

    def get_gold_cost(self):
        return self.gold_cost

    def get_wood_cost(self):
        return self.wood_cost

    def __str__(self):
        return self.name


ARCHER = _Unit("ARCHER", **_data["ARCHER"])
CASTLE = _Unit("CASTLE", **_data["CASTLE"])
FORTRESS = _Unit("FORTRESS", **_data["FORTRESS"])
KNIGHT = _Unit("KNIGHT", **_data["KNIGHT"])
LANDMINE = _Unit("LANDMINE"**_data["MINE"])
MAGE = _Unit("MAGE", **_data["MAGE"])
PEASANT = _Unit("PEASANT", **_data["PEASANT"])
TOTEM = _Unit("TOTEM", **_data["TOTEM"])
TOWER = _Unit("TOWER", **_data["TOWER"])

ALLOWED_CREATIONS = {}
for unit, allowed_units in _data["ALLOWED_CREATIONS"].items():
    ALLOWED_CREATIONS[locals()[unit]] = set(locals()[other] for other in allowed_units)
