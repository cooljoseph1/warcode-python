#!/usr/bin/env python3
import sys
from argparse import ArgumentParser

from warcode.viewer import Viewer

def main():
    parser = ArgumentParser(description="View a warcode replay.")
    parser.add_argument("replay", metavar="FILE", help="replay to view")
    parser.add_argument("-w", "--width", help="width of viewer")
    parser.add_argument("-h", "--height", help="height of viewer")

    parser.parse_args()

    Viewer(parser.replay, parser.width, parser.height)

if __name__ == "__main__":
    main()
