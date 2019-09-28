import numpy as np


def game():
    return Game.instance


class Game:
    instance = None

    def __init__(self):
        # Define game state as 5 by 5 grid. Each piece is uniquely numbered and
        # id is stored at the matrix position. 0,0 is top left.
        self.game_state = np.zeros((5, 5))

        # place pieces
        for i in range(1, 6):
            self.game_state[i - 1, 0] = i
            self.game_state[i - 1, 4] = i + 5

        from src.components.card import Card, CARDS

        self.card_state = [Card(card) for card in CARDS][:5]
        self.selected_card = None
        self.selected_card_index = -1
        self.selected_board_x = -1
        self.selected_board_y = -1
        self.current_player = 0

        Game.instance = self

    def select_card(self, card):
        if (card == self.card_state[0] or card == self.card_state[1]) and self.current_player == 0:
            self.selected_card = card
            for i in range(0, 5):
                if card == self.card_state[i]:
                    self.selected_card_index = i
        elif (card == self.card_state[3] or card == self.card_state[4]) and self.current_player == 1:
            self.selected_card = card
            for i in range(0, 5):
                if card == self.card_state[i]:
                    self.selected_card_index = i

    def make_move(self, x, y):
        self.game_state[x, y] = self.game_state[self.selected_board_x, self.selected_board_y]
        self.game_state[self.selected_board_x, self.selected_board_y] = 0
        self.selected_board_x = self.selected_board_y = -1
        self.current_player = 1 - self.current_player
        self.card_state[self.selected_card_index] = self.card_state[2]
        self.card_state[2] = self.selected_card
        self.selected_card = None
        self.check_win()

    def select_tile(self, x, y):

        # successful player 1 move
        if self.selected_card is not None and self.selected_board_x != -1 \
                and self.check_valid_card_move(self.selected_board_x, self.selected_board_y, x, y, self.selected_card) \
                and ((self.game_state[x, y] == 0 or self.game_state[x, y] > 5) and self.current_player == 0):
            self.make_move(x, y)
            return

        # successful player 2 move
        if self.selected_card is not None and self.selected_board_x != -1 \
                and self.check_valid_card_move(self.selected_board_x, self.selected_board_y, x, y, self.selected_card) \
                and ((self.game_state[x, y] == 0 or self.game_state[x, y] <= 5) and self.current_player == 1):
            self.make_move(x, y)
            return

        if ((1 <= self.game_state[x, y] <= 5 and self.current_player == 0) or (
                self.game_state[x, y] > 5 and self.current_player == 1)):
            self.selected_board_x = x
            self.selected_board_y = y

    def check_valid_card_move(self, from_x, from_y, to_x, to_y, card):

        # print(f'attempting to move from ({fromX},{fromY}) to ({toX},{toY}) with {card.card}')

        from src.components.card import CARDS

        positions = CARDS[card.card]

        if self.current_player == 0:
            for possible in positions:
                dx = -possible[0]
                dy = possible[1]
                if to_x - from_x == dx and to_y - from_y == dy:
                    return True
        else:
            for possible in positions:
                dx = possible[0]
                dy = -possible[1]
                if to_x - from_x == dx and to_y - from_y == dy:
                    return True

        return False

    def check_win(self):
        # win by reaching enemy start
        if self.game_state[2, 0] == 8:
            self.current_player = 3
        if self.game_state[2, 4] == 3:
            self.current_player = 2

        player1_master = False
        player2_master = False

        for x in range(0, 5):
            for y in range(0, 5):
                if self.game_state[x, y] == 3:
                    player1_master = True
                if self.game_state[x, y] == 8:
                    player2_master = True

        if not player1_master:
            self.current_player = 3
        if not player2_master:
            self.current_player = 2
