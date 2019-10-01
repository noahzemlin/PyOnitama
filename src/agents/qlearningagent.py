import json
import random

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


class QLearningAgent(BaseAgent):
    def __init__(self, file=None):
        super().__init__()

        self.Q = {}
        self.alpha = 0.10  # Learning rate
        self.gamma = 0.98  # Discount factor
        self.epsilon = 0.15  # Epsilon greedy

        self.last_state_key_blue = None
        self.last_state_key_red = None

        self.last_played = Piece.NONE

        if file is not None:
            with open(file, 'r') as f:
                self.Q = json.load(f)

    def q_learn(self, last_state, reward, future_estimate):
        new_Q = (1 - self.alpha) * self.getQ(last_state) + self.alpha * (reward + self.gamma * future_estimate)

        # Don't write 0's, no point but wastes space
        if new_Q != 0:
            self.Q[last_state] = new_Q

    def game_end(self, game: GameState):
        # give +5 if win, -2.5 if lose

        if self.last_state_key_blue is not None and game.winner == Piece.BLUE:
            self.q_learn(self.last_state_key_blue, 5, 0)
            self.q_learn(self.last_state_key_red, -2.5, 0)
        elif self.last_state_key_red is not None:
            self.q_learn(self.last_state_key_blue, -2.5, 0)
            self.q_learn(self.last_state_key_red, 5, 0)

        self.last_state_key_blue = None
        self.last_state_key_red = None

    def getQ(self, key):
        if key not in self.Q:
            return 0  # Default everything at 0 here!!!
        else:
            return self.Q[key]

    def move(self, game: GameState):

        self.last_played = game.current_player

        max_action = None
        max_action_value = -100000
        actions = game.get_possible_actions()

        if random.random() < self.epsilon:
            # pick random action lol
            max_action = random.choice(actions)
            max_action_value = self.getQ(game_state_to_q_state(game, max_action))
        else:
            action_value = {}
            for action in actions:
                value = self.getQ(game_state_to_q_state(game, action))
                action_value[action] = value
                if value > max_action_value:
                    max_action = action
                    max_action_value = value
            if max_action_value == 0:  # if no learned path, pick random path
                max_action = random.choice([action for action in actions if action_value[action] == 0])

        # cool line to get percentage confidence of winning based on last move
        # uncomment when playing against agent
        # print(f'Confidence: {max_action_value/5}')

        if game.current_player == Piece.BLUE:
            if self.last_state_key_blue is not None:
                self.q_learn(self.last_state_key_blue, 0, max_action_value)

            self.last_state_key_blue = game_state_to_q_state(game, max_action)

        else:
            if self.last_state_key_red is not None:
                self.q_learn(self.last_state_key_red, 0, max_action_value)

            self.last_state_key_red = game_state_to_q_state(game, max_action)

        game.make_move_tuple(max_action)
