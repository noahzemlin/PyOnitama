import pygame

from src.components.card import Card
from src.game import Game

from src.components.board import draw_board

# constants
SCREEN_SCALE = 0.8
SCREENRECT = pygame.Rect(0, 0, int(1000 * SCREEN_SCALE), int(1000 * SCREEN_SCALE))


def get_mouse_position():
    return int(pygame.mouse.get_pos()[0] / SCREEN_SCALE), int(pygame.mouse.get_pos()[1] / SCREEN_SCALE)


class Screen:

    def __init__(self, game: Game):
        self.game = game
        self.running = True

        pygame.init()
        pygame.display.set_caption('PyOnitama')

        best_color_depth = pygame.display.mode_ok(SCREENRECT.size, 0, 32)
        self.screen = pygame.display.set_mode(SCREENRECT.size, 0, best_color_depth)
        self.pieces = [pygame.image.load("assets/" + filename).convert_alpha() for filename in
                       ['red_pawn.png', 'red_king.png', 'blue_pawn.png', 'blue_king.png']]

        if Card.FONT is None:
            Card.FONT = pygame.font.Font('freesansbold.ttf', 24)

    def update(self):
        screen = pygame.Surface((1000, 1000))
        pieces = self.pieces

        # render
        screen.fill((255, 255, 255))
        draw_board(screen, self.game)

        # draw whose turn it is
        if self.game.current_player <= 1:
            text_surf = Card.FONT.render("Player " + str(self.game.current_player + 1) + "'s turn!", True, (0, 0, 0))
            text_rect = text_surf.get_rect()
            if self.game.current_player == 0:
                text_rect.center = (220, 40)
            else:
                text_rect.center = (220, 960)
        else:
            if self.game.current_player == 2:
                text_surf = Card.FONT.render("Player 1 Won!", True, (0, 0, 0))
            else:
                text_surf = Card.FONT.render("Player 2 Won!", True, (0, 0, 0))
            text_rect = text_surf.get_rect()
            text_rect.center = (220, 40)
        screen.blit(text_surf, text_rect)

        # draw cards
        self.game.card_state[0].draw(screen, 20, 90, self.game)  # top left
        self.game.card_state[1].draw(screen, 270, 90, self.game)  # top right
        self.game.card_state[2].draw(screen, 550, 440, self.game)  # center
        self.game.card_state[3].draw(screen, 20, 790, self.game)  # bottom left
        self.game.card_state[4].draw(screen, 270, 790, self.game)  # bottom right

        # draw pieces
        for x in range(0, 5):
            for y in range(0, 5):
                if self.game.game_state[x, y] != 0:
                    if self.game.game_state[x, y] < 6:
                        if self.game.game_state[x, y] == 3:
                            # red king
                            screen.blit(pieces[1], (25 + x * 95, 265 + y * 95, 90, 90))
                        else:
                            # red pawn
                            screen.blit(pieces[0], (25 + x * 95, 265 + y * 95, 90, 90))
                    else:
                        if self.game.game_state[x, y] == 8:
                            # blue king
                            screen.blit(pieces[3], (25 + x * 95, 265 + y * 95, 90, 90))
                        else:
                            # blue pawn
                            screen.blit(pieces[2], (25 + x * 95, 265 + y * 95, 90, 90))

        # render
        self.screen.blit(pygame.transform.smoothscale(screen, SCREENRECT.size), (0, 0))
        pygame.display.flip()
