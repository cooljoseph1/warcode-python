#!/usr/bin/env python3
import sys
import os
my_dir = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(my_dir, os.pardir))

from warcode.engine import Engine


if __name__ == "__main__":
    engine = Engine("Arrow", ["exampleplayer.py", "exampleplayer.py"])
    engine.play()
