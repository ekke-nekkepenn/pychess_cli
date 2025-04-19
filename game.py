from dataclasses import dataclass
from email.mime import base
from hmac import new
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

        """ move_history stores each move per turn. Moves are in this format [(x, y), (nx, ny), "Captured Piece?"]. 
        Old position to new position + captured piece if even"""
        move_history = []
        captured_pieces = {}  # k: turn, v: Piece

        while flag_run:
            all_valid_moves = self.mfinder.find_all_moves(board)
            turn += 1
            turn_player = player_1 if turn % 2 != 0 else player_2

            print(f"{turn_player}'s Turn ({turn})")
            board.printb()
            # get player input
            origin = self.select_square()
            og_pos = self.convert_chess_nota_to_index(origin)

            dest = self.select_square()
            new_pos = self.convert_chess_nota_to_index(dest)

            break

    def select_square(self) -> str:
        while True:
            ipt = input(": ")
            if len(ipt) != 2:
                print("[a-h][1-8] e.g d4")
                continue

            if ipt[0].lower() < "a" or ipt[0].lower() > "h":
                continue

            if ipt[1] < "1" or ipt[1] > "8":
                continue

            break
        return ipt

    def convert_chess_nota_to_index(self, nota):
        # nota's first 2 chars HAVE TO be a LETTER and DIGIT
        y = 8 - int(nota[1])
        x = ord(nota[0].lower()) - ord("a")
        return x, y

    def convert_index_to_chess_nota(self, idx):
        # idx has 2 int each need to be btw 0-7
        d = str(8 - idx[0])
        c = int(ord("a") + idx[1])
        return c + d


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
# the letter after j is always |2|
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
    # "Pawn"[0] white and [1] black
    # "Pawn"[0][0] & [1][0] move vector
    # "Pawn"[0][1-2] & [1][1-2] capture vectors
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
                self.all_valid_moves.setdefault(piece, [])

                if piece.type == PieceType.PAWN:
                    pass
                elif piece.type == PieceType.KING or PieceType.KNIGHT:
                    self.fm_king_knight(b, piece, x, y, bvs)
                else:  # Queen, Rook, Bishop use same logic
                    self.fm_qbr(b, piece, x, y, bvs)

        return self.all_valid_moves

    def fm_pawn(self, b: Board, p, x, y, bvs):
        """rules for how a Pawn can move:
        -can only move forward 1 square
        -can move 2 if not moved before (as first move)
        -can move diagionally to capture if enemy in place
        -En Passant rule ~
        """
        bv = bvs[0][0] if p.color == Colors.WHITE else bvs[1][0]

        for i in range(1, (2 if p.status_moved else 3)):
            v = bv * i
            nx = x + v.x
            ny = y + v.y

            if not self.is_in_bounds(nx, ny):
                break

            if b.get_item(nx, ny) is None:
                if self.is_king_exposed():
                    break
                self.all_valid_moves[p].append()

            else:
                break

    def fm_pawn_capture(self, b: Board, p, x, y, bvs):
        bvs = bvs[0] if p.color == Colors.WHITE else bvs[1]

        for bv in bvs:
            nx = x + bv.x
            ny = y + bv.y

            if not self.is_in_bounds(nx, ny):
                continue

            item = b.get_item(nx, ny)

            if item is None or item.color == p.color:
                continue

            else:
                if self.is_king_exposed():
                    continue

                self.all_valid_moves[p].append(bv)

    def fm_pawn_en_passant(self, b: Board, p, x, y, bvs):
        """need to exstablish MOVE HISTORY and inspect the last move in it. If a pawn moved 2 sqrs from start pos then we en passant that bitch"""
        raise NotImplementedError

    def fm_king_knight(self, b: Board, p, x, y, bvs):
        for bv in bvs:
            nx = x + bv.x
            ny = y + bv.y

            if not self.is_in_bounds(nx, ny):
                continue

            item = b.get_item(nx, ny)

            if item is None or item.color != p.color:
                if self.is_king_exposed():
                    continue
                self.all_valid_moves[p].append(bv)

    def fm_qbr(self, b: Board, p, x, y, bvs):
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
                    if self.is_king_exposed():
                        break
                    self.all_valid_moves[p].append(v)

                elif item.color == p.color:
                    break

                else:
                    self.all_valid_moves[p].append(v)
                    break

                i += 1

    def is_in_bounds(self, nx, ny):
        return 0 <= nx <= 7 and 0 <= ny <= 7

    def is_king_exposed(self, b: Board, x, y, nx, ny):
        """Checking if king is exposed after moving a piece. Make the move, then from the position of the king use Queen bvs and Knight bvs outwards from the king and if you find an OPPS it means king is exposed THEN revert the move"""
        return False
