from pathlib import Path

from player import Player
from board import Board
from colors import Colors
from pieces import Piece, PieceType
from vectors import Vector


class Game:
    def __init__(self, p1: Player, p2: Player, board: Board):
        self.p1 = p1
        self.p2 = p2
        self.board = board
        self.mfinder = MoveFinder(self.board)
        self.layout_handler = LayoutHandler()

    def run(self):
        # setup things before game begins

        player_white = self.p1
        player_black = self.p2

        turn_counter = 0

        flag_run = True
        while flag_run:
            # (Upkeep Step) Things to do before a Player Turn Starts
            # all_valid_moves = self.mfinder.find_all_moves(self.board)
            all_valid_moves = {}
            # self.debug_to_files(all_valid_moves)

            turn_counter += 1
            turn_player = player_white if turn_counter % 2 != 0 else player_black

            # print(f"{turn_player}'s Turn ({turn_counter})")
            # self.board.printb()

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

    def load_layout(self):
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

    def layout_to_string(self, board: Board) -> str:
        layout_string = ""
        for rank in board.grid:
            for square in rank:
                if square.occ is None:
                    pass

                else:
                    if square.occ.color == Colors.WHITE:
                        layout_string += "w"
                    elif square.occ.color == Colors.BLACK:
                        layout_string += "b"

                    if square.occ.type == PieceType.PAWN:
                        layout_string += "P"
                    elif square.occ.type == PieceType.ROOK:
                        layout_string += "R"
                    elif square.occ.type == PieceType.KNIGHT:
                        layout_string += "N"
                    elif square.occ.type == PieceType.BISHOP:
                        layout_string += "B"
                    elif square.occ.type == PieceType.QUEEN:
                        layout_string += "Q"
                    elif square.occ.type == PieceType.KING:
                        layout_string += "K"

                layout_string += ","

            # remove last comma in a line with a newline
            layout_string = layout_string[:-1] + "\n"
        return layout_string

    def layout_to_file(self, board: Board, fp: Path):
        layout_string = self.layout_to_string(board)
        with open(fp, "w") as f:
            f.write(layout_string)


# Shared Vectors
v_U = Vector(0, -1)
v_D = Vector(0, 1)
v_R = Vector(1, 0)
v_L = Vector(-1, 0)

v_UR = Vector(1, -1)
v_DR = Vector(1, 1)
v_UL = Vector(-1, -1)
v_DL = Vector(-1, 1)


def get_base_vectors(piece: Piece) -> tuple[Vector]:
    base_vectors = {
        PieceType.PAWN: (
            v_D,
            v_DR,
            v_DL,
        ),  # need to multiply each by -1 for other direction
        PieceType.ROOK: (v_D, v_U, v_R, v_L),
        PieceType.KNIGHT: (
            Vector(2, 1),
            Vector(2, -1),
            Vector(-2, 1),
            Vector(-2, -1),
            Vector(1, 2),
            Vector(1, -2),
            Vector(-1, 2),
            Vector(-1, -2),
        ),
        PieceType.BISHOP: (v_DR, v_DL, v_UR, v_UL),
        PieceType.QUEEN: (v_D, v_U, v_R, v_L, v_DR, v_DL, v_UR, v_UL),
        PieceType.KING: (v_D, v_U, v_R, v_L, v_DR, v_DL, v_UR, v_UL),
    }
    bvs = base_vectors[piece.type]
    if piece.type is PieceType.PAWN:
        direction = 1 if piece.color == Colors.BLACK else -1
        if direction == -1:
            bvs = tuple([v * direction for v in bvs])
    return bvs


class Node:
    def __init__(self, position: Vector, next_node: "Node | None" = None):
        self.position = position
        self.adjacent_nodes = []


class MoveFinder:
    def __init__(self, board: Board):
        self.board = board
        self.root_nodes = {}  # k: Piece, v: Node

    def create_root_nodes(self):
        self.root_nodes = {}
        for y, line in enumerate(self.board.grid):
            for x, square in enumerate(line):
                if square.occ is None:
                    continue

                self.root_nodes.setdefault(square.occ, Node(Vector(x, y)))

    def find_adjacent_nodes(self, piece: Piece):
        root_node = self.root_nodes[piece]
        base_vectors = get_base_vectors(piece)
