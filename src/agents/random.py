import random

from src.agents.base_agent import BaseAgent
from src.interfaces.cards_enum import CARDS
from src.interfaces.game_state import GameState, Piece


class RandomAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.first_turn = True

    def game_end(self, game: GameState):
        pass

    def move(self, game: GameState):

        moves = []

        # Find pieces
        pieces = []
        for x in range(0, 5):
            for y in range(0, 5):
                if game[x, y].value == game.current_player.value or game[x, y].value == game.current_player.value + 1:
                    pieces.append((x, y))

        # Get Available Cards
        if game.current_player == Piece.BLUE:
            available_cards = [0, 1]
        else:
            available_cards = [3, 4]

        # For each card, for each piece, find valid moves
        for card_index in available_cards:
            move_options = CARDS[game.cards[card_index]]
            for move_option in move_options:
                for piece in pieces:
                    x = piece[0]
                    y = piece[1]
                    if game.current_player == Piece.BLUE and game.check_valid_move(x, y, x + move_option[0],
                                                                                   y - move_option[1],
                                                                                   card_index):  # blue side
                        moves.append((x, y, x + move_option[0], y - move_option[1], card_index))
                    if game.current_player == Piece.RED and game.check_valid_move(x, y, x - move_option[0],
                                                                                  y + move_option[1],
                                                                                  card_index):  # red side
                        moves.append((x, y, x - move_option[0], y + move_option[1], card_index))

        # If there is a move
        if len(moves) > 0:
            actual_move = random.choice(moves)
            # print(f'[Random {self.player}] Making move: {actual_move}')
            game.make_move_tuple(actual_move)  # Make it
        else:
            # print(f'[Random {self.player}] No moves! Passing turn...')
            game.pass_move()
