import json
import struct

from src.agents.qlearningagent import QLearningAgent
from src.agents.random import RandomAgent
from src.experiments.base_experiment import BaseExperiment
from src.interfaces.game_state import GameState, Piece


class QLearningExperiment(BaseExperiment):
    def __init__(self):
        super().__init__()

        # Eventually move to using the same agent for both, but difficult to get last action
        self.q_agent = QLearningAgent("qlearned.brain")

        self.blue_agent = self.q_agent
        self.red_agent = self.q_agent

        self.do_render = False

        self.num_games = 0

    def game_ended(self, game_state: GameState):
        self.num_games += 1

        if self.num_games < 10000:
            if self.num_games % 2000 == 0:  # every 10000 games, record and reset agents
                print(f'{self.num_games / 10000.0 * 100.0}% done!')
                with open("qlearned.brain", 'wb') as f:
                    for key in self.q_agent.Q:
                        f.write(int(key).to_bytes(16, "big"))
                        f.write(struct.pack('f', self.q_agent.Q[key]))

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
