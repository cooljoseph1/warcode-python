#!/usr/bin/env python3
import sys

class Logger:
    """
    Simple logger class
    """
    def __init__(self, stdout=sys.stdout, stderr=sys.stderr):
        self.stdout = stdout
        self.stderr = stderr

    def log(self, message):
        print(message, file=self.stdout)

    def log_error(self, message):
        print(message, file=self.stderr)
