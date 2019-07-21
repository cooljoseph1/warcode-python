import os
import json
import tkinter
from tkinter import filedialog

from warcode.constants import CONSTANTS

__my_dir__ = os.path.dirname(os.path.realpath(__file__))


class Window(tkinter.Tk):
    """
    This class is a window that you can use to create a map
    """
    def __init__(self, canvas_size=(800, 800), map_size=(30, 30), name="Untitled", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_name(name)
        self.save_location = None
        self.title(self.name)
        self.resizable(False, False)

        self.add_widgets(map_size, canvas_size)
        self.bind("<Button 1>", self.mouse_click)
        self.bind("<B1 Motion>", self.mouse_move)

    def set_name(self, name):
        self.name = name
        self.title(self.name)
        self.update()

    def add_widgets(self, map_size, canvas_size):
        """
        Add widgets when initializing window
        """
        # Add menu
        self.initialize_menu()
        # Add canvas
        self.initialize_canvas(map_size, canvas_size)

    def initialize_menu(self):
        # Our menu bar
        menu = tkinter.Menu(self)

        # Set up file menu
        file_menu = tkinter.Menu(menu, tearoff=0)
        file_menu.add_command(label="Open", command=self.open)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="Save As", command=self.save_as)
        # Add file menu to menu
        menu.add_cascade(label="File", menu=file_menu)

        # Set up options
        options_menu = tkinter.Menu(menu, tearoff=0)
        options_menu.add_command(label="Fullscreen", command=self.fullscreen)
        options_menu.add_command(label="Map Size", command=self.change_map_size)
        # Add options menu to menu
        menu.add_cascade(label="Options", menu=options_menu)

        # Set up tool menu
        self.tools = ["Empty", "Block", "Gold Mine", "Tree", "Team 1", "Team 2",
            "Team 3", "Team 4", "Team 5", "Team 6"]
        self.tool = tkinter.StringVar(self, self.tools[0])
        tool_menu = tkinter.Menu(menu, tearoff=0)
        for tool in self.tools:
            tool_menu.add_radiobutton(label=tool, variable=self.tool)
        # Add tool menu to menu
        menu.add_cascade(label="Tool", menu=tool_menu)

        # Add menu bar to window
        self.config(menu=menu)


    def initialize_canvas(self, map_size, canvas_size):
        """
        Initialize the canvas
        """
        self.canvas = Canvas(map_size, master=self, width=canvas_size[0], height=canvas_size[1])

    def open(self):
        """
        Open a saved warcode map
        """
        initial_directory = os.path.abspath(os.path.join(__my_dir__, os.pardir, "maps"))
        mask = [("Warcode Maps", "*.wcm"), ("All Files", "*.*")]
        file = filedialog.askopenfile(initialdir=initial_directory,
            filetypes=mask, mode="r")
        if file is None:
            return
        self.save_location=file.name

        data = json.load(file)
        file.close()
        if 2*data["width"] > data["height"]:
            width, height = 800, data["height"]/data["width"]*800
        else:
            width, height = data["width"]/data["height"]*1600, 1600

        self.canvas.destroy()
        self.canvas = Canvas(
            (data["width"], data["height"]),
            self,
            game_map=data["board"],
            starting_locations=data["starting_locations"],
            width=width,
            height=height
        )

        self.canvas.pack()
        self.set_name(data["name"])

    def save(self):
        if self.save_location is None:
            self.save_as()
        else:
            file = open(self.save_location, "w")
            data = {
                "name": self.name,
                "width": self.canvas.get_map_width(),
                "height": self.canvas.get_map_height(),
                "starting_locations": self.canvas.get_starting_locations(),
                "board": self.canvas.get_map()
            }
            json.dump(data, file)
            file.close()


    def save_as(self):
        initial_directory = os.path.abspath(os.path.join(__my_dir__, os.pardir, "maps"))
        mask = [("Warcode Maps", "*.wcm"), ("All Files", "*.*")]
        file = filedialog.asksaveasfile(initialdir=initial_directory,
            initialfile=self.name, filetypes=mask, defaultextension=".wcm",
            mode="w")
        if file is None:
            return
        self.save_location = file.name
        self.set_name(os.path.splitext(os.path.basename(file.name))[0])

        data = {
            "name": self.name,
            "width": self.canvas.get_map_width(),
            "height": self.canvas.get_map_height(),
            "starting_locations": self.canvas.get_starting_locations(),
            "board": self.canvas.get_map()
        }
        json.dump(data, file)
        file.close()

    def fullscreen(self):
        pass

    def change_map_size(self):
        pass

    def more_tools(self):
        pass

    def mouse_click(self, event):
        """
        Process the user clicking somewhere
        """
        self.canvas.set_square_at_canvas_position(event.x, event.y, self.tool.get())

    def mouse_move(self, event):
        """
        Processes the user moving their mouse while holding it down
        """
        self.canvas.set_square_at_canvas_position(event.x, event.y, self.tool.get())


