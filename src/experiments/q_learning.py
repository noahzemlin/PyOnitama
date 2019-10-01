import json

from src.agents.qlearningagent import QLearningAgent
from src.agents.random import RandomAgent
from src.experiments.base_experiment import BaseExperiment
from src.interfaces.game_state import GameState, Piece


class QLearningExperiment(BaseExperiment):
    def __init__(self):
        super().__init__()

        # Eventually move to using the same agent for both, but difficult to get last action
        self.q_agent = QLearningAgent()

        self.blue_agent = RandomAgent()
        self.red_agent = self.q_agent

        self.do_render = False

        self.num_games = 0
        self.game_history = []

    def game_ended(self, game_state: GameState):
        self.num_games += 1
        self.game_history.append(game_state.winner)

        if self.num_games < 500:
            last_100_games = self.game_history[-100:]
            if self.num_games % 100 == 0:
                print(round(last_100_games.count(Piece.BLUE) / len(last_100_games) * 100) / 100)

            # swap positions to learn both sides
            temp = self.blue_agent
            self.blue_agent = self.red_agent
            self.red_agent = temp

            return True
        else:
            # Store agent's Q into file
            with open("knowledge.txt", 'w') as f:
                json.dump(self.q_agent.Q, f)
            return False
