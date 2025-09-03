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
        p_white = self.p1
        p_black = self.p2
        turn_counter = 0
        running = True
        move_history = []

        while running:
            # find possible moves for turn
            self.mfinder.create_nodes()

            turn_player = p_white if turn_counter % 2 != 0 else p_black
            print(f"{turn_player}'s Turn")
            self.board.printb()

            print("Select your Piece")
            self.debug_to_files(self.mfinder.root_nodes)
            break
            pos = self.player_selects_piece(turn_player)

    def player_selects_piece(self, player, flag=True):
        while True:
            pos = self.convert_chess_nota_to_vector(self.player_selects_square())

            selected_piece = self.board.get_item(pos)
            if selected_piece is None:
                print("You selected nothing. You get nothing! Good day SIR!")
                continue

            if flag and selected_piece.color == player:
                print("Please select your own piece.")
                return pos
            if not flag and selected_piece.color != player:
                print("Please select an opponent's piece.")
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

    def convert_chess_nota_to_vector(self, nota):
        # TODO error handling
        y = 8 - int(nota[1])
        x = ord(nota[0].lower()) - ord("a")
        return Vector(x, y)

    def convert_vector_to_chess_nota(self, position: Vector):
        # TODO error handling
        file = str(8 - position.y)
        rank = str(int(ord("a") + position.x))
        return f"{file}{rank}"

    def debug_to_files(self, all_moves, fp="valid_moves.txt"):
        with open(fp, "w") as f:
            for piece, root_nodes in all_moves.items():
                f.write(f"{piece}\n")
                root_nodes.print_nodes(fp=f)
                print("\n", file=f)


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
                    print("applying layout failed!")
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

class MoveHistory:
    def __init__(self):
        self.mh = []

    def add_move(self, )

#TODO if nothing else uses this function except Node just make it a method
def get_base_vectors(piece: Piece) -> tuple[Vector]:
    """This function just handles the case for a pawn whose vectors depend on its colors"""
    # Shared Vectors
    v_U = Vector(0, -1)
    v_D = Vector(0, 1)
    v_R = Vector(1, 0)
    v_L = Vector(-1, 0)

    v_UR = Vector(1, -1)
    v_DR = Vector(1, 1)
    v_UL = Vector(-1, -1)
    v_DL = Vector(-1, 1)

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
            bvs = tuple([v.scale(direction) for v in bvs])
    return bvs


class Node:
    def __init__(self, position: Vector):
        self.position = position
        # only the root node has multiple adjacent nodes.
        # child nodes have 0 ajd nodes or 1
        self.adjacent_nodes = []

    def add_node(self, node: "Node"):
        self.adjacent_nodes.append(node)

    def print_nodes(self, level=0, fp=None):
        print(f"{"\t"*level}{self.position}, level: {level}", file=fp)
        for n in self.adjacent_nodes:
            n.print_nodes(level=(level + 1), fp=fp)


class MoveFinder:
    def __init__(self, board: Board):
        self.board = board
        self.root_nodes = {}  # k: Piece, v: Node

    def is_in_bounds(self, pos: Vector) -> bool:
        return 0 <= pos.x <= 7 and 0 <= pos.y <= 7

    def create_nodes(self):
        self.root_nodes = {}
        for y, line in enumerate(self.board.grid):
            for x, square in enumerate(line):
                if square.occ is None:
                    continue

                self.root_nodes.setdefault(square.occ, Node(Vector(x, y)))
                self.find_pseudo_legal_adjacent_nodes(square.occ)

    def find_pseudo_legal_adjacent_nodes(self, piece: Piece):
        base_vectors = get_base_vectors(piece)

        if piece.type in (PieceType.QUEEN, PieceType.BISHOP, PieceType.ROOK):
            self.find_adjacent_nodes_QBR(piece, base_vectors)
        elif piece.type == PieceType.KING:
            self.find_adjacent_nodes_KING(piece, base_vectors)
        elif piece.type == PieceType.KNIGHT:
            self.find_adjacent_nodes_KNIGHT(piece, base_vectors)
        elif piece.type == PieceType.PAWN:
            self.find_adjacent_nodes_PAWN(piece, base_vectors)
        else:
            print(piece)
            raise ValueError

    def find_adjacent_nodes_KING(self, piece: Piece, base_vectors: tuple[Vector]):
        root_node = self.root_nodes[piece]
        for bv in base_vectors:
            new_pos = root_node.position + bv
            if self.is_in_bounds(new_pos):
                root_node.add_node(Node(new_pos))

        # add castling nodes
        if piece.unmoved:
            root_node.add_node(Node(root_node.position - Vector(2, 0)))
            root_node.add_node(Node(root_node.position + Vector(2, 0)))

    def find_adjacent_nodes_QBR(self, piece: Piece, base_vectors: tuple[Vector]):
        root_node = self.root_nodes[piece]
        for bv in base_vectors:
            current_node = root_node
            new_pos = current_node.position + bv
            while self.is_in_bounds(new_pos):
                adj_node = Node(new_pos)
                current_node.add_node(adj_node)
                current_node = adj_node
                new_pos = current_node.position + bv

    def find_adjacent_nodes_KNIGHT(self, piece: Piece, base_vectors: tuple[Vector]):
        """this function does not find castling for the king"""
        root_node = self.root_nodes[piece]

        for bv in base_vectors:
            new_pos = root_node.position + bv
            if self.is_in_bounds(new_pos):
                root_node.add_node(Node(new_pos))

    def find_adjacent_nodes_PAWN(self, piece: Piece, base_vectors: tuple[Vector]):
        """Pawn has some shenanigans. First vector in base_vector is its normal move vector. 
        The next two are capture vectors"""
        root_node = self.root_nodes[piece]
        move_vector = base_vectors[0]
        capture_vectors = base_vectors[1:]

        # cursed code but i like it lol
        current_node = root_node
        for s in range(1, piece.unmoved + 2):
            new_pos = current_node.position + move_vector
            if self.is_in_bounds(new_pos):
                adj_node = Node(new_pos)
                current_node.add_node(adj_node)
                current_node = adj_node

        for cv in capture_vectors:
            new_pos = root_node.position + cv
            if self.is_in_bounds(new_pos):
                root_node.add_node(Node(new_pos))
