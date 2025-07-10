from pathlib import Path

from player import Player
from board import Board
from colors import Colors
from pieces import Piece, PieceType
from vectors import Vector


class Game:
    def __init__(self, p1: Player, p2: Player, style):
        self.p1 = p1
        self.p2 = p2
        self.board = Board(style)
        self.mfinder = MoveFinder()
        self.layout_handler = LayoutHandler()

    def run(self):
        # setup things before game begins

        player_1 = self.p1
        player_2 = self.p2

        turn_counter = 0

        """ move_history stores each move per turn. Moves are in this format [(x, y), (nx, ny), "Captured Piece?"]. 
        Old position to new position + captured piece if even"""
        move_history = []
        captured_pieces = {}  # k: turn, v: Piece

        flag_run = True
        while flag_run:
            # (Upkeep Step) Things to do before a Player Turn Starts
            all_valid_moves = self.mfinder.find_all_moves(self.board)
            # self.debug_to_files(all_valid_moves)

            turn_counter += 1
            turn_player = player_1 if turn_counter % 2 != 0 else player_2

            print(f"{turn_player}'s Turn ({turn_counter})")
            self.board.printb()

            # get player input
            while True:
                pos_og = self.player_selects_piece(turn_player, self.board, True)
                piece = self.board.get_item(pos_og)

                piece_moves = all_valid_moves[piece]
                # original position + each vector -> new position
                valid_coord = [(pos_og + v) for v in piece_moves]

                self.board.printb(valid_coord)

                pos_new = self.convert_chess_nota_to_position(
                    self.player_selects_square()
                )

                if (pos_og - pos_new) in piece_moves:
                    """found a valid move"""
                    break
                else:
                    print(
                        f"Invalid move by {piece}. Cannot move from {pos_og} to {pos_new}\n\t{piece_moves}"
                    )

            self.board.move(pos_og, pos_new)

            print(valid_coord)
            self.board.printb(valid_coord)

            nota_new = self.player_selects_square()
            pos_new = self.convert_chess_nota_to_position(nota_new)

    # TODO refactor this bs. Just remake it ew
    def player_selects_piece(self, player, board: Board, flag=True):
        while True:
            # select player piece
            pos = self.convert_chess_nota_to_position(self.player_selects_square())

            selected_piece = board.get_item(pos)
            if selected_piece is None:
                print("You selected nothing. You get nothing! Good day SIR!")
                continue

            # for selecting own piece
            if flag and selected_piece.color == player:
                return pos
            # for selecting enemy piece
            if not flag and selected_piece.color != player:
                return pos

    def player_selects_square(self) -> str:
        while True:
            ipt = input(": ")
            if len(ipt) != 2:
                print("use this format: [a-h][1-8], for example: d4, h8, a7, etc.")
                continue

            if ipt[0].lower() < "a" or ipt[0].lower() > "h":
                continue

            if ipt[1] < "1" or ipt[1] > "8":
                continue

            break
        return ipt

    ## SAFE
    def convert_chess_nota_to_position(self, nota):
        # TODO error handling
        y = 8 - int(nota[1])
        x = ord(nota[0].lower()) - ord("a")
        return Vector(x, y)

    def convert_position_to_chess_nota(self, position: Vector):
        # TODO error handling
        file = str(8 - position.y)
        rank = str(int(ord("a") + position.x))
        return f"{file}{rank}"

    def debug_to_files(self, all_moves):
        with open("valid_moves.txt", "w") as f:
            for k, v in all_moves.items():
                f.write(f"{k}\n")
                for i in v:
                    f.write(f"\t{i}\n")

    ## SAFE


