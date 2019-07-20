import tkinter

from warcode.constants import CONSTANTS
from warcode.engine import game_map


class Window(tkinter.Tk):
    """
    This class is a window that you can use to create a map
    """
    def __init__(self, canvas_size=(500, 500), map_size=(30, 30), name="Untitled", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.title(self.name)
        self.resizable(False, False)

        self.game_map = [[game_map.Empty().represent()
                          for x in range(map_size[0])] for y in range(map_size[1])]

        self.add_widgets(map_size, canvas_size)
        self.bind("<Button 1>", self.mouse_click)
        self.bind("<B1 Motion>", self.mouse_move)

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
        
        pass

    def save(self):
        pass

    def save_as(self):
        pass

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
        self.canvas.set_square_at(event.x, event.y, self.tool.get())

    def mouse_move(self, event):
        """
        Processes the user moving their mouse while holding it down
        """
        self.canvas.set_square_at(event.x, event.y, self.tool.get())


class Canvas(tkinter.Canvas):
    def __init__(self, map_size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.map_size = map_size

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
                    fill="white"
                ) for x in range(self.map_size[0])
            ] for y in range(self.map_size[1])
        ]

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

    def set_square_at(self, canvas_x, canvas_y, tool):
        x, y = self.scale_back((canvas_x, canvas_y))
        if 0 <= x < self.map_size[0] and 0 <= y < self.map_size[1]:
            self.itemconfig(self.squares[y][x], fill=self.tool_colors[tool])

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
