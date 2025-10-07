from pathlib import Path
from enum import Enum

from player import Player
from board import Board
from colors import Colors
from vectors import Vector
from pieces import Piece, PieceType, ALL_BASE_VECTORS


class State(Enum):
    UPKEEP = 1
    SELECTION = 2
    VALIDATION = 3
    END_PHASE = 4



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
        game_state = State.UPKEEP

        ## GAME LOOP
        ##
        while running:

            # TODO fix this up
            if State.UPKEEP == game_state:
                self.mfinder.create_nodes()
                self.mfinder.filter_blocked_nodes()
                turn_player = p_white if turn_counter % 2 != 0 else p_black

                game_state = State.SELECTION

            if State.SELECTION == game_state:
                game_state = State.VALIDATION

            if State.VALIDATION == game_state:
                pass


            if State.END_PHASE == game_state:
                game_state = State.UPKEEP




            # UPKEEP STUFF
            self.mfinder.create_nodes()
            self.mfinder.filter_blocked_nodes()

            turn_player = p_white if turn_counter % 2 != 0 else p_black
            print(f"{turn_player}'s Turn")
            self.board.printb()


            print("Select your Piece:", end=" ")
            self.debug_to_files(self.mfinder.root_nodes)

            pos = self.player_selects_square()
            selected_piece = self.board.get_item(pos)
            if selected_piece is None or selected_piece.color != turn_player.color:



    

    def player_selects_square(self) -> Vector:
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
        return self.convert_chess_nota_to_vector(ipt)

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
                f.write(f"{piece.type}{piece.color}\n")
                root_nodes.print_nodes(fp=f)
                print("\n", file=f)

    def save_board_state(self):
        self.layout_handler.layout_to_file(self.board, Path("board_state.csv"))
        return self.layout_handler.layout_to_string


class LayoutHandler:
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
                # piece HERE is just a string like "wP", "bQ" or ""
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

                # instantiate Piece obj and set it on the board
                board.set_item(Vector(x, y), Piece(pcolor, ptype))

    def layout_to_string(self, board: Board) -> str:
        layout_string = ""
        for rank in board.grid:
            for square in rank:
                if square.occ is None:
                    pass
                else:
                    layout_string += (
                        f"{square.occ.get_color_symbol()}{square.occ.get_symbol()}"
                    )

                layout_string += ","

            # remove last ',' in a line with a newline
            layout_string = layout_string[:-1] + "\n"
        # get rid of last '\n' char
        layout_string = layout_string[:-1]
        return layout_string

    def layout_to_file(self, board: Board, fp: Path):
        layout_string = self.layout_to_string(board)
        with open(fp, "w") as f:
            f.write(layout_string)


class MoveHistory:
    def __init__(self):
        self.mh = []

    def add_move(self):
        raise NotImplementedError


# TODO if nothing else uses this function except Node just make it a method
def get_base_vectors(piece: Piece):
    """This function just handles the case for a pawn whose vectors depend on its colors"""
    bvs = ALL_BASE_VECTORS[piece.type]
    if piece.type is PieceType.PAWN:
        direction = 1 if piece.color == Colors.BLACK else -1
        if direction == -1:
            bvs = tuple([v.scale(direction) for v in bvs])
    return bvs


class Node:
    def __init__(self, pos: Vector, parent):
        self.pos = pos
        # only the root node has multiple adjacent nodes.
        # child nodes have 0-1 adj_nodes
        self.parent = parent
        self.adjacent_nodes = []

    def add_node(self, node: "Node"):
        self.adjacent_nodes.append(node)

    def print_nodes(self, level=0, fp=None):
        print(
            f"{"\t"*level}{self} parent {self.parent}",
            file=fp,
        )
        for n in self.adjacent_nodes:
            n.print_nodes(level=(level + 1), fp=fp)

    def __str__(self):
        return f"({self.pos.x}, {self.pos.y})"


