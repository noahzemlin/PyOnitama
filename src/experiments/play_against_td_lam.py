import json

from src.agents.base_agent import BaseAgent
from src.agents.tdlamlearningagent import TDLambdaLearningAgent
from src.agents.random import RandomAgent
from src.experiments.base_experiment import BaseExperiment
from src.interfaces.game_state import GameState, Piece

class HumanTDLamExperiment(BaseExperiment):
    def __init__(self):
        super().__init__()
        print("Starting brain load. May take a bit.")
        self.td_agent = TDLambdaLearningAgent("knowledgeLamHeur.txt")
        print("Finished brain load.")
        self.td_agent.moveDepth=4
        self.blue_agent = self.td_agent
        self.red_agent = BaseAgent()
        self.td_agent.epsilon=0

        self.do_render = True

        self.num_games = 0

        self.realGamesWon=0
        self.reallyPlaying=False
    def game_ended(self, game_state: GameState):
        #Things that need to be reset
        self.td_agent.reset_game()

        if self.reallyPlaying:
            if game_state.winner == Piece.BLUE:
                self.realGamesWon += 1
        self.num_games += 1
        if self.num_games % 10000 == 0:  # every 10000 games, record
            # with open("Human.txt", 'w') as f:
            #     json.dump(self.td_agent.V, f)
            print("Dumped at game "+str(self.num_games))
        while True:
            if self.num_games % 5000 == 0:
                self.td_agent.epsilon=0
                self.reallyPlaying=True
                self.td_agent.moveDepth=10
            if self.num_games % 5000 == 100:
                self.td_agent.epsilon=0.15
                self.reallyPlaying=False
                self.td_agent.moveDepth=4
                # f = open("human", "a")
                # f.write(str(self.num_games-100)+", "+str(self.realGamesWon)+"\n")
                # print("GamesPlayed: "+str(self.num_games)+", Win %: "+str(self.realGamesWon))
                f.write(str(self.num_games-100)+", "+str(self.realGamesWon)+", "+str(len(self.td_agent.V))+"\n")
                print("GamesPlayed: "+str(self.num_games)+", Win %: "+str(self.realGamesWon)+", len(V) = "+str(len(self.td_agent.V)))
                self.realGamesWon=0

            #print("game complete\n")
            return True
        return False
