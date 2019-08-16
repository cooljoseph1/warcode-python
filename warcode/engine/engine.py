#!/usr/bin/env python3
import json
import random
import traceback
import os

from warcode import constants
from warcode.exceptions import InvalidAction
from warcode.engine import Unit, Map, GoldMine, Player, Tree, Team

my_dir = os.path.realpath(os.path.dirname(__file__))

class Engine:
    """
    Overall engine class.  Runs a game.
    """

    def __init__(self, map_name, players, save_file, quiet=False):
        self.game_map = Map(map_name)
        self.quiet = quiet
        if not save_file.endswith(".wcr"):
            save_file += ".wcr"
        self.save_file = save_file

        self.ids_given = set()
        self.things = {}

        self.teams = {}
        for i in range(self.game_map.get_num_teams()):
            self.create_team()
        self.gold_mines = {}
        for x, y in self.game_map.get_gold_mine_locations():
            self.create_gold_mine(x, y)
        self.trees = {}
        for x, y in self.game_map.get_tree_locations():
            self.create_tree(x, y)

        # Randomly order the players
        players = random.sample(players, len(players))
        self.players = [Player(player) for player in players]
        # Assign each player a team
        for player, team in zip(self.players, self.teams.values()):
            player.set_team(team)

        self.units = {}
        for unit in self.game_map.get_starting_units():
            self.create_unit(unit["x"], unit["y"], getattr(constants, unit["type"]),
                self.players[unit["team"] - 1].get_team())


        self.finished = False
        self.turn = 0

        self.game_data = {
            "map": self.game_map.get_board(),
            "players": [{"team": player.team.get_id()} for player in self.players],
            "initial_units": [unit.to_dict() for unit in self.units.values()],
            "turns": [],
            "winner": None
        }

    def play(self):
        """
        Play the game, returning the winning player
        """
        self.turn += 1
        for player in self.players:
            data = self.get_first_turn_data(player)
            player.first_turn(data)

        while not self.finished:
            self.step()

    def step(self):
        """
        Goes through each player's turn
        """
        try:
            self.turn += 1
            self.game_data["turns"].append([])
            for player in self.players:
                data = self.get_data(player)
                actions = player.turn(data)
                self.process_actions(actions, player.get_team())

            for player in self.players[:]:
                if not player.is_alive():
                    self.remove_player(player)

            if len(self.players) <= 1 or self.turn >= 1000:
                self.end()
        except KeyboardInterrupt:
            print("Keyboard interrupt. Cleaning up nicely...")
            self.clean_up()

    def end(self):
        """
        End the game and clean up
        """
        if len(self.players) == 0:
            self.game_data["winner"] = "TIE"
        else:
            # TODO implement tie breaking
            self.game_data["winner"] = random.choice(self.players).get_name()

        self.clean_up()

    def get_winner(self):
        """
        Returns the name of the winning player
        """
        return self.game_data["winner"]

    def get_game_map(self):
        return self.game_map

    def generate_id(self):
        """
        Creates a random, unique 32 bit integer id
        """
        id = random.randint(0, 2**32 - 1)
        while id in self.ids_given:
            id = random.randint(0, 2**32 - 1)

        self.ids_given.add(id)
        return id

    def get_teams(self):
        return self.teams

    def create_team(self):
        id = self.generate_id()
        team = Team(id, self)
        self.teams[id] = team
        self.things[id] = team

    def remove_team(self, team):
        del self.teams[team.get_id()]
        del self.things[team.get_id()]

    def get_units(self):
        return self.units

    def create_unit(self, x, y, unit_type, team):
        id = self.generate_id()
        unit = Unit(id, x, y, unit_type, team, self)
        self.units[id] = unit
        self.things[id] = unit
        team.add_unit(unit)
        self.game_map.set_square_at(x, y, id)

    def remove_unit(self, unit):
        del self.units[unit.get_id()]
        del self.things[unit.get_id()]
        unit.get_team().remove_unit(unit)
        self.game_map.set_square_at(x, y, constants.EMPTY)

    def get_gold_mines(self):
        return self.gold_mines

    def create_gold_mine(self, x, y):
        id = self.generate_id()
        gold_mine = GoldMine(id, x, y, self)
        self.gold_mines[id] = gold_mine
        self.things[id] = gold_mine
        self.game_map.set_square_at(x, y, constants.GOLD_MINE)

    def remove_gold_mine(self, gold_mine):
        del self.gold_mines[gold_mine.get_id()]
        del self.things[gold_mine.get_id()]
        self.game_map.set_square_at(gold_mine.get_x(), gold_mine.get_y(),
            constants.BLOCK)

    def get_trees(self):
        return self.trees

    def create_tree(self, x, y):
        id = self.generate_id()
        tree = Tree(id, x, y, self)
        self.trees[id] = tree
        self.things[id] = tree
        self.game_map.set_square_at(x, y, constants.TREE)

    def remove_tree(self, tree):
        del self.trees[tree.get_id()]
        del self.things[tree.get_id()]
        self.game_map.set_square_at(tree.get_x(), tree.get_y(), constants.EMPTY)

    def remove_player(self, player):
        self.players.remove(player)

    def get_first_turn_data(self, player):
        """
        Get data for first turn
        """
        data = {}
        board = self.game_map.get_board()
        num_players = self.game_map.get_num_teams()
        starting_units = self.get_units().values()

        data["map"] = board
        data["num_players"] = num_players
        data["starting_units"] = [unit.to_dict() for unit in starting_units]
        data["teams"] = list(self.teams.keys())
        data["team_id"] = player.get_team().get_id()

        return json.dumps(data)


    def get_data(self, player):
        """
        Get data to pass to a player
        """
        team = player.get_team()

        data = {}
        board = self.game_map.get_visible_board(team)
        visible_units = [
            unit.to_dict() for unit in self.units.values()
            if board[unit.y][unit.x] != constants.INVISIBLE
        ]
        visible_gold_mines = [
            gold_mine.to_dict() for gold_mine in self.gold_mines.values()
            if board[gold_mine.y][gold_mine.x] != constants.INVISIBLE
        ]
        visible_trees = [
            tree.to_dict() for tree in self.trees.values()
            if board[tree.y][tree.x] != constants.INVISIBLE
        ]

        data["time"] = player.get_time()
        data["map"] = board
        data["units"] = visible_units
        data["gold_mines"] = visible_gold_mines
        data["trees"] = visible_trees
        data["gold"] = team.get_gold()
        data["wood"] = team.get_wood()

        return json.dumps(data)

    def process_actions(self, action_string, team):
        """
        Process actions from a json string
        """
        data = json.loads(action_string)
        for action in data:
            self.complete_action(action, team)

    def complete_action(self, action, team):
        """
        Processes a single action
        """
        try:
            # Check to make sure they aren't trying to control someone else's
            # units.
            if action["type"] in (constants.ATTACK, constants.BUILD, constants.GIVE, constants.CUT, constants.MINE):
                unit = self.units[action["unit"]]
                if unit.team != team:
                    raise InvalidAction("You can't control units that are not your own.")

            # Process the action
            if action["type"] == constants.ATTACK:
                unit = self.units[action["unit"]]
                unit.attack(action["x"], action["y"])
            elif action["type"] == constants.BUILD:
                unit = self.units[action["unit"]]
                unit.build(action["unit_type"], action["x"], action["y"])
            elif action["type"] == constants.GIVE:
                unit = self.units[action["unit"]]
                other = self.units[action["other"]]
                unit.give(other, action["gold"], action["wood"])
            elif action["type"] == constants.CUT:
                unit = self.units[action["unit"]]
                unit.cut(action["x"], action["y"])
            elif action["type"] == constants.MINE:
                unit = self.units[action["unit"]]
                unit.mine(action["x"], action["y"])
            elif action["type"] == constants.LOG:
                pass # Logs are dealt with later
            else:
                raise InvalidAction(action)
        except Exception:
            if not self.quiet:
                traceback.print_exc()
        # Save the action to our action log if it was valid, and print it out
        else:
            short = self.short_version(action)
            if action["type"] != constants.LOG:
                # Don't save logs, because who cares about those?
                self.save_action(short)
            if not self.quiet:
                print(*short)


    def short_version(self, action):
        """
        Create a shorter version of an action, useful for saving it in a file
        without taking up a lot of room
        """
        if action["type"] == constants.ATTACK:
            return (constants.ATTACK, action["unit"], action["x"], action["y"])
        elif action["type"] == constants.BUILD:
            return (constants.BUILD, action["unit"], action["unit_type"], action["x"], action["y"])
        elif action["type"] == constants.GIVE:
            return (constants.GIVE, action["unit"], action["other"], action["gold"], action["wood"])
        elif action["type"] == constants.CUT:
            return (constants.CUT, action["unit"], action["x"], action["y"])
        elif action["type"] == constants.MINE:
            return (constants.MINE, action["unit"], action["x"], action["y"])
        elif action["type"] == constants.LOG:
            return (constants.LOG, action["message"])
        return None

    def save_action(self, action):
        self.game_data["turns"][-1].append(action)

    def clean_up(self):
        self.finished = True
        for player in self.players:
            player.clean_up(self.game_data["winner"])

        self.save()

    def save(self):
        print("Saving...")
        with open(os.path.join(my_dir, os.pardir, "saves", self.save_file), 'w') as f:
            f.write(json.dumps(self.game_data))
        print("Done!")
