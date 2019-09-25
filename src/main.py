import pygame
from src.game import Game
from src.render import Screen

def main():
    game = Game()
    screen = Screen(game)

    clock = pygame.time.Clock()

    while screen.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                screen.running = False

        screen.update()

        #wait for next frame
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
