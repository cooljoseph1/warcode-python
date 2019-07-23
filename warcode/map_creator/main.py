import os
import math
import json
import tkinter
from tkinter import filedialog, ttk, messagebox

from warcode.constants import CONSTANTS

__my_dir__ = os.path.dirname(os.path.realpath(__file__))


class Window(tkinter.Tk):
    """
    This class is the main window that you can use to create a map
    """
    def __init__(self, canvas_size=(800, 800), map_size=(30, 30), name="Untitled", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_name(name)
        self.save_location = None
        self.resizable(False, False)
        self.set_unsaved_changes(False)
        self.title("*" + self.name + "*")

        self.add_widgets(map_size, canvas_size)
        self.bind("<Button 1>", self.mouse_click)
        self.bind("<B1 Motion>", self.mouse_click)
        self.protocol("WM_DELETE_WINDOW", self.quit)

    def set_name(self, name):
        """
        Set the name of our map
        """
        self.name = name
        self.title(self.name)

    def set_unsaved_changes(self, value):
        self.unsaved_changes = value
        if value:
            self.title("*" + self.name + "*")
        else:
            self.title(self.name)


    def add_widgets(self, map_size, canvas_size):
        """
        Add widgets when initializing window
        """
        # Add menu
        self.initialize_menu()
        # Add canvas
        self.initialize_canvas(map_size, canvas_size)

    def initialize_menu(self):
        """
        Create our menu bar
        """
        # Our menu bar
        menu = tkinter.Menu(self)

        # Set up file menu
        self.file_menu = tkinter.Menu(menu, tearoff=0)
        self.file_menu.add_command(label="New", underline=0, command=self.new, accelerator="Ctrl+N")
        self.bind_all("<Control-n>", self.new)
        self.file_menu.add_command(label="Open", underline=0, command=self.open, accelerator="Ctrl+O")
        self.bind_all("<Control-o>", self.open)
        self.file_menu.add_command(label="Save", underline=0, command=self.save, accelerator="Ctrl+S")
        self.bind_all("<Control-s>", self.save)
        self.file_menu.add_command(label="Save As", underline=5, command=self.save_as, accelerator="Ctrl+Shift+S")
        self.bind_all("<Control-Shift-s>", self.save_as)
        self.file_menu.add_command(label="Exit", underline=1, command=self.quit, accelerator="Ctrl+Q")
        self.bind_all("<Control-q>", self.quit)
        # Add file menu to menu
        menu.add_cascade(label="File", menu=self.file_menu, underline=0)

        # Set up symmetry menu
        symmetries = ["None", "Horizontal", "Vertical", "UR Diagonal", "DR Diagonal", "Radial"]
        self.symmetry = tkinter.StringVar(self, symmetries[1])
        self.symmetry_menu = tkinter.Menu(menu, tearoff=0)
        for symmetry in symmetries:
            self.symmetry_menu.add_radiobutton(label=symmetry, underline=0, variable=self.symmetry)

        # Add symmetry menu to menu
        menu.add_cascade(label="Symmetry", menu=self.symmetry_menu, underline=0)

        # Set up players menu
        player_options = [str(i) + " Players" for i in range(2, 7)]
        self.num_players_string = tkinter.StringVar(self, player_options[0])
        self.num_players = 2
        self.player_menu = tkinter.Menu(menu, tearoff=0)
        for player_option in player_options:
            self.player_menu.add_radiobutton(label=player_option, underline=0,
                variable=self.num_players_string, command=self.update_num_players)

        # Add player menu to menu
        menu.add_cascade(label="Players", menu=self.player_menu, underline=0)

        # Set up tool menu
        tools = ["Empty", "Block", "Gold Mine", "Tree"]
        self.tool = tkinter.StringVar(self, tools[1])
        self.tool_menu = tkinter.Menu(menu, tearoff=0)
        for tool in tools:
            self.tool_menu.add_radiobutton(label=tool, underline=0, variable=self.tool)
        for i in range(1, self.num_players + 1):
            self.tool_menu.add_radiobutton(label="Team "+str(i), underline=5, variable=self.tool)
        # Add tool menu to menu
        menu.add_cascade(label="Tool", menu=self.tool_menu, underline=0)

        # Add menu bar to window
        self.config(menu=menu)

    def update_num_players(self):
        self.num_players = int(self.num_players_string.get()[0])
        self.tool_menu.delete(4, "end")
        for i in range(1, self.num_players + 1):
            self.tool_menu.add_radiobutton(label="Team "+str(i), underline=5, variable=self.tool)
        if self.tool.get()[-1].isdigit() and int(self.tool.get()[-1]) > self.num_players:
            self.tool.set("Block")
        self.symmetry_menu.delete(0, "end")
        if self.num_players == 2:
            symmetries = ["None", "Horizontal", "Vertical", "UR Diagonal", "DR Diagonal", "Radial"]
        elif self.num_players == 4:
            symmetries = ["None", "Horizontal/Vertical", "Radial"]
        elif self.num_players in (3, 5, 6):
            symmetries = ["None", "Radial"]

        if self.symmetry.get() not in symmetries:
            self.symmetry.set(symmetries[1])

        for symmetry in symmetries:
            self.symmetry_menu.add_radiobutton(label=symmetry, underline=0, variable=self.symmetry)

    def initialize_canvas(self, map_size, canvas_size):
        """
        Initialize the canvas
        """
        self.canvas = Canvas(map_size, master=self, width=canvas_size[0], height=canvas_size[1])

    def new(self, event=None):
        """
        Create a new map
        """
        if not self.check_unsaved("New"):
            return

        popup = tkinter.Toplevel(self)
        popup.title("New Map")
        popup.resizable(False, False)

        input_frame = tkinter.Frame(popup)

        LARGE_FONT= ("Verdana", 12)

        name_label = ttk.Label(input_frame, text="Name: ", font=LARGE_FONT)
        width_label = ttk.Label(input_frame, text="Width: ", font=LARGE_FONT)
        height_label = ttk.Label(input_frame, text="Height: ", font=LARGE_FONT)
        name_entry = ttk.Entry(input_frame, font=LARGE_FONT)
        width_entry = ttk.Entry(input_frame, font=LARGE_FONT)
        height_entry = ttk.Entry(input_frame, font=LARGE_FONT)

        name_label.grid(row=0, column=0, padx=5, pady=5)
        width_label.grid(row=1, column=0, padx=5, pady=5)
        height_label.grid(row=2, column=0, padx=5, pady=5)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        width_entry.grid(row=1, column=1, padx=5, pady=5)
        height_entry.grid(row=2, column=1, padx=5, pady=5)

        def create_new(event=None):
            try:
                width = int(width_entry.get())
            except:
                messagebox.showerror("Error", "Invalid width", master=popup)
                popup.deiconify()
                return
            try:
                height = int(height_entry.get())
            except:
                messagebox.showerror("Error", "Invalid height", master=popup)
                popup.deiconify()
                return

            name = name_entry.get()
            popup.destroy()
            self.set_name(name)
            self.title("*" + name + "*")
            self.save_location = None
            self.canvas.destroy()
            self.canvas = Canvas((width, height), master=self)
            popup.destroy()

        def cancel(event=None):
            popup.destroy()

        button_frame = tkinter.Frame(popup)

        cancel_button = ttk.Button(button_frame, text="Cancel", command=cancel)
        cancel_button.bind("<Return>", cancel)
        cancel_button.grid(row=0, column=0)
        ok_button = ttk.Button(button_frame, text="OK", command=create_new)
        ok_button.bind("<Return>", create_new)
        ok_button.grid(row=0, column=1)

        input_frame.pack(padx=20, pady=20)
        button_frame.pack(padx=20, pady=20, side="right")
        popup.mainloop()


    def open(self, event=None):
        """
        Open a saved warcode map
        """

        if not self.check_unsaved("Open"):
            return

        initial_directory = os.path.abspath(os.path.join(__my_dir__, os.pardir, "maps"))
        mask = [("Warcode Maps", "*.wcm"), ("All Files", "*.*")]
        file = filedialog.askopenfile(initialdir=initial_directory,
            filetypes=mask, mode="r")
        if file is None:
            return
        self.save_location=file.name

        data = json.load(file)
        file.close()

        self.canvas.destroy()
        self.canvas = Canvas(
            (data["width"], data["height"]),
            master=self,
            game_map=data["board"],
            starting_locations=data["starting_locations"]
        )

        self.canvas.pack()
        self.set_name(data["name"])
        self.num_players_string.set(str(data["players"]) + " Players")
        self.update_num_players()
        self.set_unsaved_changes(False)

    def save(self, event=None):
        """
        Save our map, asking for a save location if one is not yet chosen
        """
        if self.save_location is None:
            self.save_as()
        else:
            file = open(self.save_location, "w")
            data = {
                "name": self.name,
                "players": self.num_players,
                "width": self.canvas.get_map_width(),
                "height": self.canvas.get_map_height(),
                "starting_locations": self.canvas.get_starting_locations(),
                "board": self.canvas.get_map()
            }
            json.dump(data, file)
            file.close()

        self.set_unsaved_changes(False)


    def save_as(self, event=None):
        """
        Save our map as a different file
        """
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
            "players": self.num_players,
            "width": self.canvas.get_map_width(),
            "height": self.canvas.get_map_height(),
            "starting_locations": self.canvas.get_starting_locations(),
            "board": self.canvas.get_map()
        }
        json.dump(data, file)
        file.close()
        self.set_unsaved_changes(False)

    def quit(self, event=None):
        """
        Actions to be taken upon quiting
        """
        if self.check_unsaved("Quit"):
            self.destroy()

    def check_unsaved(self, title="Continue",
            message="You still have unsaved changes. Are you sure you want to continue?"):
        """
        Checks with the user if they want to do an action even though they have
        unsaved changes.
        """
        if not self.unsaved_changes:
            return True
        else:
            return messagebox.askokcancel(title, message)

    def mouse_click(self, event, diff=1):
        """
        Process the user clicking somewhere, telling the canvas and map to update
        places according to the symmetry, number of players, and tool
        """
        def next_player(player_name, diff):
            num = int(player_name[-1])
            num += diff
            if num > self.num_players:
                num -= self.num_players
            return "Team " + str(num)

        position = (event.x, event.y)
        positions = [position]
        if self.symmetry.get() == "None":
            pass
        elif self.symmetry.get() == "Horizontal":
            positions.append((event.x, self.canvas.winfo_height() - event.y))
        elif self.symmetry.get() == "Vertical":
            positions.append((self.canvas.winfo_width() - event.x, event.y))

        elif self.symmetry.get() == "Radial":
            center = (self.canvas.winfo_width()/2, self.canvas.winfo_height()/2)
            displacement = (position[0] - center[0], position[1] - center[1])
            cos_angle = math.cos(2*math.pi/self.num_players)
            sin_angle = math.sin(2*math.pi/self.num_players)
            for i in range(1, self.num_players):
                displacement = (
                    cos_angle*displacement[0] - sin_angle*displacement[1],
                    sin_angle*displacement[0] + cos_angle*displacement[1]
                )
                positions.append((displacement[0] + center[0], displacement[1] + center[1]))

        elif self.symmetry.get() == "DR Diagonal":
            positions.append((event.y, event.x))
        elif self.symmetry.get() == "UR Diagonal":
            positions.append((self.winfo_height() - event.y, self.winfo_width() - event.x))
        elif self.symmetry.get() == "Horizontal/Vertical":
            positions.append((self.winfo_width() - event.x, event.y))
            positions.append((self.winfo_width() - event.x, self.winfo_height() - event.y))
            positions.append((event.x, self.winfo_height() - event.y))

        if self.tool.get().startswith("Team"):
            positions_changed = [
                self.canvas.set_square_at_canvas_position(
                    position[0], position[1], next_player(self.tool.get(), i)
                ) for i, position in enumerate(positions)
            ]
        else:
            positions_changed = [
                self.canvas.set_square_at_canvas_position(
                    position[0], position[1], self.tool.get()
                ) for position in positions
            ]

        if  any(positions_changed):
            self.set_unsaved_changes(True)


