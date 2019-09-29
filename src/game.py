import numpy as np

from src.interfaces.game_state import GameState, Piece
from src.config import Config


class Game:
    instance = None

    def __init__(self):
        self.game_state = GameState()
        self.game_state.reset()
        self.game_state.set_cards()

        self.agent_blue = Config.agent_blue_method
        self.agent_red = Config.agent_red_method

    def update(self):
        # If agent is human, then human will act on its own through ui to change current_player
        if self.game_state.current_player == Piece.BLUE:
            if self.agent_blue is not "human":
                pass
        if self.game_state.current_player == Piece.RED:
            if self.agent_red is not "human":
                pass
