import json

from src.agents.tdlamlearningagent import TDLambdaLearningAgent
from src.agents.tdlamlearningagentRED import TDLambdaLearningAgentRed
from src.agents.random import RandomAgent
from src.agents.heuristic_agent import HeuristicAgent
from src.experiments.base_experiment import BaseExperiment
from src.interfaces.game_state import GameState, Piece

class TDLambdaVsTDLambdaLearningExperiment(BaseExperiment):
    def __init__(self):
        super().__init__()
        self.tdLam_agent_Blue = TDLambdaLearningAgent()
        self.tdLam_agent_Red = TDLambdaLearningAgentRed()
        self.tdLam_agent_Red.V=self.tdLam_agent_Blue.V
        self.rand_agent=RandomAgent()
        self.h_agent=HeuristicAgent()

        self.blue_agent = self.tdLam_agent_Blue
        self.red_agent = self.tdLam_agent_Red

        self.do_render = False

        self.num_games = 0

        self.realGamesWon=0
        self.reallyPlaying=False
    def game_ended(self, game_state: GameState):
        #Things that need to be reset
        self.tdLam_agent_Blue.reset_game()
        self.tdLam_agent_Red.reset_game()

        if self.reallyPlaying:
            if game_state.winner == Piece.BLUE:
                self.realGamesWon += 1
        self.num_games += 1
        if self.num_games % 10000 == 0:  # every 10000 games, record
            with open("knowledgeLamLamGood.txt", 'w') as f:
                json.dump(self.tdLam_agent_Blue.V, f)
            print("Dumped at game "+str(self.num_games))
        while True:
            if self.num_games % 5000 == 0 and self.num_games != 0:
                self.red_agent=self.h_agent
                self.tdLam_agent_Blue.epsilon=0
                self.reallyPlaying=True
                self.tdLam_agent_Blue.moveDepth=2
            if self.num_games % 5000 == 100 and self.num_games != 100:
                self.red_agent=self.tdLam_agent_Red
                self.tdLam_agent_Blue.epsilon=0.10
                self.reallyPlaying=False
                self.tdLam_agent_Blue.moveDepth=0
                f = open("resultsLamLamGood", "a")
                # f.write(str(self.num_games-100)+", "+str(self.realGamesWon)+"\n")
                # print("GamesPlayed: "+str(self.num_games)+", Win %: "+str(self.realGamesWon))
                f.write(str(self.num_games-100)+", "+str(self.realGamesWon)+", "+str(len(self.tdLam_agent_Blue.V))+"\n")
                print("GamesPlayed: "+str(self.num_games)+", Win %: "+str(self.realGamesWon)+", len(V) = "+str(len(self.tdLam_agent_Blue.V)))
                self.realGamesWon=0

            #print("game complete\n")
            return True
        return False
