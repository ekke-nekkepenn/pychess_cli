from components import Player, Piece, PieceType, Board, Square


class Game:
    def __init__(self, board):
        self.board = board

    def run(self):

        while True:
            print("(1) Standard\n(2) Puzzle\n(0) Exit")
            ipt = "1"

            match ipt:
                case "1":
                    results = Standard().setup(self.board)
                case "2":
                    # puzzle mode
                    raise NotImplementedError
                case "0":
                    input("Exiting now. Press any key to continue.")
                    return
                case _:
                    print("thats not an option")
                    continue


class GameMode:
    def get_layout(self, fp):
        """loads a layout from a file and turns strings into Piece|None."""
        color_map = {"b": Colors.BLACK, "w": Colors.WHITE}
        piece_map = {
            "P": PieceType.PAWN,
            "R": PieceType.ROOK,
            "N": PieceType.KNIGHT,
            "B": PieceType.BISHOP,
            "Q": PieceType.QUEEN,
            "K": PieceType.KING,
        }

        with open(fp) as file:
            layout = []
            for line in file.read().split():
                line = line.split(",")

                # convert strings to Piece|None
                for i, item in enumerate(line):
                    if not item:
                        item = None
                        continue
                    type = piece_map[item[1]]
                    color = color_map[item[0]]
                    line[i] = Piece(type, color)

                layout.append(tuple(line))
        return tuple(layout)


class Standard:
    def __init__(self, board: Board):
        self.board = board
        input_handler = InputHandler()
        logic = Logic()

    def run(self):
        white = Player(Colors.WHITE, "Vendrik")
        black = Player(Colors.BLACK, "Gwyn")

        self.game_loop(white, black)

    def game_loop(self, white: Player, black: Player):
        print(f"{white.name} VS {black.name}")

        turn = 0
        running = True
        while running:

            turn += 1
            current_player = self.set_current_player(turn, white, black)
            self.board.printb()
            # TODO implement input_handler. Check for valid input

            return

    def set_current_player(self, turn: int, white: Player, black: Player):
        if turn % 2 != 0:
            return white
        else:
            return black

    # def reset_move_lists(self):
    #     positions_and_pieces = self.board.where_is_all()
    #     for (_, _), piece in positions_and_pieces:
    #         piece.del_moves()

    # def find_all_valid_moves(self):
    #     positions_and_pieces = self.board.where_is_all()
    #     for (x, y), piece in positions_and_pieces:
    #         if piece.type == "Pawn":
    #             self.find_valid_moves_pawn(x, y, piece)
    #         else:
    #             self.find_valid_moves(x, y, piece)

    # def find_valid_moves(self, x, y, piece: Piece):
    #     for vec in piece.get_base_vectors():
    #         scal = 0
    #         while True:
    #             scal += 1
    #             nx, ny = x + (vec[0] * scal), y + (vec[1] * scal)
    #             if is_point_oob(nx, ny):
    #                 break

    #             if (piece2 := self.board[(nx, ny)]) is None:
    #                 piece.add_move(vec)

    #             elif piece != piece2:
    #                 piece.add_move(vec)
    #                 break

    #             elif piece == piece2:
    #                 break

    #             if piece.type in ("Knight", "King"):
    #                 break

    # def find_valid_moves_pawn(self, x, y, piece: Piece):
    #     d = piece.get_pawn_d()
    #     move_vec = piece.get_base_vectors()[0]  # (0, 1)
    #     for i in range(1, 3):
    #         # x stays the same because move_vec[0] = 0
    #         vy = move_vec[1] * d * i
    #         ny = y + vy
    #         if self.board[(x, ny)] is None:
    #             piece.add_move((0, vy))

    #         else:
    #             break

    #         if piece.status_moved:
    #             break

    # def find_valid_moves_pawn_atk(self, x, y, piece: Piece):
    #     d = piece.get_pawn_d()
    #     atk_vectors = piece.get_base_vectors()[1:]
    #     for vec in atk_vectors:
    #         nx, ny = x + (vec[0] * d), y + (vec[1] * d)
    #         if is_point_oob(nx, ny):
    #             continue

    #         if (piece2 := self.board[(nx, ny)]) is None:
    #             continue

    #         elif piece != piece2:
    #             piece.add_move(vec)

    # def select_point(self, message="IMPLEMENT MESSAGES") -> Point:
    #     while True:
    #         ipt = input(message)
    #         if s := contains_chess_coord(ipt):
    #             return parse_chess_notation(s)
    #         print("Try again.")

    # def set_current_player(self, turn):
    #     if turn % 2 == 0:
    #         return self.player1
    #     return self.player2

    # def debug_print_pieces_moves(self):
    #     positions_and_pieces = self.board.where_is_all()

    #     for pos, piece in positions_and_pieces:
    #         print(f"{pos}; {piece}; {piece.moves_valid}")


class Logic:
    """this class bundles logic and other rules stuff"""

    def __init__(self, board: Board):
        self.board = board

    def find_moves_RBQ(self, piece: Piece, x: int, y: int):
        """this finds valid moves for Rook, Bishop or Queen"""
        valid_moves = []
        for v in piece.my_vectors:

            s = 1
            while True:
                new_vx, new_vy = s * v[0], s * v[1]  # we scale vector
                nx, ny = x + new_vx, y + new_vy

                # first check if empty. WHy? because we want to acces square.occupant.color
                # else it crashes
                # then we want to check if piece.color == occupant.color

                if self.is_out_of_bounds(nx, ny):
                    break

                square = self.board.array2D[ny][nx]

                if square.occupant == None:
                    valid_moves.append((new_vx, new_vy))
                    # inc s

                elif square.occupant.color != piece.color:
                    valid_moves.append((new_vx, new_vy))
                    break

                elif square.occupan.color == piece.color:
                    break

                s += 1

        return valid_moves

    def find_moves_NK(self, piece: Piece, x: int, y: int):
        """finds valid moves for Knight & King"""
        valid_moves = []
        for v in piece.vectors:
            nx, ny = x + v[0], y + v[1]

            if self.is_out_of_bounds(nx, ny):
                continue

            square = self.board.array2D[ny][nx]

            if square.occupant == None:
                valid_moves.append(v)

            elif square.occupant.color != piece.color:
                valid_moves.append(v)

            elif square.occupant.color == piece.color:
                continue

        return valid_moves()

    def is_new_position_valid(self, nx, ny, color):
        # nx, ny = x + v[0], y + v[1]
        if self.is_out_of_bounds(nx, ny):
            return False

        square = self.board.array2D[ny][nx]

        if square.occupant == None:
            return True

        elif square.occupant.color != color:
            return True

        elif square.occupant.color == color:
            return False

    def is_out_of_bounds(self, x, y):
        return x < 0 or x >= self.board.SIZE or y < 0 or y >= self.board.SIZE
