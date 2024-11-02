from turtle import color
from .colors import Colors
from .pieces import Piece, PieceType


class Board:
    def __init__(self, glyph_mode):
        self.SIZE = 8
        self.printer = BoardPrinter(glyph_mode)

        # board creation Square instances are created
        self.array2D = []
        for y in range(self.SIZE):
            tmp = []
            for x in range(self.SIZE):
                if (x + y) % 2 != 0:
                    color = Colors.BLACK
                else:
                    color = Colors.WHITE
                tmp.append(Square(color))
            self.array2D.append(tuple(tmp))
        self.array2D = tuple(self.array2D)

    def printb(self):
        self.printer.printb(self.array2D)

    def is_point_oob(self, x, y) -> bool:
        return not (0 <= x <= self.SIZE and 0 <= y <= self.SIZE)

    def set_item(self, x, y, item):
        square = self.array2D[y][x]
        square.set_item(item)

    def load_layout(self, layout):
        for y, line in enumerate(layout):
            for x, item in enumerate(line):
                self.set_item(x, y, item)

    def convert_chess_notation_to_coordinate(self, s: str) -> tuple[int, int]:
        m = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        x = m[s[0].lower()]
        y = 8 - int(s[1])
        return x, y

    # def __getitem__(self, tup) -> None | Piece:
    #     """You can add an item by using board[(x, y)]"""
    #     return self.board[tup[1]][tup[0]]

    # def set_item(self, item: None | Piece, x: int, y: int):
    #     self.board[y][x] = item

    # def remove_item(self, x, y) -> None | Piece:
    #     item = self.board[y].pop(x)
    #     self.board[y].insert(x, None)
    #     return item

    # @staticmethod
    # def is_square_white(x: int, y: int) -> bool:
    #     """black squares -> odd (False) | white squares -> even (True)"""
    #     return (x + y) % 2 == 0


class Square:
    def __init__(self, color):
        self.color = color
        self.occupant = None  # either None or Piece

    def set_item(self, item):
        self.occupant = item


class BoardPrinter:
    glyphs = {
        "W": {"K": "♔", "Q": "♕", "R": "♖", "B": "♗", "K": "♘", "P": "♙", None: "⬜"},
        "B": {"K": "♚", "Q": "♛", "R": "♜", "B": "♝", "K": "♞", "P": "♟︎", None: "⬛"},
    }

    def __init__(self, glpyh_mode=False):
        self.glyph_mode = glpyh_mode

    def printb(self, board, highlights=None):
        if highlights is None:
            highlights = ()

        print("     A  B  C  D  E  F  G  H ")
        print("  |‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
        for y, row in enumerate(board):
            for x, square in enumerate(row):
                if x == 0:
                    print(f"{len(board) - y}", end=" | ")

                # print either "X" for highlights or Square.color or Square.occupant
                if (x, y) in highlights:
                    print(f"XX", end=" ")

                elif not square.occupant:
                    color_key = square.color[0]
                    glyph = self.glyphs[color_key][None]
                    print(glyph, end=" ")

                else:
                    color_key = square.occupant.color[0]
                    type_key = square.occupant.type[0]

                    glyph = self.glyphs[color_key][type_key]
                    print(glyph + " ", end=" ")

            print()


if __name__ == "__main__":
    b = Board()
    b.printb()
