from dataclasses import dataclass
from enum import StrEnum

import colorama

# REMOVE THIS
from game import LayoutHandler

# REMOVE THIS

from colors import Colors
from pieces import Piece, PieceType
from vectors import Vector


class Style(StrEnum):
    GLYPH = "glyph"
    CHAR = "char"


class Printer:
    sprite_sheets = {
        Style.GLYPH: {
            Colors.WHITE: {
                PieceType.KING: "♔",
                PieceType.QUEEN: "♕",
                PieceType.ROOK: "♖",
                PieceType.BISHOP: "♗",
                PieceType.KNIGHT: "♘",
                PieceType.PAWN: "♙",
            },
            Colors.BLACK: {
                PieceType.KING: "♚",
                PieceType.QUEEN: "♛",
                PieceType.ROOK: "♜",
                PieceType.BISHOP: "♝",
                PieceType.KNIGHT: "♞",
                PieceType.PAWN: "♟︎",
            },
            None: {None: " "},
        },
        Style.CHAR: {
            Colors.WHITE: {
                PieceType.KING: "wK",
                PieceType.QUEEN: "wQ",
                PieceType.ROOK: "wR",
                PieceType.BISHOP: "wB",
                PieceType.KNIGHT: "wN",
                PieceType.PAWN: "wP",
            },
            Colors.BLACK: {
                PieceType.KING: "bK",
                PieceType.QUEEN: "bQ",
                PieceType.ROOK: "bR",
                PieceType.BISHOP: "bB",
                PieceType.KNIGHT: "bN",
                PieceType.PAWN: "bP",
            },
            None: {None: "  "},
        },
    }

    def __init__(self, style: Style, color_mode: bool):
        self.style = style
        self.color_mode = color_mode

    def print_board(self, board: "Board"):
        n_pad = 3
        left_pad = n_pad * "\t"

        size_dep = 2 if self.style == Style.GLYPH else 1

        size = " " * size_dep

        for i, row in enumerate(board.grid):
            print(left_pad, end="")
            print(f"{board.size-i}", end=" ")

            for j, square in enumerate(row):
                # print board legend on left side (1-8)

                symbol = self.construct_symbol(square)
                print(f"{symbol}", end=f"{size}{colorama.Style.RESET_ALL}")

            print()

        # print the board legend (A-H) under borad
        print(left_pad, end=" " * 2)
        for i in range(board.size):
            # chr(65) is "A"
            print(f" {chr(i+65)}", end=size)
        print()

    def construct_symbol(self, square: "Square") -> str:
        symbol = ""
        occt = square.get_occ_type()
        occc = square.get_occ_color()
        sprite = self.sprite_sheets[self.style][occc][occt]
        symbol += sprite
        pad = ""
        if self.color_mode:
            pad = " "
            bg_color = (
                colorama.Back.BLACK
                if square.color == Colors.BLACK
                else colorama.Back.RED
            )
            fg_color = colorama.Fore.WHITE
            symbol = f"{bg_color}{fg_color}{pad}{sprite}"
        return symbol


@dataclass
class Square:
    coord: Vector
    color: Colors
    occ: Piece | None = None  # occupant

    def get_occ_type(self) -> None | PieceType:
        return self.occ.type if self.occ else None

    def get_occ_color(self) -> None | Colors:
        return self.occ.color if self.occ else None


class Board:
    def __init__(self):
        self.size = 8
        self.grid = self.__init_grid__()

    def __init_grid__(self) -> tuple[tuple[Square]]:
        grid = []
        for y in range(self.size):
            row = []
            for x in range(self.size):
                c = Colors.BLACK if (x + y) % 2 != 0 else Colors.WHITE
                row.append(Square(coord=Vector(x, y), color=c))
            grid.append(tuple(row))
        return tuple(grid)

    def get_item(self, pos: Vector) -> Piece | None:
        return self.grid[pos.y][pos.x].occ

    def set_item(self, pos: Vector, item: Piece | None):
        sqr: Square = self.grid[pos.y][pos.x]
        sqr.occ = item

    def remove_item(self, pos: Vector) -> Piece | None:
        p = self.get_item(pos)
        if p:
            self.set_item(pos, None)
        return p

    def move(self, pos_og: Vector, pos_new: Vector) -> Piece | None:
        # moves p to dest and return what is at dest
        if pos_og == pos_new:
            print("Cannot move to the same square")
            raise ValueError("Origin and destination squares are the same.")

        p = self.get_item(pos_og)
        if p is None:
            print("cannot move None")
            raise ValueError

        self.set_item(pos_og, None)
        removed_item = self.get_item(pos_new)
        self.set_item(pos_new, p)
        return removed_item


colorama.just_fix_windows_console()

# Tests
s1 = Square(Vector(0, 0), Colors.WHITE)
s2 = Square(Vector(1, 0), Colors.BLACK)
s3 = Square(Vector(2, 0), Colors.WHITE)
s4 = Square(Vector(3, 0), Colors.BLACK)

p1 = Piece(Colors.WHITE, PieceType.KING)
p2 = Piece(Colors.WHITE, PieceType.KNIGHT)

p3 = Piece(Colors.BLACK, PieceType.PAWN)
p4 = Piece(Colors.BLACK, PieceType.ROOK)

s1.occ = p1
# s2.occ = p2
s3.occ = p3
# s4.occ = p4

prt = Printer(style=Style.GLYPH, color_mode=True)

# st1 = prt.construct_symbol(s1)
# st2 = prt.construct_symbol(s2)
# st3 = prt.construct_symbol(s3)
# st4 = prt.construct_symbol(s4)


# print(st1, end="")
# print(st2, end="")
# print(st3, end="")
# print(st4, end="")
# print()

board = Board()

layout_handler = LayoutHandler()
layout_handler.load_layout()
layout_handler.apply_layout(board)

prt.print_board(board)
