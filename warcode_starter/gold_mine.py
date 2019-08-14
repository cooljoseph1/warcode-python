#!/usr/bin/env python3
class GoldMine:
    def __init__(self, player, id, gold, x, y):
        self.player = player
        self.id = id
        self.gold = gold
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_location(self):
        return (self.x, self.y)

    def get_gold(self):
        return self.gold

    def subtract_gold(self, amount):
        self.gold -= amount
        if self.gold <= 0:
            self.player.remove_gold_mine(self)

    def damage(self, amount):
        self.subtract_gold(amount)

    def distance_to(self, x, y):
        return (self.x - x)**2 + (self.y - y)**2
