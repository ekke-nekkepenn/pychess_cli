class Game:
    def __init__(self, board):
        self.board = board

    def run(self):
        return

    #     while running:
    #         self.reset_move_lists()
    #         self.find_all_valid_moves()
    #         self.debug_print_pieces_moves()
    #         # Turn Starts
    #         self.board.printb()

    #         # move selected piece

    #         # end step
    #         turn += 1
    #         current_player = self.set_current_player(turn)
    #         running = False

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
