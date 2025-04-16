from dataclasses import dataclass
from email.mime import base
from board import Board
from colors import Colors
from pieces import Piece, PieceType
from dataclasses import dataclass

# keys are coordinates on board and valuesa are a list of vectors
# moves get recalculated after each turn


@dataclass
class Vector:
    x: int
    y: int

    def __mul__(self, m):
        return Vector(self.x * m, self.y * m)


class Game:
    def __init__(self):
        self.mfinder = MoveFinder()

    def run(self, board: Board):
        # setup things before game begins
        player_1 = Colors.WHITE
        player_2 = Colors.BLACK

        turn = 0
        flag_run = True

        while flag_run:
            all_valid_moves = self.mfinder.find_all_moves(board)
            turn += 1
            turn_player = player_1 if turn % 2 != 0 else player_2

            print(f"({turn}) {turn_player}'s Turn")
            board.printb()

            # get player input

            break


# base vectors
v_U = Vector(0, -1)
v_D = Vector(0, 1)
v_R = Vector(1, 0)
v_L = Vector(-1, 0)

v_UR = Vector(-1, 1)
v_DR = Vector(1, 1)
v_UL = Vector(-1, -1)
v_DL = Vector(1, -1)

# knight jumps
# the letter after j has always |2| as value
# e.g v_jDR -> D is 2
v_jUR = Vector(-2, 1)
v_jUL = Vector(-2, -1)
v_jRU = Vector(-1, 2)
v_jRD = Vector(1, 2)
v_jDR = Vector(2, 1)
v_jDL = Vector(2, -1)
v_jLU = Vector(-1, -2)
v_jLD = Vector(1, -2)


base_vectors = {
    # Moves are in (x, y)
    # ["Pawn"][0] is for white and [1] is for black
    "Pawn": ((v_U, v_UR, v_UL), (v_D, v_DR, v_DL)),
    "Rook": (v_R, v_L, v_U, v_D),
    "Bishop": (v_UR, v_DR, v_UL, v_DL),
    "Queen": (v_U, v_D, v_R, v_L, v_UR, v_DR, v_UL, v_DL),
    "King": (v_U, v_D, v_R, v_L, v_UR, v_DR, v_UL, v_DL),
    "Knight": (v_jUR, v_jUL, v_jRU, v_jRD, v_jDR, v_jDL, v_jLU, v_jLD),
}


class MoveFinder:
    def __init__(self):
        # key[Piece]: value[list]
        self.all_valid_moves = {}

    def find_all_moves(self, b: Board):
        """This function does not find moves just bundles every move_finding_ function"""

        self.all_valid_moves = {}
        for y, row in enumerate(b.field):
            for x, square in enumerate(row):
                if square.occ is None:
                    continue

                piece = square.occ
                bvs = base_vectors[piece.type]

                if piece.type == PieceType.PAWN:
                    pass
                elif piece.type == PieceType.KING:
                    pass
                elif piece.type == PieceType.KNIGHT:
                    pass
                else:  # Queen, Rook, Bishop use same logic
                    self.fm_qbr(b, piece, x, y, bvs)

        return self.all_valid_moves

    def fm_pawn(self, b: Board, x, y, bv):
        """rules for how a Pawn can move:
        -can only move forward 1 square
        -can move 2 if not moved before (as first move)
        -can move diagionally to capture if enemy in place
        -En Passant rule ~
        """
        pass

    def fm_pawn_capture(self, b: Board, p, x, y, bvs):
        pass

    def fm_pawn_en_passant(self, b: Board, p, x, y, bvs):
        pass

    def fm_king(self, b: Board, p, x, y, bvs):
        pass

    def fm_knight(self, b: Board, p, x, y, bvs):
        pass

    def fm_qbr(self, b: Board, p, x, y, bvs):
        self.all_valid_moves.setdefault(p, [])
        # iter over base vectors
        for bv in bvs:
            i = 1
            while True:
                # scale base vector
                v = bv * i  # check dataclass Vector.__mul__()
                # get the new position and check if valid
                nx = x + v.x
                ny = y + v.y

                if not self.is_in_bounds(nx, ny):
                    break

                item = b.get_item(nx, ny)

                if item is None:
                    self.all_valid_moves[p].append(v)

                elif item.color == p.color:
                    break

                else:
                    self.all_valid_moves[p].append(v)
                    break

                i += 1
            print()

    def is_in_bounds(self, nx, ny):
        return 0 <= nx <= 7 and 0 <= ny <= 7
