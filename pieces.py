from enum import StrEnum
from dataclasses import dataclass
from colors import Colors


class PieceType(StrEnum):
    KING = "King"
    QUEEN = "Queen"
    BISHOP = "Bishop"
    KNIGHT = "Knight"
    ROOK = "Rook"
    PAWN = "Pawn"


# eq & frozen == true so we can use it as key in a dict
@dataclass(eq=True, frozen=True)
class Piece:
    color: Colors
    type: PieceType
    status_moved = False
