from src.components.card import Card, CARDS
from src.game import Game
import random


class BaseAgent:
    def __init__(self):
        pass

    def move(self, pieces, cards: Card, game: Game, player_number):
        moves = []
        for piece in pieces:
            for card in cards:
                for card_move in CARDS[card.card]:
                    if game.check_valid_card_move(piece[0], piece[1], piece[0] + card_move[0], piece[1] + card_move[1]):
                        moves.append((piece, card_move))

        actual_move = random.choice(moves)
        game.selected_card = card
        game.selected_card_index = 0
        game.selected_board_x = actual_move[0][0]
        game.selected_board_y = actual_move[0][1]
        game.make_move(game.selected_board_x + actual_move[1][0], game.selected_board_y + actual_move[1][1])
