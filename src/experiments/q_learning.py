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
        self.stored_epsilon = self.q_agent.epsilon
        self.stored_alpha = self.q_agent.alpha
        self.random_agent = RandomAgent()

        self.blue_agent = self.q_agent
        self.red_agent = self.q_agent

        self.do_render = False

        self.num_games = 0
        self.wins = 0

    def game_ended(self, game_state: GameState):
        self.num_games += 1

        if self.num_games < 200000:
            if self.num_games % 2500 == 2000:  # every 10000 games, record and reset agents
                print(f'{self.num_games / 200000.0 * 100.0}% done!')
                with open("knowledge.txt", 'w') as f:
                    json.dump(self.q_agent.Q, f)

                # perform exhibitionism

                self.blue_agent = self.random_agent
                self.red_agent = self.q_agent
                self.q_agent.epsilon = 0
                self.q_agent.alpha = 0
                self.wins = 0
            elif self.num_games % 2500 > 2000 and self.num_games % 2500 != 2499:  # exhibition matches
                if game_state.winner == self.q_agent.last_played:
                    self.wins += 1
                temp = self.blue_agent
                self.blue_agent = self.red_agent
                self.red_agent = temp
            elif self.num_games % 2500 == 2499:  # exhibition done
                print(f'wins {self.wins / 500}')
                self.q_agent.epsilon = self.stored_epsilon
                self.q_agent.alpha = self.stored_alpha
                self.blue_agent = self.q_agent
                self.red_agent = self.q_agent
            return True
        else:
            # Store agent's Q into file
            with open("knowledge.txt", 'w') as f:
                json.dump(self.q_agent.Q, f)
            return False
