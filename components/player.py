# this the player class
from pieces import Piece


class Player:
    def __init__(self, color, name):
        self.color: str = color
        self.name: str = name
