import random

from src.agents.base_agent import BaseAgent
from src.interfaces.game_state import GameState, Piece


class HeuristicAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def game_end(self, game: GameState):
        pass

    def move(self, game: GameState):

        moves = game.get_possible_actions()

        # If there is a move
        if len(moves) > 0:
            ratings = [[move, 0] for move in moves]

            for rating in ratings:
                move = rating[0]
                if move[3] > move[1] and game.current_player == Piece.RED:  # moving forward is good
                    rating[1] = rating[1] + 1
                if move[3] < move[1] and game.current_player == Piece.BLUE:  # moving forward is good
                    rating[1] = rating[1] + 1

                if 0 <= game[(move[2], move[
                    3])].value - Piece.BLUE.value <= 1 and game.current_player == Piece.RED:  # is red moving onto blue
                    rating[1] = rating[1] + 2
                if 0 <= game[(move[2], move[
                    3])].value - Piece.RED.value <= 1 and game.current_player == Piece.BLUE:  # is blue moving onto red
                    rating[1] = rating[1] + 2

                if game.does_move_win_tuple(move):  # if win, do it
                    rating[1] = rating[1] + 10

            random.shuffle(ratings)
            ratings.sort(key=lambda x: x[1], reverse=True)

            game.make_move_tuple(ratings[0][0])  # Make it
        else:
            game.pass_move()
