#!/usr/bin/env python3
import sys
from argparse import ArgumentParser

from viewer import Viewer

def main():
    parser = ArgumentParser(description="View a warcode replay.")
    parser.add_argument("replay", metavar="FILE", help="replay to view")
    parser.add_argument("-W", "--width", help="width of viewer")
    parser.add_argument("-H", "--height", help="height of viewer")

    args = parser.parse_args()

    Viewer(args.replay, args.width, args.height)

if __name__ == "__main__":
    main()
