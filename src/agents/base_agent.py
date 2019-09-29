from src.interfaces.game_state import GameState


class BaseAgent:
    def __init__(self):
        pass

    def move(self, game: GameState, player):
        pass
