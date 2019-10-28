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


class QLearningAgentDouble(BaseAgent):
    def __init__(self):
        super().__init__()

        self.QA = {}
        self.QB = {}
        self.alpha = 0.05  # Learning rate
        self.gamma = 0.98  # Discount factor
        self.epsilon = 0.15  # Epsilon greedy

        self.last_state_key_blue = None
        self.last_state_key_red = None

    def write_to_file(self, file):
        with open(file, 'wb') as f:
            pickle.dump(self.QA, f)

    def read_from_file(self, file):
        with open(file, 'rb') as f:
            self.QA = pickle.load(f)

    def q_learn(self, last_state, reward, best_b_from_a, best_a_from_b):
        new_QA = self.getQA(last_state) + self.alpha * (reward + self.gamma * best_b_from_a - self.getQA(last_state))
        new_QB = self.getQB(last_state) + self.alpha * (reward + self.gamma * best_a_from_b - self.getQB(last_state))

        # Don't write 0's, no point but wastes space
        if new_QA != 0:
            self.QA[last_state] = new_QA
        if new_QB != 0:
            self.QB[last_state] = new_QB

    def game_end(self, game: GameState):
        # give +1 if win, -1 if lose

        if self.last_state_key_blue is not None and game.winner == Piece.BLUE:
            self.q_learn(self.last_state_key_blue, 1, 0, 0)
            self.q_learn(self.last_state_key_red, -1, 0, 0)
        elif self.last_state_key_red is not None:
            self.q_learn(self.last_state_key_red, 1, 0, 0)
            self.q_learn(self.last_state_key_blue, -1, 0, 0)

        self.last_state_key_blue = None
        self.last_state_key_red = None

    def getQA(self, key):
        if key not in self.QA:
            return 0  # Default everything at 0.5 here!!!
        else:
            return self.QA[key]

    def getQB(self, key):
        if key not in self.QB:
            return 0  # Default everything at 0.5 here!!!
        else:
            return self.QB[key]

    def move(self, game: GameState):

        actions = game.get_possible_actions()
        action_key_value_pairs = []

        for action in actions:
            key = game_state_to_q_state(game, action)
            value = self.getQA(key)
            action_key_value_pairs.append((action, key, value))

        random.shuffle(action_key_value_pairs)
        action_key_value_pairs.sort(key=lambda x: x[2], reverse=True)
        max_action_a = action_key_value_pairs[0][0]
        max_action_key_a = action_key_value_pairs[0][1]
        max_action_value_b_from_a = self.getQB(max_action_key_a)

        action_key_value_pairs = []

        for action in actions:
            key = game_state_to_q_state(game, action)
            value = self.getQB(key)
            action_key_value_pairs.append((action, key, value))

        random.shuffle(action_key_value_pairs)
        action_key_value_pairs.sort(key=lambda x: x[2], reverse=True)
        max_action_key_b = action_key_value_pairs[0][1]
        max_action_value_a_from_b = self.getQB(max_action_key_b)

        if random.random() < self.epsilon:
            # pick random action lol
            max_action_a = random.choice(actions)
            max_action_key_a = game_state_to_q_state(game, max_action_a)



        # cool line to get percentage confidence of winning based on last move
        # uncomment when playing against agent
        # print(f'Confidence: {max_action_value}')

        if game.current_player == Piece.BLUE:
            if self.last_state_key_blue is not None:
                self.q_learn(self.last_state_key_blue, 0, max_action_value_b_from_a, max_action_value_a_from_b)

            self.last_state_key_blue = max_action_key_a

        else:
            if self.last_state_key_red is not None:
                self.q_learn(self.last_state_key_red, 0, max_action_value_b_from_a, max_action_value_a_from_b)

            self.last_state_key_red = max_action_key_a

        game.make_move_tuple(max_action_a)
