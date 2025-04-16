from colors import Colors
from pieces import Piece, PieceType
from dataclasses import dataclass

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
}


@dataclass
class Square:
    x: int
    y: int
    occ: Piece | None = None  # occupant


class Board:
    def __init__(self, letters_on=True):
        self.field = self.__generate_field__()
        self.letters_on = letters_on
        self.p = Printer()

    def __generate_field__(self) -> tuple[tuple[Square], ...]:
        # 8x8 tuple with [None] filled
        # return tuple([tuple([[None] for _ in range(8)]) for _ in range(8)])
        field = []
        for y in range(8):
            row = []
            for x in range(8):
                row.append(Square(x, y))
            field.append(tuple(row))
        return tuple(field)

    def printb(self):
        self.p.print_field(self.field, self.letters_on)

    def get_item(self, x, y) -> Piece | None:
        return self.field[y][x].occ

    def set_item(self, x, y, item: Piece | None):
        # elements in field are each a list with one element
        # acces item with [0]
        self.field[y][x].occ = item

    def remove_item(self, x, y) -> Piece | None:
        e = self.field[y][x].occ
        if e:
            self.field[y][x] = None
        return e


class Printer:
    def __init__(self):
        pass

    def print_field(self, field, mode):
        if mode:
            self.print_letters(field)
        else:
            self.print_glyphs(field)

    def print_letters(self, field):
        for y, row in enumerate(field):
            for x, square in enumerate(row):
                piece = square.occ
                if piece is None:
                    c = Colors.WHITE if (y + x) % 2 == 0 else Colors.BLACK
                    t = None
                    sprite = Sprite_letters[c][t]
                else:
                    c = piece.color
                    t = piece.type
                    sprite = Sprite_letters[c][t]
                print(sprite, end=" ")
            print()

    def print_glyphs(self, field):
        for y, row in enumerate(field):
            for x, square in enumerate(row):
                piece = square.occ
                if piece is None:
                    c = Colors.WHITE if (y + x) % 2 == 0 else Colors.BLACK
                    t = None
                    sprite = Sprite_glyphs[c][t]
                else:
                    c = piece.color
                    t = piece.type
                    sprite = Sprite_glyphs[c][t]
                print(sprite, end=" ")
            print()
