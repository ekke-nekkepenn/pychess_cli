from pathlib import Path
from board import Board
from game import Game
from pieces import Piece, PieceType
from colors import Colors

# Custom Types
type Layout = tuple[tuple[str, ...], ...]


file_name = "layout_standard.csv"

# Paths
path_layout = Path() / "layouts" / file_name


def main():
    board = Board()
    layout = get_layout(path_layout)

    if not apply_layout(board, layout):
        print("Failed applying layout.")
        return

    game = Game()
    game.run(board)


def get_layout(fp: Path) -> Layout:
    with open(fp, "r") as f:
        layout = f.read().split()
        for i, e in enumerate(layout):
            layout[i] = tuple(e.split(","))

    return tuple(layout)


def apply_layout(b: Board, l: Layout) -> bool:
    """Create Piece objects and fill up game board"""
    # iterate over Layout
    for y, line in enumerate(l):
        for x, e in enumerate(line):
            # skip empty strings
            if not e:
                continue

            ptype = None
            pcolor = None
            # Get color and type e.g "bP" -> "Black" "Pawn"
            pcolor = Colors.WHITE if e[0] == "w" else Colors.BLACK
            for t in PieceType:
                if e[1] == t[0]:
                    ptype = t
                    break

            # check if failed for some reason
            if pcolor == None or ptype == None:
                return False

            p = Piece(pcolor, ptype)
            b.set_item(x, y, p)
    return True


if __name__ == "__main__":
    main()
