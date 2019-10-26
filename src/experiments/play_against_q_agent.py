import time

from src.agents.base_agent import BaseAgent
from src.agents.qlearningagent import QLearningAgent
from src.agents.random import RandomAgent
from src.experiments.base_experiment import BaseExperiment
from src.interfaces.game_state import GameState


class PlayAgainstQExperiment(BaseExperiment):
    def __init__(self):
        super().__init__()

        self.q_agent = QLearningAgent()
        self.q_agent.read_from_file('q.brain')
        self.q_agent.epsilon = 0
        self.q_agent.alpha = 0

        self.red_agent = self.q_agent
        self.blue_agent = BaseAgent()

        self.do_render = True
        self.q_wins = 0
        self.games = 0

    def game_ended(self, game_state: GameState):
        return True
