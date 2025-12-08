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
        if sys.argv[1] == "-g":
            style = "Glyph"
        elif sys.argv[1] == "-c":
            style = "Char"
        elif sys.argv[1] in ("-h", "--help"):
            print("Usage: python main.py [flag]")
            print("\t-g\tUse Unicode Symbols (Glyphs)")
            print("\t-c\tUse ASCII characters. Is the default flag")
            print("\t-h\tPrint this Help message")
            print("\t--help\tPrint this Help message")

            return

    p1 = Player("Vendrick", Colors.WHITE)
    p2 = Player("Gwyn", Colors.BLACK)

    # TODO Board and Printer interaction changed
    board = Board()
    game = Game(p1, p2, board)
    game.layout_handler.load_layout()
    game.layout_handler.apply_layout(game.board)
    game.run()


if __name__ == "__main__":
    main()
