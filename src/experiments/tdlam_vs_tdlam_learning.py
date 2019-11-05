import json
import time

from src.agents.tdlamlearningagent import TDLambdaLearningAgent
from src.agents.tdlamlearningagentRED import TDLambdaLearningAgentRed
from src.agents.random import RandomAgent
from src.agents.heuristic_agent import HeuristicAgent
from src.experiments.base_experiment import BaseExperiment
from src.interfaces.game_state import GameState, Piece

class TDLambdaVsTDLambdaLearningExperiment(BaseExperiment):
    def __init__(self):
        super().__init__()
        self.lastReport=time.time()
        self.nowReport=-1
        self.tdLam_agent_Blue = TDLambdaLearningAgent()
        self.tdLam_agent_Red = TDLambdaLearningAgentRed()
        self.tdLam_agent_Red.V=self.tdLam_agent_Blue.V
        self.rand_agent=RandomAgent()
        self.h_agent=HeuristicAgent()

        self.blue_agent = self.tdLam_agent_Blue
        self.tdLam_agent_Blue.moveDepth=0
        self.red_agent = self.tdLam_agent_Red
        self.tdLam_agent_Red.moveDepth=0

        self.do_render = False

        self.num_games = 0

        self.realGamesWon=0
        self.reallyPlaying=False
    def game_ended(self, game_state: GameState):
        #print("game end: "+str(self.num_games))
        #Things that need to be reset
        self.tdLam_agent_Blue.reset_game()
        self.tdLam_agent_Red.reset_game()

        if self.reallyPlaying:
            if game_state.winner == Piece.BLUE:
                self.realGamesWon += 1
        self.num_games += 1
        if self.num_games % 10000 == 0:  # every 10000 games, record
            with open("knowledgeLamSelfPlay2NoReward.txt", 'w') as f:
                json.dump(self.tdLam_agent_Blue.V, f)
            print("Dumped at game "+str(self.num_games))
        while True:
            if self.num_games % 3000 == 0 and self.num_games != 0:
                self.red_agent=self.h_agent
                self.tdLam_agent_Blue.epsilon=0
                self.reallyPlaying=True
                self.tdLam_agent_Blue.moveDepth=2
            if self.num_games % 3000 == 300 and self.num_games != 300:
                self.nowReport = time.time()
                self.red_agent=self.tdLam_agent_Red
                self.tdLam_agent_Blue.epsilon=0.10
                self.reallyPlaying=False
                self.tdLam_agent_Blue.moveDepth=0
                f = open("resultsLamSelfPlay2NoReward", "a")
                # f.write(str(self.num_games-100)+", "+str(self.realGamesWon)+"\n")
                # print("GamesPlayed: "+str(self.num_games)+", Win %: "+str(self.realGamesWon))
                f.write(str(self.num_games-100)+", "+str(self.realGamesWon)+", "+str(len(self.tdLam_agent_Blue.V))+", "+str(int(self.nowReport)-int(self.lastReport))+"\n")
                print("GamesPlayed: "+str(self.num_games)+", Lap Time: "+str(int(self.nowReport)-int(self.lastReport))+", Win %: "+str((0.0+self.realGamesWon)/300*100)+", len(V) = "+str(len(self.tdLam_agent_Blue.V)))
                self.realGamesWon=0
                self.lastReport=self.nowReport

            #print("game complete\n")
            return True
        return False
