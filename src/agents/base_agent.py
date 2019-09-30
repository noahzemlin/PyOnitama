from src.interfaces.game_state import GameState, Piece


class BaseAgent:
    def __init__(self):
        pass

    def move(self, game: GameState):
        pass

    def game_end(self, game: GameState):
        pass
