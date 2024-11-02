from .components.board import Board
from .components.pieces import Piece, PieceType


class Logic:
    """this class bundles logic and other rules stuff"""

    def __init__(self, board: Board):
        self.board = board

    def find_moves(self, piece: Piece, x: int, y: int):
        vectors = piece.my_vectors
        color = piece.color

        valid_moves = []
        # TODO

    def is_move_valid(self, v, x, y, color):

        nx, ny = x + v[0], y + v[1]  # vector + old position = new position
        if self.is_out_of_bounds(nx, ny):
            return False

        square = self.board.array2D[ny][nx]

        if square.occupant == None:
            return True

        elif square.occupant.color == color:
            return False

        elif square.occupant.color != color:
            return True

    def is_out_of_bounds(self, x, y):
        return x < 0 or x >= self.board.SIZE or y < 0 or y >= self.board.SIZE
