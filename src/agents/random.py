import random

from src.agents.base_agent import BaseAgent
from src.interfaces.cards_enum import CARDS
from src.interfaces.game_state import GameState, Piece


class RandomAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def game_end(self, game: GameState):
        pass

    def move(self, game: GameState):

        moves = game.get_possible_actions()

        # If there is a move
        if len(moves) > 0:
            actual_move = random.choice(moves)
            # print(f'[Random {self.player}] Making move: {actual_move}')
            game.make_move_tuple(actual_move)  # Make it
        else:
            # print(f'[Random {self.player}] No moves! Passing turn...')
            game.pass_move()