class MoveFinder:
    def __init__(self, board: Board):
        self.board = board
        self.root_nodes = {}  # k: Piece, v:
        self.king_black = None
        self.king_white = None

    def is_in_bounds(self, pos: Vector) -> bool:
        return 0 <= pos.x <= 7 and 0 <= pos.y <= 7

    def create_nodes(self):
        # Whole Move finding starts here
        self.root_nodes = {}
        for y, line in enumerate(self.board.grid):
            for x, square in enumerate(line):
                if square.occ is None:
                    continue

                if square.occ.type == PieceType.KING:
                    if square.occ.color == Colors.BLACK:
                        self.king_black = square.occ
                    else:
                        self.king_white = square.occ

                self.root_nodes.setdefault(square.occ, Node(Vector(x, y), None))
                self.find_pseudo_moves(square.occ)

    # PSEUDO MOVE BLOCK
    def find_pseudo_moves(self, piece: Piece):
        base_vectors = get_base_vectors(piece)

        if piece.type in (PieceType.KING, PieceType.KNIGHT):
            self.add_pseudo_moves_KN(piece, base_vectors)
        if piece.type in (PieceType.QUEEN, PieceType.BISHOP, PieceType.ROOK):
            self.add_pseudo_moves_QBR(piece, base_vectors)
        if piece.type == PieceType.PAWN:
            self.add_pseudo_moves_P(piece, base_vectors)

    def add_pseudo_moves_KN(self, piece: Piece, base_vectors):
        root_node = self.root_nodes[piece]

        for bv in base_vectors:
            new_pos = root_node.pos + bv
            if self.is_in_bounds(new_pos):
                adj_node = Node(new_pos, root_node)
                root_node.add_node(adj_node)
                parent_node = adj_node

        # add castling nodes
        if piece.type == PieceType.KING and piece.unmoved:
            root_node.add_node(Node(root_node.pos - Vector(2, 0), root_node))

            root_node.add_node(Node(root_node.pos + Vector(2, 0), root_node))

    def add_pseudo_moves_QBR(self, piece: Piece, base_vectors):
        root_node = self.root_nodes[piece]
        for bv in base_vectors:
            new_pos = root_node.pos + bv
            current_node = root_node
            while self.is_in_bounds(new_pos):
                adj_node = Node(new_pos, current_node)
                current_node.add_node(adj_node)
                current_node = adj_node
                new_pos = current_node.pos + bv

    def add_pseudo_moves_P(self, piece: Piece, base_vectors):
        """Pawn has some shenanigans. First vector in base_vectors is its normal move vector.
        The next two are capture vectors"""
        root_node = self.root_nodes[piece]
        move_vector = base_vectors[0]
        capture_vectors = base_vectors[1:]

        # cursed code but i like it lol
        current_node = root_node
        for s in range(1, piece.unmoved + 2):
            new_pos = current_node.pos + move_vector
            if self.is_in_bounds(new_pos):
                adj_node = Node(new_pos, current_node)
                current_node.add_node(adj_node)
                current_node = adj_node

        for cv in capture_vectors:
            new_pos = root_node.pos + cv
            if self.is_in_bounds(new_pos):
                root_node.add_node(Node(new_pos, root_node))

    # PSEUDO MOVE BLOCK END

    # COLLISION BLOCK
    def filter_blocked_nodes(self):
        for piece, root_node in self.root_nodes.items():
            # collision type 1

            if piece.type == PieceType.KING:
                pass

            if piece.type in (
                PieceType.QUEEN,
                PieceType.BISHOP,
                PieceType.ROOK,
            ):
                pass
                # self.filter_collision_type1(root_node, piece)

            # collision type 2
            if piece.type == PieceType.KNIGHT:
                self.filter_collision_type2(root_node, piece)
            # collision type 31
            if piece.type == PieceType.PAWN:
                pass

    # TODO finish the filter
    def filter_collision_type1(self, node, piece):
        for n in node.adjacent_nodes:
            p = self.board.get_item(n.pos)
            if p is None or p.color != piece.color:
                # call func rec
                self.filter_collision_type1(n, piece)
            else:
                node.adjacent_nodes.remove(n)

    def filter_collision_type2(self, node, piece):
        for n in node.adjacent_nodes:
            p = self.board.get_item(n.pos)
            if p is None or p.color != piece.color:
                pass
            else:
                node.adjacent_nodes.remove(n)

    # COLLISION BLOCK END
