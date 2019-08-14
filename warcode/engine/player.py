#!/usr/bin/env python3
import random
from subprocess import PIPE
from psutil import Popen
import os

my_dir = os.path.realpath(os.path.dirname(__file__))


def open_script(player_file):
    """
    Runs a player file.  Returns the process of the player file script.
    """

    return Popen(["python", player_file], stdin=PIPE, stdout=PIPE)


class Player:
    def __init__(self, player_name):
        player_file = os.path.join(my_dir, os.pardir, "players", player_name)
        self.process = open_script(player_file)
        self.process.suspend()
        self.time = 1

    def set_team(self, team):
        self.team = team

    def get_team(self):
        return self.team

    def get_time(self):
        return self.time

    def get_name(self):
        return self.name

    def first_turn(self, data):
        """
        Pass data to player and complete the first turn
        """
        self.process.resume()
        self.process.stdin.write((data + "\n").encode('utf-8'))
        self.process.stdin.flush()
        self.name = self.process.stdout.readline().strip()
        self.process.suspend()

    def turn(self, data):
        """
        Pass data to player and return its actions for a turn
        """
        # TODO:  Implement timing
        self.reset()
        self.process.resume()
        self.process.stdin.write((data + "\n").encode('utf-8'))
        self.process.stdin.flush()
        actions = self.process.stdout.readline().strip()
        self.process.suspend()
        return actions

    def is_alive(self):
        return len(self.team.get_units()) > 0

    def reset(self):
        """
        Prepare ourself for our turn
        """
        for unit in self.team.get_units().values():
            unit.reset()

    def clean_up(self, winner):
        """
        Clean up at the end of the game
        """
        print("{} won the game!".format(winner), file=self.process.stdin)
        self.process.kill()
        #self.process.stdin.close()
        #self.process.stdout.close()

    def to_dict(self):
        return {
            "name": self.name,
            "team": self.team.get_id()
        }
