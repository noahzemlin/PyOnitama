import json

from src.agents.tdlamlearningagent import TDLambdaLearningAgent
from src.agents.random import RandomAgent
from src.experiments.base_experiment import BaseExperiment
from src.interfaces.game_state import GameState, Piece

class TDLambdaLearningExperiment(BaseExperiment):
    def __init__(self):
        super().__init__()
        self.td_agent = TDLambdaLearningAgent()
        self.rand_agent=RandomAgent()

        self.blue_agent = self.td_agent
        self.red_agent = self.rand_agent

        self.do_render = False

        self.num_games = 0

        self.realGamesWon=0
        self.reallyPlaying=False
    def game_ended(self, game_state: GameState):
        self.td_agent.e={}
        self.td_agent.statesThisGame=[]
        if self.reallyPlaying:
            if game_state.winner == Piece.BLUE:
                self.realGamesWon += 1
        self.num_games += 1
        if self.num_games % 10000 == 0:  # every 10000 games, record
            with open("knowledgeLam.txt", 'w') as f:
                json.dump(self.td_agent.V, f)
            print("Dumped at game "+str(self.num_games))
        while True:
            if self.num_games % 5000 == 0:
                self.td_agent.epsilon=0
                self.reallyPlaying=True
            if self.num_games % 5000 == 100:
                self.td_agent.epsilon=0.15
                self.reallyPlaying=False
                f = open("resultsLam", "a")
                f.write(str(self.num_games-100)+", "+str(self.realGamesWon)+"\n")
                print("GamesPlayed: "+str(self.num_games)+", Win %: "+str(self.realGamesWon))
                self.realGamesWon=0

            #print("game complete\n")
            return True
        return False
