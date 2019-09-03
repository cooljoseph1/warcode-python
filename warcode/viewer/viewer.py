#!/usr/bin/env python3
import tkinter
from canvas import Canvas
from replay import Replay

class Viewer(tkinter.Tk):
    def __init__(self, replay_name, width=None, height=None):
        self.replay = Replay(replay_name)

        if not width or not height:
            height = 700
            width = self.replay.width / self.replay.height * height

        self.canvas = Canvas(self, width, height, replay.width, replay.height)
