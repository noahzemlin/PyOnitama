import time

from src.agents.random import RandomAgent
from src.experiments.base_experiment import BaseExperiment
from src.interfaces.game_state import GameState, Piece


class RandomAgentsExperiment(BaseExperiment):
    def __init__(self):
        super().__init__()

        self.blue_agent = RandomAgent()
        self.red_agent = RandomAgent()

        self.do_render = False

        self.num_games = 0
        self.blue_won = 0

        self.time_started = time.time()

    def game_ended(self, game_state: GameState):
        self.num_games += 1
        self.blue_won += 1 if game_state.winner == Piece.BLUE else 0

        if self.num_games == 1000:
            print(f'Blue side win-rate: {self.blue_won / self.num_games}')
            print(f'This experiment took {time.time() - self.time_started} seconds')
            return False
        else:
            return True
