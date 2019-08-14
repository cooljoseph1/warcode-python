from warcode_starter import Player

class ExamplePlayer(Player):
    def first_turn(self):
        self.log("First Turn!")

    def turn(self):
        self.log(self.get_turn_number())

if __name__ == "__main__":
    ExamplePlayer("ExamplePlayer")
