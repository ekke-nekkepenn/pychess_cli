from colors import Colors


class Board:
    SIZE = 8

    def __init__(self, glyph_mode=False):
        self.printer = BoardPrinter(glyph_mode)

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


class BoardPrinter:
    glyphs = {
        "W": {
            "K": "♔",
            "Q": "♕",
            "R": "♖",
            "B": "♗",
            "K": "♘",
            "P": "♙",
        },
        "B": {
            "K": "♚",
            "Q": "♛",
            "R": "♜",
            "B": "♝",
            "K": "♞",
            "P": "♟︎",
        },
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
                    print(f"{8 - y}", end=" | ")

                # print either "X" for highlights or Square.color or Square.occupant
                if (x, y) in highlights:
                    print(f"XX", end=" ")

                if not square.occupant:
                    print(square.color, end=" ")

                else:
                    # fetch symbol from glyph hash
                    glyph = self.glyphs[square.occupant[0]]
                    print(glyph, end=" ")

            print()


if __name__ == "__main__":
    b = Board()
    b.printb()
