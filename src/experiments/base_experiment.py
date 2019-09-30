from src.agents.base_agent import BaseAgent
from src.interfaces.game_state import GameState


class BaseExperiment():
    def __init__(self):
        self.blue_agent: BaseAgent = BaseAgent()
        self.red_agent: BaseAgent = BaseAgent()

        self.do_render = True

    # Return True to play another game, False to end
    def game_ended(self, game_state: GameState):
        return True
