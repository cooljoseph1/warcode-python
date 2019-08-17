#!/usr/bin/env python3
import tkinter
from warcode.viewer import Canvas, Replay

class Viewer(tkinter.Tk):
    def __init__(self, replay_name, width=None, height=None):
        self.replay = Replay(replay_name)
