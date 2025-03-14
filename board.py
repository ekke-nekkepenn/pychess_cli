from colors import Colors
from pieces import Piece


class Board:
    def __init__(self):
        self.field = self.__generate_field__()

    def __generate_field__(self):
        # 8x8 tuple with [None] filled
        return tuple([tuple([[None] for _ in range(8)]) for _ in range(8)])

    def printb(self):
        pass

    def set_item(self, x, y, item):
        # elements in field are each a list with one element
        # acces item with [0]
        self.field[y][x][0] = item

    def remove_item(self, x, y) -> Piece | None:
        e = self.field[y][x][0]
        if e:
            self.field[y][x][0] = None
        return e


# class BoardPrinter:
# glyphs = {
# "W": {"K": "♔", "Q": "♕", "R": "♖", "B": "♗", "K": "♘", "P": "♙", None: "⬜"},
# "B": {"K": "♚", "Q": "♛", "R": "♜", "B": "♝", "K": "♞", "P": "♟︎", None: "⬛"},
# }
