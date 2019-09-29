from src.interfaces.game_state import GameState, Piece


class InterfaceState:
    def __init__(self, game_state: GameState):
        self.selected_card = -1
        self.selected_board = (-1, -1)
        self.game_state = game_state

    def select_card(self, index):
        if (index == 0 or index == 1) and self.game_state.current_player == Piece.BLUE:
            self.selected_card = index
        elif (index == 3 or index == 4) and self.game_state.current_player == Piece.RED:
            self.selected_card = index

    def select_board(self, x, y):
        if self.selected_card == -1:
            return

        # Select friendly piece
        if self.game_state.current_player == Piece.BLUE and (
                self.game_state[x, y] == Piece.BLUE or self.game_state[x, y] == Piece.BLUE_KING):
            self.selected_board = (x, y)
            return

        if self.game_state.current_player == Piece.RED and (
                self.game_state[x, y] == Piece.RED or self.game_state[x, y] == Piece.RED_KING):
            self.selected_board = (x, y)
            return

        # If friendly piece selected and chose another place, perform move
        if self.selected_board != (-1, -1):
            if self.game_state.check_valid_move(self.selected_board[0], self.selected_board[1], x, y, self.selected_card):
                self.game_state.make_move(self.selected_board[0], self.selected_board[1], x, y, self.selected_card)
                self.selected_card = -1
                self.selected_board = (-1, -1)
