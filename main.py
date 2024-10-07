from game import Game
from components.board import Board


def main():
    # TODO: make sure glyphs are visible then enable them
    glpyh_mode = True
    board = Board(glyph_mode=glpyh_mode)
    game = Game(board)
    game.run()


if __name__ == "__main__":
    main()
