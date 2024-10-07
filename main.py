from game import Game
from board import Board


def main(argv):

    board = Board()
    game = Game(board)
    game.run()


if __name__ == "__main__":
    main(argv)