class Canvas(tkinter.Canvas):
    def __init__(self, map_size, *args, game_map=None, starting_locations=None, **kwargs):
        # Find the optimal width and height
        if "width" not in kwargs and "height" not in kwargs:
            if 2*map_size[1] > map_size[0]:
                width, height = map_size[0]/map_size[1]*800, 800
            else:
                width, height = 1600, map_size[1]/map_size[0]*1600
        elif "width" in kwargs and "height" in kwargs:
            width = kwargs["width"]
            height = kwargs["height"]
            del kwargs["width"]
            del kwargs["height"]
        else:
            raise Exception("If one of width/height is provided, both must be provided.")

        # Run super constructor
        super().__init__(*args, width=width, height=height, **kwargs)
        self.pack()
        self.update()

        self.map_size = map_size

        # Create map array
        if game_map == None:
            self.game_map = [
                [
                    CONSTANTS["MAP_DATA"]["EMPTY"] for x in range(self.map_size[0])
                ] for y in range(self.map_size[1])
            ]
        else:
            self.game_map = game_map

        # Create array of starting locations for the players
        if starting_locations is None:
            self.starting_locations = [set() for i in range(6)] #6 players
        else:
            self.starting_locations = [set(tuple(location) for location in locations)
                for locations in starting_locations] + [set() for i in range(6 - len(starting_locations))]

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
        Adds a location to a team's starting locations, returning True if the
        location was not already in there
        """
        if (x, y) in self.starting_locations[team - 1]:
            return False
        else:
            self.starting_locations[team - 1].add((x, y))

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
        Sets the square at (x, y) to the type, updating the screen as well.
        Returns if the square changes in any way
        """

        changed = False
        if tool in ("Empty", "Team 1", "Team 2", "Team 3", "Team 4", "Team 5", "Team 6"):
            type = "EMPTY"
        elif tool == "Gold Mine":
            type = "GOLD_MINE"
        elif tool == "Tree":
            type = "TREE"
        elif tool == "Block":
            type = "BLOCK"

        if self.game_map[y][x] != CONSTANTS["MAP_DATA"][type]:
            changed = True
            self.game_map[y][x] = CONSTANTS["MAP_DATA"][type]

        if self.itemcget(self.squares[y][x], "fill") != self.tool_colors[tool]:
            self.itemconfig(self.squares[y][x], fill=self.tool_colors[tool])

        for team, positions in enumerate(self.starting_locations):
            if (x, y) in positions:
                if "Team " + str(team + 1) != tool:
                    changed = True
                    positions.remove((x, y))

        if tool in ("Team 1", "Team 2", "Team 3", "Team 4", "Team 5", "Team 6"):
            if self.add_starting_location(x, y, int(tool[-1])):
                changed = True

        return changed

    def set_square_at_canvas_position(self, canvas_x, canvas_y, tool):
        """
        Changes a square from a canvas position, returning True if the square
        changes in any way.
        """
        x, y = self.scale_back((canvas_x, canvas_y))
        if 0 <= x < self.map_size[0] and 0 <= y < self.map_size[1]:
            return self.set_square(x, y, tool)
        else:
            return False

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
