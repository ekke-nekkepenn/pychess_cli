import re

from my_types import Point, Vector

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
