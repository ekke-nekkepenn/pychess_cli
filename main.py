from sys import argv

from game import Game
from pieces import Piece
from player import Player
from board import Board


# Variables and Constants
file_names = [
    "layout_standard.csv",
    "layout_no_pawns.csv",
    "layout_king_checked.csv",
]


def get_layout(file_name) -> list[list[str]]:
    layout = []
    with open(file_name) as csv_file:
        for s in csv_file.readlines():
            s = s.strip()
            l = s.split(",")
            layout.append(l)
    return layout


def fill_board(b: Board, layout):
    colors = {"b": "Black", "w": "White"}
    piece_map = {
        "p": "Pawn",
        "r": "Rook",
        "n": "Knight",
        "b": "Bishop",
        "q": "Queen",
        "k": "King",
    }
    for y, row in enumerate(layout):
        for x, item in enumerate(row):
            if not item:
                continue
            type = piece_map[item[1].lower()]
            color = colors[item[0].lower()]

            p = Piece(type, color)
            b.set_item(p, x, y)


def main(argv):
    if len(argv) == 3:
        white, black = argv[1], argv[2]
    else:
        black, white = "Player 2", "Player 1"

    p1 = Player(white, "White")
    p2 = Player(black, "Black")

    board = Board()

    file_path = "./layouts/" + file_names[0]
    layout = get_layout(file_path)
    fill_board(board, layout)

    game = Game(board, p1, p2)
    game.run()


if __name__ == "__main__":
    main(argv)
