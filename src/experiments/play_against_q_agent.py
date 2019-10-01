import time

from src.agents.base_agent import BaseAgent
from src.agents.qlearningagent import QLearningAgent
from src.agents.random import RandomAgent
from src.experiments.base_experiment import BaseExperiment
from src.interfaces.game_state import GameState


class PlayAgainstQExperiment(BaseExperiment):
    def __init__(self):
        super().__init__()

        self.blue_agent = QLearningAgent("knowledge2_red.txt")
        self.blue_agent.epsilon = 0
        self.red_agent = BaseAgent()

        self.do_render = True

    def game_ended(self, game_state: GameState):
        return True
