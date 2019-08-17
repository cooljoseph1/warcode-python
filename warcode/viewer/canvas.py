#!/usr.bin/env python3
import tkinter

from warcode import constants

class Canvas(tkinter.Canvas):
    """
    This is the canvas used to draw the game
    """
    def __init__(width, height, map_width, map_height):
        super().__init__(width=width, height=height)
        self.map_width = map_width
        self.map_height = map_height

        self.pack()

        self.width_ratio = self.winfo_width() / self.map_width
        self.height_ratio = self.winfo_height() / self.map_height

        self.squares = [
            [
                self.create_rectangle(
                    x * self.width_ratio,
                    y * self.height_ratio,
                    (x + 1) * self.width_ratio,
                    (y + 1) * self.height_ratio,
                    fill="white",
                    outline="black",
                    tags="square"
                ) for x in range(self.map_width)
            ] for y in range(self.map_height)
        ]

    def draw(self, data):
        """
        Draw the game state given a dictionary of data.
        The units and actions are dictionaries as well
        """
        board = data["board"]
        units = data["units"]
        actions = data["actions"]

        # Update the baord
        self.update_board(board)

        # Destroy all previous unit images and health bars
        self.delete("unit")

        # Add unit drawings
        for unit in units:
            self.draw_unit(unit)

        # Destroy all previous action drawings
        self.delete("action")

        # Add action drawings
        for action in actions:
            self.draw_action(action)

    def update_board(self, board):
        """
        Update our board colors
        """
        for y, row in enumerate(board):
            for x, value in enumerate(row):
                current_color = self.itemcget(square, "fill")
                desired_color = self.get_color(value)
                # Only change the fill color if it is different from the
                # color we want
                if current_color != desired_color:
                    self.itemconfig(square, fill=desired_color)

    def get_color(self, square):
        """
        Return the color a square should be given its type
        """
        color_dict = {
            constants.EMPTY: "white",
            constants.BLOCK: "black",
            constants.GOLD_MINE: "gold",
            constants.TREE: "forest green",
            constants.INVISIBLE: "gray"
        }

        return color_dict[square]

    def set_square_color(self, x, y, color):
        """
        Change the square at (x, y) to the color if it is not yet that color.
        """
        square = self.squares[y][x]
        current_color = self.itemcget(square, "fill")
        desired_color = self.get_color(value)
        if current_color != desired_color:
            self.itemconfig(square, fill=desired_color)

    def draw_unit(self, unit):
        """
        Draw a unit given its x, y, type, health, and team
        """
        x, y, type, health, team = unit["x"], unit["y"], unit["type"], unit["health"], unit["team"]

        # Set background color to the team's color
        color = self.get_team_color(team)
        self.set_square_color(x, y, color)

        # Create the image
        image = self.get_image(type)
        self.create_image(
            x * self.width_ratio,
            y * self.height_ratio,
            image=image,
            tags=("unit", "image")
        )

        # Create the health bar
        self.create_rectangle(
            (x + 0.1) * self.width_ratio,
            (y + 0.8) * self.height_ratio,
            (x + 0.9) * self.width_ratio,
            (y + 0.9) * self.height_ratio,
            fill="gray",
            outline="black",
            tags=("unit", "health bar")
        )
        self.create_rectangle(
            (x + 0.1) * self.width_ratio,
            (y + 0.8) * self.height_ratio,
            (x + 0.1 + 0.8 *  health / type.initial_health) * self.width_ratio,
            (y + 0.9) * self.height_ratio,
            fill="yellow",
            tags=("unit", "health bar")
        )

    def get_image(self, type):
        """
        Returns the image a unit type corresponds with
        """
        image_dict = {
            constants.ARCHER: self.archer_image,
            constants.CASTLE: self.castle_image,
            constants.FORTRESS: self.fortress_image,
            constants.KNIGHT: self.knight_image,
            constants.LANDMINE: self.landmine_image,
            constants.MAGE: self.mage_image,
            constants.PEASANT: self.peasant_image,
            constants.TOTEM: self.totem_image,
            constants.TOWER: self.tower_image
        }
        return image_dict[type]

    def get_team_color(self):
        """
        Returns the color associated with a team
        """
        color_dict = {
            1: "red",
            2: "blue",
            3: "yellow",
            4: "cyan",
            5: "green",
            6: "pink"
        }
        return color_dict[team]

    def draw_action(self, action):
        """
        Draw an action.  Currently only attack actions are implemented.
        """
        if action["type"] == constants.ATTACK:
            self.draw_attack_action(action)

    def draw_attack_action(self, action):
        """
        Draw an attack action
        """
        start_x = action["unit_x"]
        start_y = action["unit_y"]
        end_x = action["x"]
        end_y = action["y"]
        team = action["unit_team"]
        color = self.get_team_color(team)

        self.create_line(
            (start_x + 0.5) * self.width_ratio,
            (start_y + 0.5) * self.height_ratio,
            (end_x + 0.5) * self.width_ratio,
            (end_y + 0.5) * self.height_ratio,
            fill=color,
            tags=("action", "attack")
        )
