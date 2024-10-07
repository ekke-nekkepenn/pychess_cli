import re

# Chess Notation
pattern_chess_notation = r"[A-H][1-8]"

re_chess = re.compile(pattern_chess_notation, re.IGNORECASE)


def contains_chess_coord(ipt) -> str | None:
    """if match found. First match is returned else 'None'"""
    if m := re_chess.search(ipt):
        return m.group(0)
    return m


def parse_chess_notation(s: str) -> Point:
    m = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    x = m[s[0].lower()]
    y = 8 - int(s[1])
    return x, y


def is_point_oob(x, y) -> bool:
    if x < 0 or x > 7:
        return True
    if y < 0 or y > 7:
        return True
    return False


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
            type = piece_map[item[0].lower()]
            color = colors[item[-1].lower()]

            p = Piece(type, color)
            b.set_item(p, x, y)
