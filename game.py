from board import Board
from colors import Colors
from pieces import Piece, PieceType
from dataclasses import dataclass

# keys are coordinates on board and valuesa are a list of vectors
# moves get recalculated after each turn
all_valid_moves = {}


class Game:
    def __init__(self):
        self.mfinder = MoveFinder()

    def run(self, board: Board) -> str:
        # setup things before game begins
        player_1 = Colors.WHITE
        player_2 = Colors.BLACK

        turn = 0
        flag_run = True

        while flag_run:
            all_valid_moves = self.mfinder.find_all_moves()
            turn += 1
            turn_player = player_1 if turn % 2 != 0 else player_2

            print(f"({turn}) {turn_player}'s Turn")
            board.printb()

            # get player input

            break


### DOWN HERE IS LOGIC FOR CALCULATING MOVES


@dataclass
class Vector:
    x: int
    y: int


# 8 directions
v_u = Vector(0, -1)
v_d = Vector(0, 1)
v_r = Vector(1, 0)
v_l = Vector(-1, 0)

v_ur = Vector(1, -1)
v_dr = Vector(1, 1)
v_ul = Vector(-1, -1)
v_dl = Vector(-1, 1)

# knight jumps
#  letter after j has length |2|
v_jur = Vector(-2, 1)
v_jul = Vector(-2, -1)
v_jru = Vector(-1, 2)
v_jrd = Vector(1, 2)
v_jdr = Vector(2, 1)
v_jdl = Vector(2, -1)
v_jlu = Vector(-1, -2)
v_jld = Vector(1, -2)


base_vectors = {
    # Moves are in (x, y)
    # ["Pawn"][0] is for white and [1] is for black
    "Pawn": ((v_u, v_ur, v_ul), (v_d, v_dr, v_dl)),
    "Rook": (v_r, v_l, v_u, v_d),
    "Bishop": (v_ur, v_dr, v_ul, v_dl),
    "Queen": (v_r, v_l, v_u, v_d, v_ur, v_dr, v_ul, v_dl),
    "King": (v_r, v_l, v_u, v_d, v_ur, v_dr, v_ul, v_dl),
    "Knight": (v_jur, v_jul, v_jru, v_jrd, v_jdr, v_jdl, v_jlu, v_jld),
}


class MoveFinder:
    def __init__(self):
        pass

    def find_all_valid_moves(self, b: Board):
        """This function does not find moves just bundles every move_finding_ function"""
        for square in b:
            if square.occ is None:
                continue

            if square.occ == "Pawn":
                pass
            elif square.occ == "King":
                pass
            elif square.occ == "Knight":
                pass
            else:  # Queen, Rook, Bishop use same logic
                pass

    def fm_pawn(self, b: Board, x, y):
        """rules for how a Pawn can move:
        -can only move forward 1 square
        -can move 2 if not moved before (as first move)
        -can move diagionally to capture if enemy in place
        -En Passant rule ~
        """
        pass

    def fm_pawn_capture(self, b: Board, x, y):
        pass

    def fm_pawn_en_passant(self, b: Board, x, y):
        pass

    def fm_king(self, b: Board, x, y):
        pass

    def fm_knight(self, b: Board, x, y):
        pass

    def fm_qbr(self, b: Board, x, y):
        pass

    def is_in_bounds(self, nx, ny):
        return nx > 7 or ny > 7 or nx < 0 or ny < 0
