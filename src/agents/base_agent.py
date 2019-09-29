from src.interfaces.game_state import GameState, Piece


class BaseAgent:
    def __init__(self):
        pass

    def game_start(self, game: GameState, player: Piece):
        pass

    def move(self, game: GameState):
        pass

    def game_end(self, game: GameState):
        pass
