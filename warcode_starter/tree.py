#!/usr/bin/env python3
class Tree:
    def __init__(self, player, id, wood, x, y):
        self.player = player
        self.id = id
        self.wood = wood
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_location(self):
        return (self.x, self.y)

    def get_wood(self):
        return self.wood

    def subtract_wood(self, amount):
        self.wood -= amount
        if self.wood <= 0:
            self.player.remove_tree(self)

    def damage(self, amount):
        self.subtract_wood(amount)

    def distance_to(self, x, y):
        return (self.x - x)**2 + (self.y - y)**2
