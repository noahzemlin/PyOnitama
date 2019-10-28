import json
import random
import pickle

from src.agents.base_agent import BaseAgent
from src.interfaces.game_state import GameState, Piece
from src.interfaces.cards_enum import CARDS_ID


def game_state_to_q_state(game: GameState, action_tuple):
    state = ""

    cards = game.cards.copy()  # backup while we destroy them LOL

    # sort cards to ignore order
    if game.cards[3] > game.cards[4]:
        temp = game.cards[3]
        game.cards[3] = game.cards[4]
        game.cards[4] = temp

    if game.cards[0] > game.cards[1]:
        temp = game.cards[0]
        game.cards[0] = game.cards[1]
        game.cards[1] = temp

    if game.current_player == Piece.BLUE:
        for i in range(0, 5):
            for j in range(0, 5):
                state += str(game[j, i].value)
        for i in [0, 1, 2, 3, 4]:
            state += str(CARDS_ID[game.cards[i]])

        # Add in action
        state += str(action_tuple[0])  # from x
        state += str(action_tuple[1])  # from y
        state += str(action_tuple[2])  # to x
        state += str(action_tuple[3])  # to y
        state += str(CARDS_ID[cards[action_tuple[4]]])  # card
    else:
        for i in range(0, 5)[::-1]:  # flip the board by reversing locations
            for j in range(0, 5)[::-1]:
                piece = game[j, i]
                if piece == Piece.BLUE:
                    piece = Piece.RED
                elif piece == Piece.RED:
                    piece = Piece.BLUE
                elif piece == Piece.RED_KING:
                    piece = Piece.BLUE_KING
                elif piece == Piece.BLUE_KING:
                    piece = Piece.RED_KING
                state += str(piece.value)

        for i in [3, 4, 2, 0, 1]:  # same here
            state += str(CARDS_ID[game.cards[i]])

        # Add in action
        state += str(4 - action_tuple[0])  # from x
        state += str(4 - action_tuple[1])  # from y
        state += str(4 - action_tuple[2])  # to x
        state += str(4 - action_tuple[3])  # to y
        state += str(CARDS_ID[cards[action_tuple[4]]])  # card

    game.cards = cards
    return state


class QLearningAgent_But_Pass(BaseAgent):
    def __init__(self):
        super().__init__()

        self.Q = {}
        self.last_num = 0

    def write_to_file(self, file):
        with open(file, 'wb') as f:
            pickle.dump(self.Q, f)

    def read_from_file(self, file):
        with open(file, 'rb') as f:
            self.Q = pickle.load(f)

    def game_end(self, game: GameState):
        pass

    def getQ(self, key):
        if key not in self.Q:
            return 0  # Default everything at 0.5 here!!!
        else:
            return self.Q[key]

    def move(self, game: GameState):

        if game.turn_num == self.last_num:
            return

        actions = game.get_possible_actions()
        action_key_value_pairs = []

        for action in actions:
            key = game_state_to_q_state(game, action)
            value = self.getQ(key)
            action_key_value_pairs.append((action, key, value))

        random.shuffle(action_key_value_pairs)
        action_key_value_pairs.sort(key=lambda x: x[2], reverse=True)
        max_action_value = action_key_value_pairs[0][2]

        print("suggestion: ")
        print(action_key_value_pairs)

        # cool line to get percentage confidence of winning based on last move
        # uncomment when playing against agent
        print(f'Confidence: {max_action_value}')

        self.last_num = game.turn_num
