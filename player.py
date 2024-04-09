# this the player class
from dataclasses import dataclass
from pieces import Piece


@dataclass
class Player:
    color: str
    name: str
    pieces_captured = []

    def __str__(self):
        return self.color.capitalize()

    def show_captured_pieces(self):
        print(self.pieces_captured)

    def capture_piece(self, p: Piece):
        self.pieces_captured.append(p)
