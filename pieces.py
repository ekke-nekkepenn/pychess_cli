from enum import StrEnum
from dataclasses import dataclass


class PieceType(StrEnum):
    KING = "King"
    QUEEN = "Queen"
    BISHOP = "Bishop"
    KNIGHT = "Knight"
    ROOK = "Rook"
    PAWN = "Pawn"


#
@dataclass
class Piece:
    color: str
    type: str
    status_moved = False

    # need custom hash function or else Piece() instances with same fields have same hash
    def __hash__(self):
        return id(self)
