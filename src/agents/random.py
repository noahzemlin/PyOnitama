import random
from src.game import GameState
from src.interfaces.cards_enum import CARDS
from src.agents.base_agent import BaseAgent


class RandomAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def move(self, game: GameState, player_number):
        moves = []

        for card in game.cards:
            move_options = CARDS[card]
            for move_option in move_options:
                for x in range(0, 5):
                    for y in range(0, 5):
                        if game.check_valid_move(x, y, x + move_option[0], y + move_option[1], card):
                            moves.append((x, y, x + move_option[0], y + move_option[1], card))

        actual_move = random.choice(moves)

        return actual_move