## SAFE
class LayoutHandler:
    """A layout is defined as just a 8x8 2D array containing certain strings as elements
    e.g 'wP', 'bR', '',  -> white pawn, black rood, empty space
    """

    def __init__(self):
        self.paths = [
            "layout_standard.csv",
            "layout_testing.csv",
            "test2.csv",
            "test_exposed.csv",
            "test_exposed_2.csv",
        ]
        self.path_to_layout = Path(".") / "layouts" / self.paths[0]
        self.layout = []

    def reset_layout(self):
        self.layout = []

    def get_layout(self):
        with open(self.path_to_layout, "r") as f:
            # split at newlines
            for line in f.read().split():
                # split at ','
                self.layout.append(tuple(line.split(",")))

    def apply_layout(self, board: Board):
        for y, line in enumerate(self.layout):
            for x, piece in enumerate(line):
                # skip empty string -> ""
                if not piece:
                    continue

                ptype = None
                pcolor = None
                # Get color and type e.g "bP" -> "Black" "Pawn"
                pcolor = Colors.WHITE if piece[0].lower() == "w" else Colors.BLACK

                # iter over Enum and check if first letter match
                for type in PieceType:
                    if type != "Knight":
                        if piece[1].lower() == type[0].lower():
                            ptype = type
                            break
                    # except Knight which uses 'N' as identifier
                    else:
                        ptype = type

                if not pcolor or not ptype:
                    # TODO error handling
                    raise ValueError

                board.set_item(Vector(x, y), Piece(pcolor, ptype))


## SAFE


# base vectors
#     Vector(x, y)
v_U = Vector(0, -1)
v_D = Vector(0, 1)
v_R = Vector(1, 0)
v_L = Vector(-1, 0)

v_UR = Vector(1, -1)
v_DR = Vector(1, 1)
v_UL = Vector(-1, -1)
v_DL = Vector(-1, 1)

# knight jumps
# the letter after j represents 2/-2
v_jUR = Vector(-2, 1)
v_jUL = Vector(-2, -1)
v_jRU = Vector(-1, 2)
v_jRD = Vector(1, 2)
v_jDR = Vector(2, 1)
v_jDL = Vector(2, -1)
v_jLU = Vector(-1, -2)
v_jLD = Vector(1, -2)


base_vectors = {
    #! PAWN's base_vectors * -1, if .color == Color.WHITE
    "Pawn": (v_U, v_UR, v_UL),
    "Rook": (v_R, v_L, v_U, v_D),
    "Bishop": (v_UR, v_DR, v_UL, v_DL),
    "Queen": (v_U, v_D, v_R, v_L, v_UR, v_DR, v_UL, v_DL),
    "King": (v_U, v_D, v_R, v_L, v_UR, v_DR, v_UL, v_DL),
    "Knight": (v_jUR, v_jUL, v_jRU, v_jRD, v_jDR, v_jDL, v_jLU, v_jLD),
}


