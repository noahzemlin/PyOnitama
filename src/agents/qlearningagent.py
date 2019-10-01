import json
import random

from src.agents.base_agent import BaseAgent
from src.interfaces.game_state import GameState, Piece


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
        for i in range(0, 5):
            state += str(game.cards[i])

        # Add in action
        state += str(action_tuple[0])  # from x
        state += str(action_tuple[1])  # from y
        state += str(action_tuple[2])  # to x
        state += str(action_tuple[3])  # to y
        state += str(cards[action_tuple[4]])  # card
    else:
        for i in range(0, 5)[::-1]:  # flip the board by reversing locations
            for j in range(0, 5)[::-1]:
                state += str(game[i, j].value)

        for i in [3, 4, 2, 0, 1]:  # same here
            state += str(game.cards[i])

        # Add in action
        state += str(5 - action_tuple[0])  # from x
        state += str(5 - action_tuple[1])  # from y
        state += str(5 - action_tuple[2])  # to x
        state += str(5 - action_tuple[3])  # to y
        state += str(cards[action_tuple[4]])  # card

    game.cards = cards
    return state


class QLearningAgent(BaseAgent):
    def __init__(self, file=None):
        super().__init__()

        self.Q = {}
        self.alpha = 0.20  # Learning rate
        self.gamma = 0.95  # Discount factor
        self.epsilon = 0.1  # Epsilon greedy
        self.side = Piece.NONE
        self.last_state_key = None

        if file is not None:
            with open(file, 'r') as f:
                self.Q = json.load(f)

    def game_end(self, game: GameState):
        # give +5 if win, -5 if lose
        if game.winner == self.side:
            self.Q[self.last_state_key] = (1 - self.alpha) * self.getQ(self.last_state_key) + self.alpha * (5 + 0)
        else:
            self.Q[self.last_state_key] = (1 - self.alpha) * self.getQ(self.last_state_key) + self.alpha * (-5 + 0)

    def getQ(self, key):
        if key not in self.Q:
            return 0  # Default everything at 0 here!!!
        else:
            return self.Q[key]

    def move(self, game: GameState):

        self.side = game.current_player

        max_action = None
        max_action_value = -100000
        actions = game.get_possible_actions()

        if random.random() < self.epsilon:
            # pick random action lol
            max_action = random.choice(actions)
            max_action_value = self.getQ(game_state_to_q_state(game, max_action))
        else:
            for action in actions:
                value = self.getQ(game_state_to_q_state(game, action))
                if value > max_action_value:
                    max_action = action
                    max_action_value = value
            if max_action_value == 0:  # if no learned path, pick random path
                max_action = random.choice(actions)

        self.Q[self.last_state_key] = (1 - self.alpha) * self.getQ(self.last_state_key) + self.alpha * (
                    0 + self.gamma * max_action_value)

        self.last_state_key = game_state_to_q_state(game, max_action)
        game.make_move_tuple(max_action)
