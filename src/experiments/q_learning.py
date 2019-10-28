import json

from src.agents.heuristic_agent import HeuristicAgent
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
        self.heur_agent = HeuristicAgent()

        self.blue_agent = self.q_agent
        self.red_agent = self.q_agent

        self.do_render = False

        self.trained_games = 0

        self.stage = 1
        self.stage_games = 0
        self.wins = 0

        # start with exhibition
        self.q_agent.alpha = 0
        self.q_agent.epsilon = 0
        self.blue_agent = self.q_agent
        self.red_agent = self.random_agent

        print(f'{self.trained_games},{len(self.q_agent.Q)},', end='')

    def game_ended(self, game_state: GameState):
        self.stage_games = self.stage_games + 1

        if self.stage == 1 or self.stage == 2:
            if game_state.winner == Piece.BLUE and self.blue_agent == self.q_agent:
                self.wins += 1
            if game_state.winner == Piece.RED and self.red_agent == self.q_agent:
                self.wins += 1

        if self.trained_games < 2000000 + 1:

            if self.stage == 0:  # training
                self.trained_games = self.trained_games + 1

                if self.stage_games == 5000:
                    self.q_agent.write_to_file('q.brain')
                    print(f'{self.trained_games},{len(self.q_agent.Q)},', end='')

                    self.stage_games = 0
                    self.stage = 1
                    self.q_agent.alpha = 0
                    self.q_agent.epsilon = 0
                    self.blue_agent = self.q_agent
                    self.red_agent = self.random_agent

            if self.stage == 1:  # random exhib
                temp = self.blue_agent
                self.blue_agent = self.red_agent
                self.red_agent = temp

                if self.stage_games == 250:
                    print(f'{self.wins / 250},', end='')
                    self.wins = 0
                    self.stage_games = 0
                    self.stage = 2
                    self.blue_agent = self.q_agent
                    self.red_agent = self.heur_agent

            if self.stage == 2:  # heur exhib
                temp = self.blue_agent
                self.blue_agent = self.red_agent
                self.red_agent = temp

                if self.stage_games == 250:
                    print(f'{self.wins / 250}')
                    self.wins = 0
                    self.stage_games = 0
                    self.stage = 0
                    self.blue_agent = self.q_agent
                    self.red_agent = self.q_agent
                    self.q_agent.alpha = self.stored_alpha
                    self.q_agent.epsilon = self.stored_epsilon

            return True
        else:
            # Store agent's Q into file
            self.q_agent.write_to_file('q.brain')
            return False