# TODO!! Refactor all of this ?
# This whole class kinda works but checking if the king is exposed
# for a Vector seems really challenging and repetitve
class MoveFinder:
    def __init__(self):
        # key[Piece]: value[list[Vector...]]
        self.all_valid_moves = {}

    def find_all_moves(self, b: Board):
        """This function does not find moves just bundles every move_finding function"""

        # empty out all_valid_moves for a fresh turn
        self.all_valid_moves = {}
        return {}

        for y, row in enumerate(b.grid):
            for x, square in enumerate(row):
                piece = square.occ
                if piece is None:
                    continue

                # cannot use dataclasses with same fields because for "hashability" they use the fields
                # so 2 dataclass instances with exact same fields are treated as the same key
                # they are though not the same in memory
                pos = Vector(x, y)
                bvs = base_vectors[piece.type]
                self.all_valid_moves.setdefault(piece, [])

                if piece.type == PieceType.PAWN:
                    self.fm_pawn(b, piece, pos, bvs)
                    self.fm_pawn_capture(b, piece, pos, bvs)
                elif piece.type in (PieceType.KING, PieceType.KNIGHT):
                    self.fm_king_knight(b, piece, pos, bvs)
                else:
                    self.fm_qbr(b, piece, pos, bvs)

        return self.all_valid_moves

    def fm_pawn(self, b: Board, p, pos: Vector, bvs):
        """rules for how a Pawn can move:
        -can only move forward 1 square
        -can move 2 if not moved before (as first move)
        -can move diagionally to capture if enemy in place
        -En Passant rule ~
        """
        bv = bvs[0][0] if p.color == Colors.WHITE else bvs[1][0]

        for i in range(1, (2 if p.status_moved else 3)):
            # bv: Vector
            v: Vector = bv.scale(i)
            new_pos = pos + v

            if not self.is_in_bounds(new_pos):
                break

            if b.get_item(new_pos) is None:
                if self.is_king_exposed(b, p, pos, new_pos):
                    break
                # append VALID move
                self.all_valid_moves[p].append(v)

            else:
                break

    def fm_pawn_capture(self, b: Board, p: Piece, pos: Vector, bvs):
        cap_v = bvs[0][1:] if p.color == Colors.WHITE else bvs[1][1:]

        for v in cap_v:
            new_pos = pos + v

            if not self.is_in_bounds(new_pos):
                continue

            item = b.get_item(new_pos)

            if item is None or item.color == p.color:
                continue

            else:
                if self.is_king_exposed(b, p, pos, new_pos):
                    continue

                self.all_valid_moves[p].append(v)

    def fm_pawn_en_passant(self, b: Board, p: Piece, pos: Vector, new_pos: Vector, bvs):
        """need to establish MOVE HISTORY and inspect the last move in it. If a pawn moved 2 sqrs from start pos then we en passant that bitch"""
        raise NotImplementedError

    def fm_king_knight(self, b: Board, p: Piece, pos: Vector, bvs):
        for bv in bvs:
            new_pos = pos + bv

            if not self.is_in_bounds(new_pos):
                continue

            item = b.get_item(new_pos)

            if item is None or item.color != p.color:
                if self.is_king_exposed(b, p, pos, new_pos):
                    continue
                self.all_valid_moves[p].append(bv)

    def fm_qbr(self, b: Board, p: Piece, pos: Vector, bvs):
        # iter over base vectors
        for bv in bvs:
            i = 0
            while True:
                i += 1
                # scale base vector
                v = bv.scale(i)
                # get the new position and check if valid
                new_pos = pos * v

                if not self.is_in_bounds(new_pos):
                    break

                item = b.get_item(new_pos)

                if item is None:
                    if self.is_king_exposed(b, p, pos, new_pos):
                        break
                    self.all_valid_moves[p].append(v)

                elif item.color == p.color:
                    break

                else:
                    self.all_valid_moves[p].append(v)
                    break

    def is_in_bounds(self, pos: Vector):
        return 0 <= pos.x <= 7 and 0 <= pos.y <= 7

    def is_king_exposed(self, b: Board, p: Piece, pos: Vector, new_pos: Vector):
        # move piece to check if king gets exposed, reverted at end
        possible_piece = b.move(pos, new_pos)

        king_pos = None

        if p.type is PieceType.KING:
            # if p is KING remember its position
            king_pos = pos

        else:
            # find the pos of King of p.color
            for y, row in enumerate(b.grid):
                for x, square in enumerate(row):
                    if square.occ is None:
                        continue
                    if (
                        square.occ.type == PieceType.KING
                        and square.occ.color == p.color
                    ):
                        king_pos = Vector(x, y)
                        break
                # if KING is NOT found keep going next rank
                else:
                    continue
                # because KING was found a 'break' was called so also break here
                break

        if not king_pos:
            raise ValueError

        qbvs = base_vectors[PieceType.QUEEN]
        nbvs = base_vectors[PieceType.KNIGHT]

        for bv in nbvs:
            test_pos = king_pos + bv

            if not self.is_in_bounds(test_pos):
                continue

            test_piece = b.get_item(test_pos)
            if test_piece is None:
                continue

            # enemy knight is at that point
            if test_piece.color != p.color and test_piece.type == PieceType.KNIGHT:
                b.move(new_pos, pos)
                b.set_item(new_pos, possible_piece)

                return True

        for bv in qbvs:
            i = 0
            while True:
                i += 1
                v = bv.scale(i)
                test_pos = king_pos + v

                if not self.is_in_bounds(test_pos):
                    break

                test_piece = b.get_item(test_pos)

                if test_piece is None:
                    continue

                if test_piece.color == p.color:
                    break

                # TODO???? Huh? what is this
                if test_piece.type == PieceType.PAWN:
                    if i > 1:
                        pass
                    else:
                        c = 0 if test_piece.color == Colors.WHITE else 1
                        if (bv * -1) in base_vectors[test_piece.type][c][1:]:
                            b.move(new_pos, pos)
                            b.set_item(new_pos, possible_piece)
                            return True

                else:
                    if test_piece.type == PieceType.KING and i > 1:
                        pass
                    elif bv in base_vectors[test_piece.type]:
                        b.move(new_pos, pos)
                        b.set_item(new_pos, possible_piece)
                        return True

        b.move(new_pos, pos)
        b.set_item(new_pos, possible_piece)
        return False
