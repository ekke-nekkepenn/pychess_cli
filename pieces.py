from enum import StrEnum
from dataclasses import dataclass

from vectors import Vector
from colors import Colors


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

    def get_symbol(self) -> str:
        if self.type != PieceType.KNIGHT:
            return self.type[0]
        return self.type[1].capitalize()

    def get_color_symbol(self) -> str:
        return self.color[0].lower()


# Shared Vectors x, y
v_U = Vector(0, -1)
v_D = Vector(0, 1)
v_R = Vector(1, 0)
v_L = Vector(-1, 0)

v_UR = Vector(1, -1)
v_DR = Vector(1, 1)
v_UL = Vector(-1, -1)
v_DL = Vector(-1, 1)

ALL_BASE_VECTORS: dict[PieceType, tuple[Vector,...]] = {
    PieceType.PAWN: (
        v_D,
        v_DR,
        v_DL,
    ),  # need to multiply each by -1 for other direction
    PieceType.ROOK: (v_D, v_U, v_R, v_L),
    PieceType.KNIGHT: (
        v_R + v_DR,
        v_R + v_UR,
        v_L + v_DL,
        v_L + v_UL,
        v_D + v_DR,
        v_D + v_DL,
        v_U + v_UR,
        v_U + v_UL,
    ),
    PieceType.BISHOP: (v_DR, v_DL, v_UR, v_UL),
    PieceType.QUEEN: (v_D, v_U, v_R, v_L, v_DR, v_DL, v_UR, v_UL),
    PieceType.KING: (v_D, v_U, v_R, v_L, v_DR, v_DL, v_UR, v_UL),
}
