from enum import StrEnum


class Piece:
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
        self.type = type
        self.color = color
        self.my_vectors = Piece.base_vectors[type]
        self.moves_valid = []
        self.status_moved = False

    def add_move(self, vector):
        """adds an vector to moves_valid"""
        self.moves_valid.append(vector)

        self.moves_valid = []


class PieceType(StrEnum):
    KING = "King"
    QUEEN = "Queen"
    BISHOP = "Bishop"
    KNIGHT = "Knight"
    ROOK = "Rook"
    PAWN = "Pawn"
