import sys

from colors import Colors
from board import Board
from player import Player
from game import Game


def main():
    # TODO Let user select "style" through terminal after running
    # Style Selection
    style = "Char"  # default style

    if len(sys.argv) > 1:
        if sys.argv[1] == "g":
            style = "Glyph"
        elif sys.argv[1] == "c":
            style = "Char"

    # TODO Let user select names and colors
    p1 = Player("Vendrick", Colors.WHITE)
    p2 = Player("Gwyn", Colors.BLACK)
    board = Board(style)

    game = Game(p1, p2, board)

    game.layout_handler.load_layout()
    game.layout_handler.apply_layout(game.board)
    game.run()


if __name__ == "__main__":
    main()
