# class of the pieces
from dataclasses import dataclass
from my_types import Vector


@dataclass
class Piece:
    ascii_map = {
        "Black": {
            "King": "♔",
            "Queen": "♕",
            "Rook": "♖",
            "Bishop": "♗",
            "Knight": "♘",
            "Pawn": "♙",
        },
        "White": {
            "King": "♚",
            "Queen": "♛",
            "Rook": "♜",
            "Bishop": "♝",
            "Knight": "♞",
            "Pawn": "♟︎",
        },
    }

    base_vectors = {
        # Moves are in (x, y)
        "Pawn": ((0, 1), (-1, 1), (1, 1)),
        "Rook": ((0, 1), (0, -1), (1, 0), (-1, 0)),
        "Bishop": ((1, 1), (-1, 1), (1, -1), (-1, -1)),
        "Queen": ((1, 1), (-1, 1), (1, -1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)),
        "King": ((1, 1), (-1, 1), (1, -1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)),
        "Knight": (
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
            (1, 2),
            (-1, 2),
            (1, -2),
            (-1, -2),
        ),
    }

    def __init__(self, type, color):
        self.type: str = type
        self.color: str = color
        self.moves_valid: list[Vector] = []
        self.status_moved = False
        self.symbol = self.ascii_map[color][type]

    def __eq__(self, other) -> bool:
        return self.color == other.color

    def __str__(self):
        return self.symbol

    def get_base_vectors(self) -> tuple[Vector, ...]:
        return self.base_vectors[self.type]

    def add_move(self, vector: Vector):
        """adds an vector to moves_valid"""
        self.moves_valid.append(vector)

    def del_moves(self):
        self.moves_valid = []

    def change_moved_status(self):
        self.status_moved = True

    def get_pawn_d(self) -> int:
        if self.color == "Black":
            return 1
        return -1


# a = Piece("Knight", "Black")
# b = Piece("Pawn", "Black")
# c = Piece("Queen", "White")

# assert a == b, "True"
# assert a == c, "JOOOO"
# assert b == c, "XD"
