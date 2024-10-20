from ..components.pieces import Piece, PieceType
from ..components.colors import Colors


class GameMode:
    piece_dict = {
        "P": PieceType.PAWN,
        "R": PieceType.ROOK,
        "N": PieceType.KNIGHT,
        "B": PieceType.BISHOP,
        "Q": PieceType.QUEEN,
        "K": PieceType.KING,
    }

    def get_layout(self, fp):
        with open(fp) as file:
            layout = []
            for line in file.read().strip():
                line = line.strip(",")
                layout.append(tuple(line))
        return tuple(layout)
