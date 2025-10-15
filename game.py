from pathlib import Path
from enum import Enum, auto

from player import Player
from board import Board
from colors import Colors
from vectors import Vector
from pieces import Piece, PieceType, ALL_BASE_VECTORS


class State(Enum):
    UPKEEP = auto()
    SELECT_PIECE = auto()
    SELECT_DEST = auto()
    END_PHASE = auto()
    SURRENDER = auto()
    GAME_END = auto()


class Game:
    def __init__(self, p_white: Player, p_black: Player, board: Board):
        self.p_white = p_white
        self.p_black = p_black
        self.board = board
        self.mfinder = MoveFinder(self.board)
        self.layout_handler = LayoutHandler()

    def run(self):
        # setup vars before game begins
        turn_player = self.p_white
        turn_counter = 1
        running = True
        move_history = []
        game_state = State.UPKEEP

        selected_piece = None
        pos_og = None
        pos_new = None
        try_vector = None

        ## GAME LOOP
        while running:
            # -----------------------------------------------------------------------
            if State.UPKEEP == game_state:

                turn_player = self.p_white if turn_counter % 2 != 0 else self.p_black

                game_state = State.SELECT_PIECE

            # -----------------------------------------------------------------------
            elif State.SELECT_PIECE == game_state:
                ipt = self.player_input()

                if ipt == "x":
                    print("cannot cancel action")
                    continue

                if ipt == "s":
                    game_state = State.SURRENDER
                    continue

                pos_og = self.chess_nota_to_vector(ipt)
                selected_piece = self.board.get_item(pos_og)
                if selected_piece is None or selected_piece.color != turn_player.color:
                    print("Please select a square occupied by your piece")
                    continue

                game_state = State.SELECT_DEST

            # -----------------------------------------------------------------------
            elif State.SELECT_DEST == game_state:
                ipt = self.player_input()

                if ipt == "x":
                    game_state = State.SELECT_PIECE
                    continue

                if ipt == "s":
                    game_state = State.SURRENDER
                    continue

                pos_new = self.chess_nota_to_vector(ipt)
                try_vector = pos_new - pos_og
                dest_piece = self.board.get_item(pos_new)

                game_state = State.END_PHASE

            # -----------------------------------------------------------------------
            elif State.END_PHASE == game_state:
                turn_counter += 1
                game_state = State.UPKEEP

            # -----------------------------------------------------------------------
            elif State.SURRENDER == game_state:
                print(f"\nplayer {turn_player} surrendered!")
                game_state = State.GAME_END

            # -----------------------------------------------------------------------
            elif State.GAME_END == game_state:
                #running = False
                return

    def player_input(self) -> str:
        while True:
            ipt = input(": ").lower()
            ipt = ipt.strip()
            # cancel action or surrender
            if ipt in ("x", "s"):
                return ipt.lower()

            if (
                len(ipt) == 2
                and ipt[0] >= "a"
                and ipt[0] <= "h"
                and ipt[1] >= "1"
                and ipt[1] <= "8"
            ):
                return ipt
            print(self.help_message())

    def help_message(self) -> str:
        return "select a square with [a-h][1-8], e.g. b7, d3, A4\n'x' to cancel action\n's' to surrender"

    def chess_nota_to_vector(self, nota: str) -> Vector:
        y = 8 - int(nota[1])
        x = ord(nota[0].lower()) - ord("a")
        return Vector(x, y)

    def vector_to_chess_nota(self, pos: Vector) -> str:
        file = str(8 - pos.y)
        rank = str(int(ord("a") + pos.x))
        return f"{file}{rank}"

    def debug_to_file(self, all_moves, fp="valid_moves.txt"):
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


def get_base_vectors(piece: Piece):
    bvs = ALL_BASE_VECTORS[piece.type]
    if piece.type is PieceType.PAWN:
        direction = 1 if piece.color == Colors.BLACK else -1
        if direction == -1:
            bvs = tuple([v.scale(direction) for v in bvs])
    return bvs


class Node:
    def __init__(self, pos: Vector):
        self.pos = pos
        # only the root node has multiple adjacent nodes.
        # child nodes have 0-1 adj_nodes
        self.adjacent_nodes = []

    def add_node(self, node: "Node"):
        self.adjacent_nodes.append(node)

    def __str__(self):
        return f"({self.pos.x}, {self.pos.y})"


class MoveFinder:
    def __init__(self, board: Board):
        self.board = board
        self.move_graphs = {} 
        self.king_black = None
        self.king_white = None

    def is_in_bounds(self, pos: Vector) -> bool:
        return 0 <= pos.x <= 7 and 0 <= pos.y <= 7


    def create_move_graphs(self):
        for y, line in enumerate(self.board.grid):
            for x, square in enumerate(line):
                if square.occ is None:
                    continue

                if square.occ.type == PieceType.KING:
                    if square.occ.color == Colors.BLACK:
                        self.king_black = square.occ
                    else:
                        self.king_white = square.occ

                root_node = Vector(x, y)
                self.move_graphs.setdefault(
                    square.occ, {root_node: []}
                )

                self.find_adjacent_nodes(square.occ, root_node)




    def find_adjacent_nodes(self, p: Piece, root: Vector):
        bvs = get_base_vectors(p)
        graph = self.move_graphs[p]

        if p.type in (PieceType.QUEEN, PieceType.BISHOP, PieceType.ROOK):
            self.find_adj_nodes_QBR(graph, root, bvs)
        if p.type in (PieceType.KING, PieceType.KNIGHT):
            self.find_adj_nodes_KN(p, graph, root, bvs)
        if p.type == PieceType.PAWN:
            self.find_adj_nodes_P(p, graph, root, bvs)


    def find_adj_nodes_QBR(self, graph, root: Vector, base_vectors):
        for bv in base_vectors:
            current_pos = root 
            new_pos = current_pos + bv
            while self.is_in_bounds(new_pos):
                # found existing Node
                graph.setdefault(new_pos, [])
                # add to adj list
                graph[current_pos].append(new_pos)
                current_pos = new_pos
                new_pos = current_pos + bv

    def find_adj_nodes_KN(self, p: Piece, graph, root: Vector, base_vectors):
        for bv in base_vectors:
            new_pos = root + bv
            if self.is_in_bounds(new_pos):
                # found existing Node
                graph.setdefault(new_pos, [])
                # add to adj list 
                graph[root].append(new_pos)

        # add_castling
        if p.type == PieceType.KING and p.unmoved:
            castle_right = root + Vector(2, 0)
            graph.setdefault(castle_right, [])
            graph[root].append(castle_right)

            castle_left = root - Vector(2, 0)
            graph.setdefault(castle_left, [])
            graph[root].append(castle_left)




    def find_adj_nodes_P(self,p: Piece, graph, root: Vector, base_vectors):
        # capture vectors
        for bv in base_vectors[:1]:
            new_pos = root + bv
            if self.is_in_bounds(new_pos):
                # found existing Node
                graph.setdefault(new_pos, [])
                # add to adj list 
                graph[root].append(new_pos)

        # move vector
        for i in range(1, p.unmoved + 2):
            new_pos = root + base_vectors[0].scale(i)
            if self.is_in_bounds(new_pos):
                # found existing Node
                graph.setdefault(new_pos, [])
                # add to adj list 
                graph[root].append(new_pos)




