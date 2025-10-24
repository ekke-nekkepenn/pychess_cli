from encodings.punycode import T
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
            self.board.printb()
            print()
            # -----------------------------------------------------------------------
            if State.UPKEEP == game_state:
                self.mfinder.create_move_graphs()

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
                    print("Please select a square with your piece on it")
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

                # TODO!!!!!!!!!!!!!!!!!!!!!!!
                ## PUT IN FUNCTION
                graph = self.mfinder.move_graphs[selected_piece]
                print(f"BEFORE: {graph}")
                self.mfinder.foo_graph_blah_QBR(graph, pos_og, selected_piece)
                print(f"AFTER: {graph}")

                if self.mfinder.is_node_in(graph, pos_og, pos_new):
                    print("Move is valid.")
                ## PUT IN FUNCTION

                else:
                    break

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


class LayoutHandler:
    def __init__(self):
        self.paths_names = [
            "layout_standard.csv",
            "layout_testing.csv",
            "test2.csv",
            "test_exposed.csv",
            "test_exposed_2.csv",
        ]
        self.path_to_layout = Path(".") / "layouts" / self.paths_names[0]
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

                # TODO idk why i added this clause?
                if not pcolor or not ptype:
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


class MoveFinder:
    def __init__(self, board: Board):
        self.board = board
        self.move_graphs = {}

    def is_in_bounds(self, pos: Vector) -> bool:
        return 0 <= pos.x <= 7 and 0 <= pos.y <= 7

    # GRAPH CREATION BLOCK -----------------------------------------------------------
    def create_move_graphs(self):
        # creates graphs with moves that are valid on an empty board
        for y, line in enumerate(self.board.grid):
            for x, square in enumerate(line):
                piece = square.occ
                if piece is None:
                    continue

                root = Vector(x, y)  # current pos of piece
                graph = {root: []}
                self.move_graphs.setdefault(piece, graph)
                bvs = get_base_vectors(piece)

                if piece.type in (PieceType.QUEEN, PieceType.BISHOP, PieceType.ROOK):
                    self.find_adj_nodes_QBR(graph, root, bvs)
                elif piece.type in (PieceType.KING, PieceType.KNIGHT):
                    self.find_adj_nodes_KN(piece, graph, root, bvs)
                elif piece.type == PieceType.PAWN:
                    self.find_adj_nodes_P(piece, graph, root, bvs)

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

    def find_adj_nodes_P(self, p: Piece, graph, root: Vector, base_vectors):
        # capture vectors
        for bv in base_vectors[1:]:
            new_pos = root + bv
            if self.is_in_bounds(new_pos):
                # found existing Node
                graph.setdefault(new_pos, [])
                # add to adj list
                graph[root].append(new_pos)

        for i in range(1, p.unmoved + 2):  # range 1 or 2
            new_pos = root + base_vectors[0].scale(i)
            if self.is_in_bounds(new_pos):
                # found existing Node
                graph.setdefault(new_pos, [])
                # add to adj list
                graph[root].append(new_pos)

    # GRAPH CREATION BLOCK -----------------------------------------------------------

    def is_node_in(self, graph, root: Vector, test_node: Vector) -> bool:
        queue = []
        visited = []
        visited.append(root)
        queue.append(root)

        while queue:
            node = queue.pop(0)
            # techinically this will always be False for the root
            if node == test_node:
                return True

            for adjN in graph[node]:
                if adjN not in visited:
                    visited.append(adjN)
                    queue.append(adjN)

        return False

    # FILTER OUT POS THAT ARE BLOCKED
    def foo_graph_blah_QBR(self, graph, root: Vector, piece: Piece):
        queue = []
        visited = []
        visited.append(root)
        queue.append(root)
        prior_node = root

        while queue:
            node = queue.pop(0)
            new_piece = self.board.get_item(node)

            if new_piece is None:
                pass

            elif new_piece.color != piece.color:
                graph[node] = []

            elif new_piece.color == piece.color:
                if node == root:
                    pass
                else:
                    graph[prior_node].remove(node)
                    graph.pop(node)
                    continue

            for adjN in graph[node]:
                if adjN not in visited:
                    visited.append(adjN)
                    queue.append(adjN)

            prior_node = node
