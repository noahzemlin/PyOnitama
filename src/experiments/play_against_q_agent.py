import time

from src.agents.base_agent import BaseAgent
from src.agents.qlearningagent import QLearningAgent
from src.agents.qlearningagent_but_pass import QLearningAgent_But_Pass
from src.agents.qlearningagent_withdecay import QLearningAgentWithDecay
from src.agents.random import RandomAgent
from src.experiments.base_experiment import BaseExperiment
from src.interfaces.game_state import GameState


class PlayAgainstQExperiment(BaseExperiment):
    def __init__(self):
        super().__init__()

        self.q_agent = QLearningAgentWithDecay()
        self.q_agent.read_from_file('q_decay_3.brain')
        self.q_agent.alpha = 0
        self.q_agent.base_epsilon = 0
        self.q_agent.epsilon = 0
        self.q_agent.epsilon_floor = 0

        self.red_agent = QLearningAgent_But_Pass()
        self.red_agent.read_from_file('q_decay_3.brain')
        self.blue_agent = self.q_agent

        self.do_render = True
        self.q_wins = 0
        self.games = 0

    def game_ended(self, game_state: GameState):
        return True
