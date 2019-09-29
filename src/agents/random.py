import random
from src.interfaces.game_state import GameState, Piece
from src.interfaces.cards_enum import CARDS
from src.agents.base_agent import BaseAgent


class RandomAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.num_games = 0
        self.won_games = 0

        self.player = Piece.NONE

    def game_start(self, game: GameState, player: Piece):
        self.player = player

    def game_end(self, game: GameState):
        self.num_games += 1

        if game.winner == self.player:
            self.won_games += 1

        if self.num_games == 100:
            print(f'[Random {self.player}] 100 games complete! Win-rate: {self.won_games / self.num_games}')
            return False  # Return False to stop simulation
        else:
            return True  # Return True to start new game

    def move(self, game: GameState):
        moves = []

        if game.current_player == Piece.BLUE:
            available_cards = [0, 1]
        else:
            available_cards = [3, 4]

        for card_index in available_cards:
            move_options = CARDS[game.cards[card_index]]
            for move_option in move_options:
                for x in range(0, 5):
                    for y in range(0, 5):
                        if game.check_valid_move(x, y, x + move_option[0], y - move_option[1], card_index):  # blue side
                            moves.append((x, y, x + move_option[0], y - move_option[1], card_index))
                        if game.check_valid_move(x, y, x - move_option[0], y + move_option[1], card_index):  # red side
                            moves.append((x, y, x - move_option[0], y + move_option[1], card_index))

        if len(moves) > 0:
            actual_move = random.choice(moves)
            #print(f'[Random {self.player}] Making move: {actual_move}')
            game.make_move_tuple(actual_move)
        else:
            #print(f'[Random {self.player}] No moves! Passing turn...')
            game.pass_move()
