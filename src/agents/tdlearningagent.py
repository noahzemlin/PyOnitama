import json
import random

from src.agents.base_agent import BaseAgent
from src.interfaces.game_state import GameState, Piece
from src.interfaces.cards_enum import CARDS_ID

def game_to_v_state(game: GameState):
    state = ""

    cards = game.cards.copy()

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

    game.cards = cards
    return state

class TDLearningAgent(BaseAgent):
    def __init__(self, file=None):
        self.V = {} # Map S -> R
        self.alpha = 0.10  # Learning rate
        self.gamma = 0.98  # Discount factor
        self.epsilon = 0.15  # Epsilon greedy

        self.last_state_key = None

        if file is not None:
            with open(file, 'r') as f:
                self.V= json.load(f)

    def td_learn(self, last_state, reward, cur_state):
        old_V = self.getV(last_state)
        new_V = old_V + self.alpha*(reward + self.gamma*self.getV(cur_state)-old_V)

        if new_V != old_V:
            self.V[last_state] = new_V

    def game_end(self, game: GameState):
        if game.winner == Piece.BLUE:
            self.td_learn(self.last_state_key, 5, game_to_v_state(game))
            #print("TD WINS!!!")
        else:
            self.td_learn(self.last_state_key, -5, game_to_v_state(game))
            #print("Other wins...")

    def getV(self, key):
        if key not in self.V:
            return 0  # Default everything at 0 here!!!
        else:
            return self.V[key]


    def move(self, game: GameState):
        self.td_learn(self.last_state_key, 0, game_to_v_state(game))
        chosen_action = None
        actions = game.get_possible_actions()
        random.shuffle(actions) # get a random move if all are equal
        if random.random() < self.epsilon:
            chosen_action = random.choice(actions)
        else:
            max_V = -10000
            for action in actions:
                tempGame=game
                tempGame.make_move_tuple(action)
                VOfAction=self.getV(game_to_v_state(tempGame))
                if VOfAction>max_V:
                    chosen_action=action
                    max_V=VOfAction
        self.last_state_key=game_to_v_state(game)
        game.make_move_tuple(chosen_action)
