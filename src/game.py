import numpy as np

from src.agents.base_agent import BaseAgent
from src.agents.random import RandomAgent
from src.interfaces.game_state import GameState, Piece
from src.config import Config

AGENTS = {
    "human": BaseAgent,
    "random": RandomAgent
}


class Game:
    instance = None

    def __init__(self):
        self.game_state = GameState()
        self.game_state.reset()

        self.agent_blue = AGENTS[Config.agent_blue_method]()
        self.agent_red = AGENTS[Config.agent_red_method]()

        self.new_game = True

        self.playing = True

    def update(self):

        if not self.playing:
            return

        # If fresh start, tell agents
        if self.game_state.turn_num == 0 and self.new_game:
            self.agent_blue.game_start(self.game_state, Piece.BLUE)
            self.agent_red.game_start(self.game_state, Piece.RED)
            self.new_game = False

        # If agent is human, then human will act on its own through ui to change current_player
        if self.game_state.winner == Piece.NONE and self.game_state.current_player == Piece.BLUE:
            self.agent_blue.move(self.game_state)
        if self.game_state.winner == Piece.NONE and self.game_state.current_player == Piece.RED:
            self.agent_red.move(self.game_state)

        # If game ended, tell agents
        if self.game_state.winner != Piece.NONE:
            self.playing = self.agent_blue.game_end(self.game_state)
            self.playing = self.agent_red.game_end(self.game_state)
            self.game_state.reset()
            self.new_game = True
