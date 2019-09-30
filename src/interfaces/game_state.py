import random
from enum import Enum

from src.interfaces.cards_enum import CARDS


class Piece(Enum):
    NONE = 0
    BLUE = 1
    BLUE_KING = 2
    RED = 3
    RED_KING = 4


class GameState:
    def __init__(self):
        self.board = [[Piece.NONE for i in range(0, 5)] for j in range(0, 5)]
        self.cards = ["", "", "", "", ""]
        self.current_player = Piece.BLUE
        self.winner = Piece.NONE
        self.turn_num = 0

    def __setitem__(self, board_tuple, piece):
        self.board[board_tuple] = piece

    def __getitem__(self, board_tuple):
        return self.board[board_tuple[0]][board_tuple[1]]

    def set_cards(self, cards=None):
        if cards is None:
            self.cards = list(CARDS.keys())
            random.shuffle(self.cards)
            self.cards = self.cards[0:5]
        else:
            self.cards = cards

    def reset(self):
        self.board = [[Piece.NONE for i in range(0, 5)] for j in range(0, 5)]

        self.board[0][0] = Piece.RED
        self.board[1][0] = Piece.RED
        self.board[2][0] = Piece.RED_KING
        self.board[3][0] = Piece.RED
        self.board[4][0] = Piece.RED

        self.board[0][4] = Piece.BLUE
        self.board[1][4] = Piece.BLUE
        self.board[2][4] = Piece.BLUE_KING
        self.board[3][4] = Piece.BLUE
        self.board[4][4] = Piece.BLUE

        self.current_player = Piece.BLUE
        self.winner = Piece.NONE
        self.turn_num = 0

        self.set_cards()

    def make_move_tuple(self, tup):
        self.make_move(tup[0], tup[1], tup[2], tup[3], tup[4])

    def make_move(self, from_x, from_y, to_x, to_y, card):
        if self.check_valid_move(from_x, from_y, to_x, to_y, card):

            # Check if moving onto king and give win
            if self.board[to_x][to_y] == Piece.BLUE_KING:
                self.winner = Piece.RED
            if self.board[to_x][to_y] == Piece.RED_KING:
                self.winner = Piece.BLUE

            # Check if moving king onto home and give win
            if self.board[from_x][from_y] == Piece.BLUE_KING and to_x == 2 and to_y == 0:
                self.winner = Piece.BLUE
            if self.board[from_x][from_y] == Piece.RED_KING and to_x == 2 and to_y == 4:
                self.winner = Piece.RED

            # Move piece
            self.board[to_x][to_y] = self.board[from_x][from_y]
            self.board[from_x][from_y] = Piece.NONE

            # Swap card
            temp = self.cards[2]
            self.cards[2] = self.cards[card]
            self.cards[card] = temp

            # Change player turn
            if self.current_player == Piece.RED:
                self.current_player = Piece.BLUE
            else:
                self.current_player = Piece.RED

            # Increase turn number every move
            self.turn_num += 1

    def check_valid_move(self, from_x, from_y, to_x, to_y, card):

        card = self.cards[card]
        positions = CARDS[card]

        # If out of bounds
        if to_x < 0 or to_x > 4 or to_y < 0 or to_y > 4:
            return False

        # If not owned piece
        if not (0 <= self.board[from_x][from_y].value - self.current_player.value <= 1):
            return False

        # If moving onto friendly piece
        if 0 <= self.board[to_x][to_y].value - self.current_player.value <= 1:
            return False

        # Look for any valid position move
        if self.current_player == Piece.BLUE:
            for possible in positions:
                dx = possible[0]
                dy = -possible[1]
                if to_x - from_x == dx and to_y - from_y == dy:
                    return True
        else:
            for possible in positions:
                dx = -possible[0]
                dy = possible[1]
                if to_x - from_x == dx and to_y - from_y == dy:
                    return True

        return False

    def pass_move(self):
        if self.current_player == Piece.RED:
            self.current_player = Piece.BLUE
        else:
            self.current_player = Piece.RED
