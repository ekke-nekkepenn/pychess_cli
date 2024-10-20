from .game import Game
from .components.board import Board


def main():
    # TODO: make sure glyphs are visible then enable them
    glyph_mode = True
    board = Board(glyph_mode)
    game = Game(board)
    game.run()


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
