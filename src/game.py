import time

from src.experiments.base_experiment import BaseExperiment
from src.interfaces.game_state import GameState, Piece


class Game:
    instance = None

    def __init__(self, experiment: BaseExperiment):
        self.game_state = GameState()
        self.game_state.reset()

        self.experiment = experiment

        self.do_render = experiment.do_render

        self.playing = True

    def update(self):

        if not self.playing:
            return

        # Tell agents to move.
        # If agent is human, then human will act on its own through ui to change current_player
        if self.game_state.winner == Piece.NONE and self.game_state.current_player == Piece.BLUE:
            self.experiment.blue_agent.move(self.game_state)
        if self.game_state.winner == Piece.NONE and self.game_state.current_player == Piece.RED:
            self.experiment.red_agent.move(self.game_state)

        # If game ended, tell agents and experiment
        if self.game_state.winner != Piece.NONE:
            self.experiment.blue_agent.game_end(self.game_state)
            self.experiment.red_agent.game_end(self.game_state)
            if self.experiment.game_ended(self.game_state):
                self.game_state.reset()
            else:
                self.playing = False
