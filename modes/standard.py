from ..input_handler import InputHandler
from ..components.player import Player
from ..components.colors import Colors
from ..components.board import Board
from ..components.pieces import Piece


class Standard:
    def __init__(self):
        input_handler = InputHandler()

    def run(self, board: Board):
        white = Player(Colors.WHITE, "Vendrik")
        black = Player(Colors.BLACK, "Gwyn")

        self.game_loop(board, white, black)

    def game_loop(self, board: Board, white: Player, black: Player):
        print(f"{white.name} VS {black.name}")

        turn = 0
        running = True
        while running:
            turn += 1
            current_player = self.set_current_player(turn, white, black)
            board.printb()
            return

    def set_current_player(self, turn, white, black):
        if turn % 2 != 0:
            return white
        else:
            return black
