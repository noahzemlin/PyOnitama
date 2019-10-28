import json
import random
import copy

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

class TDLambdaLearningAgentRed(BaseAgent):
    def __init__(self, file=None):
        self.V = {} # Map S -> R
        self.alpha = 0.005  # Learning rate
        self.gamma = 0.98  # Discount factor
        self.epsilon = 0.15  # Epsilon greedy
        self.tdLambda = 0.7 #For TD_Lambda
        self.moveDepth = 0

        #Things that NEED to be reset each game
        self.e = {}
        self.statesThisGame=[]
        self.bestAvgY=4
        self.last_state_key = None
        self.lastGameState = None

        if file is not None:
            with open(file, 'r') as f:
                self.V= json.load(f)

    def reset_game(self):
        self.last_state_key=None
        self.bestAvgY=4
        self.e={}
        self.statesThisGame=[]
        self.lastGameState=None

    def reward(self, lastTurn: GameState, now: GameState):
        numBluePawnsLast=0
        numRedPawnsLast=0
        numBluePawnsNow=0
        numRedPawnsNow=0
        totalYLast=0.0
        totalYNow=0.0
        for x in range(0,5):
            for y in range(0,5):
                if lastTurn.board[x][y] == Piece.RED or lastTurn.board[x][y] == Piece.RED_KING:
                    numRedPawnsLast += 1
                    totalYLast+=y

                elif lastTurn.board[x][y] == Piece.BLUE or lastTurn.board[x][y] == Piece.BLUE_KING:
                    numBluePawnsLast += 1

                if now.board[x][y] == Piece.RED or now.board[x][y] == Piece.RED_KING:
                    numRedPawnsNow += 1
                    totalYNow+=y
                elif now.board[x][y] == Piece.BLUE or now.board[x][y] == Piece.BLUE_KING:
                    numBluePawnsNow += 1

        reward=0.0
        if numBluePawnsLast>numBluePawnsNow:
            reward += 0.5
        if numRedPawnsLast>numRedPawnsNow:
            reward -= 0.5
        avgYNow=totalYNow/numRedPawnsNow
        if avgYNow < self.bestAvgY:
            reward += 0.05
            self.bestAvgY=avgYNow
        return reward

    def td_learn(self, last_game: GameState, reward, cur_game: GameState):
        if reward==0:
            reward=self.reward(last_game,cur_game)
        reward=-1.0*reward

        last_state=game_to_v_state(self.lastGameState)
        cur_state=game_to_v_state(cur_game)

        old_V = self.getV(last_state)

        delta=reward+self.gamma*self.getV(cur_state)-old_V

        if last_state not in self.e:
            self.e[last_state]=0
        if last_state not in self.V:
            self.V[last_state]=0

        self.e[last_state]=self.e[last_state]+1
        self.statesThisGame.append(last_state)
        for state in self.statesThisGame:
            if state != last_state:
                self.e[state]=self.gamma*self.tdLambda*self.e[state]
        for state in self.statesThisGame:
            self.V[state]=self.V[state]+self.alpha*delta*self.e[state]
        # new_V = old_V + self.alpha*(reward + self.gamma*self.getV(cur_state)-old_V)
        # if new_V != old_V:
        #     self.V[last_state] = new_V

    def game_end(self, game: GameState):
        if game.winner == Piece.RED:
            self.td_learn(self.lastGameState, 5.0, game)
            #print("TD WINS!!!")
        else:
            self.td_learn(self.lastGameState, -5.0, game)
            #print("Other wins...")

    def getV(self, key):
        if key not in self.V:
            return 0  # Default everything at 0 here!!!
        else:
            return self.V[key]


    def move(self, game: GameState):
        if self.last_state_key != None:
            self.td_learn(self.lastGameState, 0, game)
        chosen_action = None
        actions = game.get_possible_actions()
        random.shuffle(actions) # get a random move if all are equal
        if random.random() < self.epsilon:
            chosen_action = random.choice(actions)
        else:
            min_V = 10000
            for action in actions:
                tempGame=copy.deepcopy(game)
                tempGame.make_move_tuple(action)
                tempGameV=self.miniMax(tempGame,1)
                if tempGameV < min_V:
                    chosen_action = action
                    min_V=tempGameV
        self.last_state_key=game_to_v_state(game)
        self.lastGameState=game
        game.make_move_tuple(chosen_action)

    def miniMax(self, game: GameState,depth):
        if game.winner != Piece.NONE:
            if game.winner == Piece.RED:
                return -9999
            else:
                return 9999

        if depth>=self.moveDepth:
            return self.getV(game_to_v_state(game))

        chosen_action = None
        actions = game.get_possible_actions()
        random.shuffle(actions)
        best_V=0
        if game.current_player==Piece.RED:
            best_V=10000
            for action in actions:
                tempGame=copy.deepcopy(game)
                tempGame.make_move_tuple(action)
                actionV=self.miniMax(tempGame,depth+1)
                if actionV < best_V:
                    best_V = actionV
                    chosen_action=action
        else:
            best_V=-10000
            for action in actions:
                tempGame=copy.deepcopy(game)
                tempGame.make_move_tuple(action)
                actionV=self.miniMax(tempGame,depth+1)
                if actionV > best_V:
                    best_V = actionV
                    chosen_action=action
        return best_V
