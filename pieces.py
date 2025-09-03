from enum import StrEnum
from colors import Colors
from dataclasses import dataclass


class PieceType(StrEnum):
    KING = "King"
    QUEEN = "Queen"
    BISHOP = "Bishop"
    KNIGHT = "Knight"
    ROOK = "Rook"
    PAWN = "Pawn"


@dataclass
class Piece:
    color: Colors
    type: PieceType
    unmoved = True

    # need custom hash function or else Piece() instances with same fields have same hash
    def __hash__(self):
        return id(self)
