import time

from src.agents.base_agent import BaseAgent
from src.agents.qlearningagent import QLearningAgent
from src.agents.random import RandomAgent
from src.experiments.base_experiment import BaseExperiment
from src.interfaces.game_state import GameState


class PlayAgainstQExperiment(BaseExperiment):
    def __init__(self):
        super().__init__()

        self.q_agent = QLearningAgent("qlearned.brain")
        self.q_agent.epsilon = 0
        self.q_agent.alpha = 0.2

        self.blue_agent = self.q_agent
        self.red_agent = BaseAgent()

        self.do_render = True
        self.q_wins = 0
        self.games = 0

    def game_ended(self, game_state: GameState):
        self.games += 1

        if game_state.winner == self.q_agent.last_played:
            self.q_wins += 1

        if self.games % 100 == 0:
            print(f'win-rate: {self.q_wins / self.games}')

        temp = self.blue_agent
        self.blue_agent = self.red_agent
        self.red_agent = temp

        return True
