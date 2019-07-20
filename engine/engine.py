#!/usr/bin/env python3
import json
import random

from constants import CONSTANTS
from game_map import Map
from logger import Logger


class Engine:
    """
    Overall engine class.  Runs a game.
    """

    def __init__(self, map_name, players, verbose=True, very_verbose=False):
        self.game_map = Map(map_name)
        self.ids_given = set()
        self.players = players[:]
        self.player_id_dict = dict((player.get_id(), player) for player in self.players)
        self.verbose = verbose
        self.very_verbose = very_verbose and verbose
        self.logger = Logger()
        self.finished = False
        self.turn = 0
        self.winner = None

    def create_id(self):
        """
        Creates a random, unique 32 bit integer id
        """
        id = random.randint(0, 2**32 - 1)
        while id in self.ids_given:
            id = random.randint(0, 2**32 - 1)

        self.ids_given.add(id)
        return id

    def play(self):
        """
        Play the game, returning the winning player
        """
        while not self.finished:
            self.step()

    def step(self):
        """
        Goes through each player's turn
        """
        for player in self.players:
            player.turn()

        for player in self.players[:]:
            if not player.is_alive():
                self.remove_player(player)

        if len(self.players) <= 1:
            self.end()

        self.turn += 1

    def end(self):
        """
        End the game and clean up
        """
        self.finished = True
        if len(self.players) == 0:
            self.winner = "TIE"
        else:
            # TODO implement tie breaking
            self.winner = random.choice(self.players).get_name()

        for player in self.players:
            player.clean_up(self.winner)

    def get_winner(self):
        """
        Returns the name of the winning player
        """
        return self.winner

    def get_player_from_id(self, id):
        """
        Returns a player from its id
        """
        return self.player_id_dict[id]

    def remove_player(self, player):
        """
        Removes a player from the game
        """
        self.players.remove(player)
        del self.player_id_dict[player.get_id()]

    def get_game_map(self):
        return self.game_map

    def process_actions(self, action_string):
        """
        Process actions from a json string
        """
        if self.very_verbose:
            logger.log(action_string)
        actions = json.loads(action_string)
        for action in actions:
            self.complete_action(action)

    def complete_action(self, action):
        """
        Processes a single action
        """
        try:
            action_type = action["type"]
            if action_type == "ATTACK":
                self.attack(self.get_unit_from_id(action["unit_id"]), action["location"])
            elif action_type == "CREATE":
                self.create(self.game_map.get_unit_from_id(action["creator_id"]),
                            action["unit_type"], action["location"])
            elif action_type == "MOVE":
                self.move(self.get_unit_from_id(action["unit_id"]), action["location"])
            elif action_type == "MINE":
                self.mine(self.get_unit_from_id(action["unit_id"]), action["location"])
            elif action_type == "CUT":
                self.cut(self.get_unit_from_id(action["unit_id"]), action["location"])
            elif action_type == "GIVE":
                self.give(self.get_unit_from_id(action["unit_id"]),
                          action["location"], action["gold"], action["wood"])
            else:
                raise Exception("Unknown action {}".format(action_type))

        except Exception as e:
            if self.verbose:
                logger.log_error(e)

    def attack(self, unit, location):
        """
        Processes an ATTACK action
        """
        unit.attack(location)

    def create(self, creator, unit_type, location):
        """
        Processes a CREATE action
        """
        creator.create(unit_type, location)

    def move(self, unit, location):
        """
        Processes a MOVE action
        """
        unit.move(location)

    def mine(self, unit, location):
        """
        Processes a MINE action
        """
        unit.mine(location)

    def cut(self, unit, location):
        """
        Processes a CUT action
        """
        unit.cut(location)

    def give(self, unit, location, gold, wood):
        """
        Processes a GIVE action
        """
        unit.give(location, gold, wood)
