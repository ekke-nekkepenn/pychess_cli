from ..components.pieces import Piece, PieceType
from ..components.colors import Colors


class GameMode:
    def get_layout(self, fp):
        """loads a layout from a file and turns certain strings into Piece|None."""
        color_map = {"b": Colors.BLACK, "w": Colors.WHITE}
        piece_map = {
            "P": PieceType.PAWN,
            "R": PieceType.ROOK,
            "N": PieceType.KNIGHT,
            "B": PieceType.BISHOP,
            "Q": PieceType.QUEEN,
            "K": PieceType.KING,
        }

        with open(fp) as file:
            layout = []
            for line in file.read().split():
                line = line.split(",")

                # convert strings to Piece|None
                for i, item in enumerate(line):
                    if not item:
                        item = None
                        continue
                    type = piece_map[item[1]]
                    color = color_map[item[0]]
                    line[i] = Piece(type, color)

                layout.append(tuple(line))
        return tuple(layout)
