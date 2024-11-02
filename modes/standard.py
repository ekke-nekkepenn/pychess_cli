from pathlib import Path
from .base_class import GameMode

from ..input_handler import InputHandler
from ..components.player import Player
from ..components.colors import Colors
from ..components.board import Board
from ..components.pieces import Piece


class Standard(GameMode):
    def __init__(self):
        input_handler = InputHandler()

    def setup(self, board: Board):
        white = Player(Colors.WHITE, "Vendrik")
        black = Player(Colors.BLACK, "Gwyn")

        fp = Path().absolute() / "pychess_cli" / "layouts" / "layout_standard.csv"

        layout = self.get_layout(fp)
        board.load_layout(layout)
        self.run(board, white, black)

    def run(self, board: Board, white: Player, black: Player):
        print(f"{white.name} VS {black.name}")

        turn = 0
        running = True
        # MAIN GAME LOOP
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
