import json

from src.agents.tdlearningagent import TDLearningAgent
from src.agents.tdlearningagentRED import TDLearningAgentRED
from src.agents.random import RandomAgent
from src.agents.heuristic_agent import HeuristicAgent
from src.experiments.base_experiment import BaseExperiment
from src.interfaces.game_state import GameState, Piece

class TDLearningExperiment(BaseExperiment):
    def __init__(self):
        super().__init__()
        self.td_agent = TDLearningAgent()
        self.td_agent_red = TDLearningAgentRED()
        self.td_agent.V=self.td_agent_red.V
        self.rand_agent=RandomAgent()
        self.h_agent=HeuristicAgent()

        self.blue_agent = self.td_agent
        self.red_agent = self.td_agent_red

        self.do_render = False

        self.num_games = 0

        self.realGamesWon=0
        self.reallyPlaying=False
    def game_ended(self, game_state: GameState):
        self.td_agent.new_game()
        self.td_agent_red.new_game()
        if self.reallyPlaying:
            if game_state.winner == Piece.BLUE:
                self.realGamesWon += 1
        self.num_games += 1
        if self.num_games % 10000 == 0:  # every 10000 games, record
            with open("knowledgeTDSelfPlay.txt", 'w') as f:
                json.dump(self.td_agent.V, f)
            print("Dumped at game "+str(self.num_games))
        while True:
            if self.num_games % 3000 == 0 and self.num_games != 0:
                self.red_agent=self.h_agent
                self.td_agent.epsilon=0
                self.reallyPlaying=True
            if self.num_games % 3000 == 300 and self.num_games != 300:
                self.red_agent=self.td_agent_red
                self.td_agent.epsilon=0.10
                self.reallyPlaying=False
                f = open("resultsTDSelfPlay", "a")
                f.write(str(self.num_games-100)+", "+str(self.realGamesWon)+"\n")
                print("GamesPlayed: "+str(100.0*(0.0+self.num_games)/300)+", Win %: "+str(self.realGamesWon))
                self.realGamesWon=0

            #print("game complete\n")
            return True
        return False
