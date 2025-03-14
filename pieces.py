from enum import StrEnum


class PieceType(StrEnum):
    KING = "King"
    QUEEN = "Queen"
    BISHOP = "Bishop"
    KNIGHT = "Knight"
    ROOK = "Rook"
    PAWN = "Pawn"


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


class Piece:
    def __init__(self, type, color):
        self.type = type
        self.color = color
        self.status_moved = False
