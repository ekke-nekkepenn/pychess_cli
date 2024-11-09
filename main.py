from .game import Game
from .components.board import Board

from .modes.base_class import GameMode
from .modes.standard import Standard


def main():
    # TODO: make sure glyphs are visible then enable them
    glyph_mode = True
    board = Board(glyph_mode)
    # game = Game(board)
    # game.run()
    while True:
        print("(1) Standard\n(2) Puzzle\n(0) Exit")
        ipt = "1"

        match ipt:
            case "1":
                standard_game = Standard(board)
                results = standard_game.run()
            case "2":
                # puzzle mode
                raise NotImplementedError
            case "0":
                input("Exiting now. Press any key to continue.")
                return
            case _:
                print("thats not an option")
                continue


if __name__ == "__main__":
    main()


# # variables and constants
# file_names = [
#     "layout_standard.csv",
#     "layout_no_pawns.csv",
#     "layout_king_checked.csv",
# ]


# def get_layout(file_name) -> list[list[str]]:
#     layout = []
#     with open(file_name) as csv_file:
#         for s in csv_file.readlines():
#             s = s.strip()
#             l = s.split(",")
#             layout.append(l)
#     return layout


# def fill_board(b: board, layout):
#     colors = {"b": "black", "w": "white"}
#     piece_map = {
#         "p": "pawn",
#         "r": "rook",
#         "n": "knight",
#         "b": "bishop",
#         "q": "queen",
#         "k": "king",
#     }
#     for y, row in enumerate(layout):
#         for x, item in enumerate(row):
#             if not item:
#                 continue
#             type = piece_map[item[0].lower()]
#             color = colors[item[-1].lower()]

#             p = piece(type, color)
#             b.set_item(p, x, y)
