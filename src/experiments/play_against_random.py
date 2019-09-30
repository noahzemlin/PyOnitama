from src.agents.base_agent import BaseAgent
from src.agents.random import RandomAgent
from src.experiments.base_experiment import BaseExperiment
from src.interfaces.game_state import GameState, Piece
import time


class PlayAgainstRandomExperiment(BaseExperiment):
    def __init__(self):
        super().__init__()

        self.blue_agent = BaseAgent()
        self.red_agent = RandomAgent()

        self.do_render = True

    def game_ended(self, game_state: GameState):
        time.sleep(2)
        return True
