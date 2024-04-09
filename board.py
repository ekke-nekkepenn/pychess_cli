from pieces import Piece

from my_types import Vector, Point

ChessFile = list[Piece | None]


class Board:
    white_square = "◼"
    black_square = "◻"

    def __init__(self):
        self.board: list[ChessFile] = [[None for _ in range(8)] for _ in range(8)]

    def __getitem__(self, tup) -> None | Piece:
        """You can add an item by using board[(x, y)]"""
        return self.board[tup[1]][tup[0]]

    def set_item(self, item: None | Piece, x: int, y: int):
        self.board[y][x] = item

    def remove_item(self, x, y) -> None | Piece:
        item = self.board[y].pop(x)
        self.board[y].insert(x, None)
        return item

    def where_is_all(self) -> list[tuple[Point, Piece]]:
        all = []
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if not piece:
                    continue
                all.append(((x, y), piece))
        return all

    def printb(self, highlights=None):
        if highlights is None:
            highlights = ()

        print("     A  B  C  D  E  F  G  H ")
        print("  |‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
        for y, row in enumerate(self.board):
            for x, item in enumerate(row):
                if x == 0:
                    print(f"{8 - y}", end=" | ")

                if (x, y) in highlights:
                    # print(" X", end=" ")
                    print(f" X", end=" ")

                elif not item:
                    print(f" {self.black_square}", end=" ")
                    # uncomment to have alternating square colors
                    # if self.is_square_white(x, y):
                    #     print(f" {self.white_square}", end=" ")
                    # else:
                    #     print(f" {self.black_square}", end=" ")
                else:
                    print(f" {item}", end=" ")
            print()

    @staticmethod
    def is_square_white(x: int, y: int) -> bool:
        """black squares -> odd (False) | white squares -> even (True)"""
        return (x + y) % 2 == 0
