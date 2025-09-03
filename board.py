from dataclasses import dataclass

from colors import Colors
from pieces import Piece, PieceType
from vectors import Vector

Sprite_letters = {
    "White": {
        "King": "wK",
        "Queen": "wQ",
        "Rook": "wR",
        "Bishop": "wB",
        "Knight": "wN",
        "Pawn": "wP",
        None: "[]",
    },
    "Black": {
        "King": "bK",
        "Queen": "bQ",
        "Rook": "bR",
        "Bishop": "bB",
        "Knight": "bN",
        "Pawn": "bP",
        None: "{}",
    },
    "Marked": "XX",
}

Sprite_glyphs = {
    "White": {
        "King": "♔",
        "Queen": "♕",
        "Rook": "♖",
        "Bishop": "♗",
        "Knight": "♘",
        "Pawn": "♙",
        None: "⬜",
    },
    "Black": {
        "King": "♚",
        "Queen": "♛",
        "Rook": "♜",
        "Bishop": "♝",
        "Knight": "♞",
        "Pawn": "♟︎",
        None: "⬛",
    },
    "Marked": "XX",
}


@dataclass
class Square:
    """just a cointainer for Piece instances"""

    occ: Piece | None = None  # occupant


class Board:
    def __init__(self, style="Char"):
        self.grid = self.__init_grid__()
        self.style = style
        self.printer = Printer()

    def __init_grid__(self) -> tuple[tuple[Square]]:
        grid = []
        for y in range(8):
            row = []
            for x in range(8):
                row.append(Square())
            grid.append(tuple(row))
        return tuple(grid)

    def printb(self, marked=None):
        self.printer.print_grid(self.grid, self.style, marked)

    # ACCESS methods
    def get_item(self, pos: Vector) -> Piece | None:
        return self.grid[pos.y][pos.x].occ

    def set_item(self, pos: Vector, item: Piece | None):
        # this just accesses Squares Class which stores Piece
        self.grid[pos.y][pos.x].occ = item

    def remove_item(self, pos: Vector) -> Piece | None:
        e = self.get_item(pos)
        if e:
            self.set_item(pos, None)
        return e

    def move(self, pos_og: Vector, pos_new: Vector) -> Piece | None:
        # TODO refactor for Vectors
        # moves p to dest and returns what is at dest
        p = self.get_item(pos_og)
        if p is None:
            print("cannot move None")
            raise ValueError

        self.set_item(pos_og, None)
        removed_item = self.get_item(pos_new)
        self.set_item(pos_new, p)
        return removed_item


class Printer:
    def __init__(self):
        pass

    def print_grid(self, grid, style, marked=None):
        if style == "Char":
            self.print_char(grid, marked)
        elif style == "Glyph":
            self.print_glyphs(grid, marked)

    def print_char(self, grid, marked):
        if marked is None:
            marked = []

        for y, row in enumerate(grid):
            for x, square in enumerate(row):
                piece = square.occ

                if (x, y) in marked:
                    sprite = Sprite_letters["Marked"]

                elif piece is None:
                    c = Colors.WHITE if (y + x) % 2 == 0 else Colors.BLACK
                    t = None
                    sprite = Sprite_letters[c][t]
                else:
                    c = piece.color
                    t = piece.type
                    sprite = Sprite_letters[c][t]
                print(sprite, end=" ")
            print()

    def print_glyphs(self, grid, marked):
        if marked is None:
            marked = []

        for y, row in enumerate(grid):
            for x, square in enumerate(row):
                piece = square.occ

                if (x, y) in marked:
                    sprite = Sprite_glyphs["Marked"]

                elif piece is None:
                    c = Colors.WHITE if (y + x) % 2 == 0 else Colors.BLACK
                    t = None
                    sprite = Sprite_glyphs[c][t]
                else:
                    c = piece.color
                    t = piece.type
                    sprite = Sprite_glyphs[c][t]
                print(sprite, end=" ")
            print()
