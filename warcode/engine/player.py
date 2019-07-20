#!/usr/bin/env python3
import random
from subprocess import Popen, PIPE
import signal

from warcode.constants import CONSTANTS


def open_script(player_file):
    """
    Runs a player file.  Returns the process of the player file script.
    """

    return Popen([player_file], stdin=PIPE, stdout=PIPE)


class Player:
    def __init__(self, engine, player_file):
        self.engine = engine
        self.id = self.engine.create_id()
        self.gold = CONSTANTS["INITIAL_GOLD"]
        self.wood = CONSTANTS["INITIAL_WOOD"]
        self.game_map = self.engine.get_game_map()
        self.initial_positions = self.game_map.get_starting_location()
        self.process = open_script(player_file)
        self.process.send_signal(signal.SIGSTOP)
        self.name = self.process.stdout.readline().strip()
        self.units = []

    def turn(self):
        """
        Player's turn
        """
        # TODO:  Implement timing
        self.reset()
        self.process.send_signal(signal.SIGCONT)
        print(self.game_map.to_string(self.get_visible_locations()), file=self.process.stdin)
        actions = self.process.stdout.readline().strip()
        self.process.send_signal(signal.SIGSTOP)
        self.engine.process_actions(self, actions)

    def get_id(self):
        """
        Returns unit's unique id
        """
        return self.id

    def get_engine(self):
        """
        Returns the overall engine controlling the player
        """
        return self.engine

    def get_game_map(self):
        """
        Returns the overall game map
        """
        return self.game_map

    def get_visible_locations(self):
        """
        Returns all visible locations on the map
        """
        visible_locations = set(location for location in
                                game_map.get_all_locations() if self.is_visible(location))

    def is_visible(self, location):
        """
        Returns if a location is visible to the player
        """
        return any(unit.is_visible(location) for unit in units)

    def add_unit(self, unit):
        """
        Adds a new unit to ourself and the game
        """
        self.units.append(unit)
        self.game_map.add_unit(unit)

    def remove_unit(self, unit):
        """
        Completely removes a unit from the game
        """
        self.units.remove(unit)
        self.game_map.remove_unit(unit)

    def add_gold(self, amount):
        """
        Adds gold to the player's supply
        """
        self.gold += amount

    def add_wood(self, amount):
        """
        Adds wood to the player's supply
        """
        self.wood += amount

    def is_alive(self):
        return len(self.units) > 0

    def reset(self):
        """
        Prepare ourself for our turn
        """
        for unit in self.units:
            unit.reset()

    def clean_up(self, winner):
        """
        Clean up at the end of the game
        """
        print("GAME FINISHED, WINNER {}".format(winner), file=self.process.stdin)
        self.process.stdin.close()
        self.process.stdout.close()
