from enum import StrEnum
from dataclasses import dataclass, field

from colors import Colors
from pieces import Piece, PieceType
from vectors import Vector


class Color_Code(StrEnum):
    # ANSI color codes
    NO_COLOR = ""
    FG_BLACK = "30"
    FG_RED = "31"
    FG_GREEN = "32"
    FG_YELLOW = "33"
    FG_BLUE = "34"
    FG_MAGENTA = "35"
    FG_CYAN = "36"
    FG_WHITE = "37"
    #
    BG_BLACK = "40"
    BG_RED = "41"
    BG_GREEN = "42"
    BG_YELLOW = "43"
    BG_BLUE = "44"
    BG_MAGENTA = "45"
    BG_CYAN = "46"
    BG_WHITE = "47"


class Style(StrEnum):
    GLYPH = "glyph"
    CHAR = "char"


class Printer:
    """Colors work by using ANSI escape codes.
    ref: https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
    basically use "\x1bn[{...}m". replace Curly Braces with desired Code.
    You can use more than one code seperated by ";". E.g. "\x1bn35;14m"
    To reset a style use "\x1bn[0m" at the end of string
    """

    esc = "\x1b["

    sprite_sheets = {
        Style.GLYPH: {
            Colors.WHITE: {
                PieceType.KING: "♔",
                PieceType.QUEEN: "♕",
                PieceType.ROOK: "♖",
                PieceType.BISHOP: "♗",
                PieceType.KNIGHT: "♘",
                PieceType.PAWN: "♙",
                # None: "⬜",
            },
            Colors.BLACK: {
                PieceType.KING: "♚",
                PieceType.QUEEN: "♛",
                PieceType.ROOK: "♜",
                PieceType.BISHOP: "♝",
                PieceType.KNIGHT: "♞",
                PieceType.PAWN: "♟︎",
                # None: "⬛",
            },
            None: "  ",
        },
        Style.CHAR: {
            Colors.WHITE: {
                PieceType.KING: "wK",
                PieceType.QUEEN: "wQ",
                PieceType.ROOK: "wR",
                PieceType.BISHOP: "wB",
                PieceType.KNIGHT: "wN",
                PieceType.PAWN: "wP",
                None: "[]",
            },
            Colors.BLACK: {
                PieceType.KING: "bK",
                PieceType.QUEEN: "bQ",
                PieceType.ROOK: "bR",
                PieceType.BISHOP: "bB",
                PieceType.KNIGHT: "bN",
                PieceType.PAWN: "bP",
            },
            None: "  ",
        },
    }

    def __init__(self, style: Style):
        self.style = style
        self.fg_color_white = Color_Code.FG_WHITE
        self.fg_color_black = Color_Code.FG_BLACK
        self.bg_color_white = Color_Code.BG_MAGENTA
        self.bg_color_black = Color_Code.BG_GREEN

    def construct_printable(self, square: "Square") -> str:
        #TODO fg_color stays black for some reason despite the 
        #TODO correct value in the string at the end
        fg_color = ""
        bg_color = ""

        if square.color == Colors.WHITE:
            bg_color += self.bg_color_white
        else:
            bg_color += self.bg_color_black

        ptype = square.get_occ_type()
        pcolor = square.get_occ_color()

        if pcolor == Colors.WHITE:
            fg_color += self.fg_color_white
        elif pcolor == Colors.BLACK:
            fg_color += self.fg_color_black

        sprite = self.sprite_sheets[self.style][pcolor][ptype]
        return self.esc + bg_color + ";" + fg_color + "m" + sprite + self.esc + "0m"


@dataclass
class Square:
    xy: Vector
    occ: Piece | None = None  # occupant
    color: Colors = field(init=False)

    def __post_init__(self):
        if (self.xy.x + self.xy.y) % 2 == 0:
            self.color = Colors.WHITE
        else:
            self.color = Colors.BLACK

    def get_occ_type(self) -> None | PieceType:
        if self.occ is None:
            return None
        return self.occ.type

    def get_occ_color(self) -> None | Colors:
        if self.occ is None:
            return None
        return self.occ.color


class Board:
    def __init__(self):
        self.size = 8
        self.grid = self.__init_grid__()

    def __init_grid__(self) -> tuple[tuple[Square]]:
        grid = []
        for y in range(self.size):
            row = []
            for x in range(self.size):
                row.append(Square(xy=Vector(x, y)))
            grid.append(tuple(row))
        return tuple(grid)

    # ACCESS methods
    def get_item(self, pos: Vector) -> Piece | None:
        return self.grid[pos.y][pos.x].occ

    def set_item(self, pos: Vector, item: Piece | None):
        # this just accesses Squares Class which stores Piece
        self.grid[pos.y][pos.x].occ = item

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


# Tests
#prt = Printer(style=Style.CHAR)
#s1 = Square(Vector(1, 1))
#s2 = Square(Vector(5, 6))
#
#p1 = Piece(Colors.WHITE, PieceType.KING)
#p2 = Piece(Colors.BLACK, PieceType.PAWN)
#s1.occ = p1
#s2.occ = p2
#
#st1 = prt.construct_printable(s1)
#st2 = prt.construct_printable(s2)