class Canvas(tkinter.Canvas):
    def __init__(self, map_size, *args, game_map=None, starting_locations=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.map_size = map_size
        if game_map == None:
            self.game_map = [
                [
                    CONSTANTS["MAP_DATA"]["EMPTY"] for x in range(self.map_size[0])
                ] for y in range(self.map_size[1])
            ]
        else:
            self.game_map = game_map

        if starting_locations is None:
            self.starting_locations = [set() for i in range(6)] #6 players
        else:
            self.starting_locations = [set(locations) for locations in
                starting_locations]

        self.pack()
        self.update()

        self.tool_colors = {"Empty": "white", "Block": "gray50", "Gold Mine": "gold",
            "Tree": "forest green", "Team 1": "red", "Team 2": "royal blue",
            "Team 3": "orange", "Team 4": "deep sky blue", "Team 5": "yellow",
            "Team 6": "spring green"}

        self.squares = [
            [
                self.create_rectangle(
                    self.scaled_x(x),
                    self.scaled_y(y),
                    self.scaled_x(x+1),
                    self.scaled_y(y+1),
                    outline="",
                    fill=self.get_color(self.game_map[y][x])
                ) for x in range(self.map_size[0])
            ] for y in range(self.map_size[1])
        ]

        for i, locations in enumerate(self.starting_locations):
            for location in locations:
                self.itemconfig(
                    self.squares[location[1]][location[0]],
                    fill=self.tool_colors["Team "+str(i+1)]
                )

        self.x_lines = [
            self.create_line(
                self.scaled_x(x),
                0,
                self.scaled_x(x),
                self.winfo_height()
            ) for x in range(self.map_size[0] + 1)
        ]

        self.y_lines = [
            self.create_line(
                0,
                self.scaled_y(y),
                self.winfo_width(),
                self.scaled_y(y)
            ) for y in range(self.map_size[1] + 1)
        ]

    def get_map(self):
        """
        Returns the board
        """
        return self.game_map

    def get_map_width(self):
        """
        Returns the game map's width
        """
        return self.map_size[0]

    def get_map_height(self):
        return self.map_size[1]

    def get_starting_locations(self):
        """
        Returns a list of the nonempty starting locations
        """
        return [list(locations) for locations in self.starting_locations if
            len(locations) > 0]

    def add_starting_location(self, x, y, team):
        """
        Adds a location to a team's starting locations
        """
        self.starting_locations[team].add((x, y))

    def get_color(self, num):
        type = CONSTANTS["MAP_DATA"][str(num)]
        if type == "EMPTY":
            return self.tool_colors["Empty"]
        if type == "BLOCK":
            return self.tool_colors["Block"]
        if type == "TREE":
            return self.tool_colors["Tree"]
        if type == "GOLD_MINE":
            return self.tool_colors["Gold Mine"]

    def set_square(self, x, y, tool):
        """
        Sets the square at (x, y) to the type, updating the screen as well
        """

        if tool in ("Empty", "Team 1", "Team 2", "Team 3", "Team 4", "Team 5", "Team 6"):
            type = "EMPTY"
        elif tool == "Gold Mine":
            type = "GOLD_MINE"
        elif tool == "Tree":
            type = "TREE"
        elif tool == "Block":
            type = "BLOCK"
        self.game_map[y][x] = CONSTANTS["MAP_DATA"][type]
        self.itemconfig(self.squares[y][x], fill=self.tool_colors[tool])

        for positions in self.starting_locations:
            if (x, y) in positions:
                positions.remove((x, y))

        if tool in ("Team 1", "Team 2", "Team 3", "Team 4", "Team 5", "Team 6"):
            self.add_starting_location(x, y, int(tool[-1]))

    def set_square_at_canvas_position(self, canvas_x, canvas_y, tool):
        x, y = self.scale_back((canvas_x, canvas_y))
        if 0 <= x < self.map_size[0] and 0 <= y < self.map_size[1]:
            self.set_square(x, y, tool)

    def scaled_x(self, x):
        """
        Return a scaled x value, where an input of 0 is the left side of the
        screen and an input of 1 is the right side of the screen.
        """
        return 2 + (self.winfo_width() - 5) * x / self.map_size[0]

    def scaled_y(self, y):
        """
        Return a scaled y value, where an input of 0 is the top side of the
        screen and an input of 1 is the bottom side of the screen.
        """
        return 2 + (self.winfo_height() - 5) * y / self.map_size[1]

    def scale_back(self, location):
        """
        Scales a location to an integer x and y where the square is
        """
        new_x = int((location[0] - 2) * self.map_size[0] / (self.winfo_width() - 5))
        new_y = int((location[1] - 2) * self.map_size[1] / (self.winfo_height() - 5))
        return (new_x, new_y)

def main():
    window = Window()
    window.tk.mainloop()


if __name__ == "__main__":
    main()
