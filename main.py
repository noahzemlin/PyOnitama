import pygame

from src.experiments.play_against_q_agent import PlayAgainstQExperiment
from src.experiments.tdlam_learning import TDLambdaLearningExperiment
from src.experiments.tdlam_vs_tdlam_learning import TDLambdaVsTDLambdaLearningExperiment
from src.experiments.play_against_td_lam import HumanTDLamExperiment
from src.experiments.td_learning import TDLearningExperiment
from src.experiments.q_learning import QLearningExperiment
from src.experiments.q_learning_double import QLearningExperimentDouble
from src.experiments.q_learning_withdecay import QLearningExperimentWithDecay
from src.game import Game
from src.render import Screen


def main():

    game = Game(PlayAgainstQExperiment())

    if game.do_render:

        screen = Screen(game.game_state)

        clock = pygame.time.Clock()

        while screen.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    screen.running = False

            game.update()
            screen.update()

            # wait for next frame
            clock.tick(60)

        pygame.quit()

    else:

        while game.playing:
            game.update()


if __name__ == "__main__":
    main()
