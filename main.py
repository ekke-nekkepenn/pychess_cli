import sys
from pathlib import Path
from board import Board
from game import Game
from pieces import Piece, PieceType
from colors import Colors

# Custom Types
# type Layout = tuple[tuple[str, ...], ...]


file_name = [
    "layout_standard.csv",
    "layout_testing.csv",
    "test2.csv",
    "test_exposed.csv",
]


# Paths
path_layout = Path(".") / "layouts" / file_name[3]


def main():
    # TEST COMMENT
    # Style Selection
    style = "Char"  # default style

    if len(sys.argv) > 1:
        if sys.argv[1] == "g":
            style = "Glyph"
        elif sys.argv[1] == "c":
            style = "Char"

    # Style Selection

    board = Board(style)
    layout = get_layout(path_layout)

    if not apply_layout(board, layout):
        print("Failed applying layout.")
        return

    game = Game()
    game.run(board)


def get_layout(fp: Path):
    with open(fp, "r") as f:
        split_text = f.read().split()
        layout = []
        for string in split_text:
            layout.append(tuple(string.split(",")))

    return tuple(layout)


def apply_layout(b: Board, layout) -> bool:
    """Create Piece objects and fill up game board"""
    # iterate over Layout
    for y, line in enumerate(layout):
        for x, e in enumerate(line):
            # skip empty string -> ""
            if not e:
                continue

            ptype = None
            pcolor = None
            # Get color and type e.g "bP" -> "Black" "Pawn"
            pcolor = Colors.WHITE if e[0] == "w" else Colors.BLACK
            # iter over Enum and check if first letter match
            for t in PieceType:
                if t != "Knight":
                    if e[1] == t[0]:
                        ptype = t
                        break
                # except Knight which uses 'N' as identifier
                else:
                    ptype = t

            # check if failed for some reason
            if pcolor == None or ptype == None:
                return False

            p = Piece(pcolor, ptype)
            b.set_item(x, y, p)

    return True


if __name__ == "__main__":
    main()
