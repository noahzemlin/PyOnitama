import pygame

from src.components.board import draw_board
from src.components.card import Card
# constants
from src.interfaces.game_state import Piece, GameState
from src.interfaces.interface_state import InterfaceState

SCREEN_SCALE = 0.8
SCREENRECT = pygame.Rect(0, 0, int(1000 * SCREEN_SCALE), int(1000 * SCREEN_SCALE))


class Screen:

    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.running = True

        self.selected_piece = (-1, -1)
        self.selected_card = -1

        self.interface_state = InterfaceState(game_state)

        Card.SCREEN_SCALE = SCREEN_SCALE

        self.cards = [
            Card(20, 790),
            Card(270, 790),
            Card(550, 440),
            Card(20, 90),
            Card(270, 90)
        ]

        pygame.init()
        pygame.display.set_caption('PyOnitama')

        best_color_depth = pygame.display.mode_ok(SCREENRECT.size, 0, 32)
        self.screen = pygame.display.set_mode(SCREENRECT.size, 0, best_color_depth)
        self.pieces = [pygame.image.load("assets/" + filename).convert_alpha() for filename in
                       ['red_pawn.png', 'red_king.png', 'blue_pawn.png', 'blue_king.png']]

        self.FONT = pygame.font.Font('freesansbold.ttf', 24)

    def play(self):
        pass

    def update(self):
        screen = pygame.Surface((1000, 1000))
        pieces = self.pieces

        # render
        screen.fill((255, 255, 255))
        draw_board(screen, self.game_state, self.interface_state)

        # draw whose turn it is
        if self.game_state.winner == Piece.NONE:
            if self.game_state.current_player == Piece.BLUE:
                text_surf = self.FONT.render("Blue's turn!", True, (0, 0, 0))
                text_rect = text_surf.get_rect()
                text_rect.center = (220, 960)
            else:
                text_surf = self.FONT.render("Red's turn!", True, (0, 0, 0))
                text_rect = text_surf.get_rect()
                text_rect.center = (220, 40)
        else:
            if self.game_state.winner == Piece.BLUE:
                text_surf = self.FONT.render("Blue Won!", True, (0, 0, 0))
            else:
                text_surf = self.FONT.render("Red Won!", True, (0, 0, 0))
            text_rect = text_surf.get_rect()
            text_rect.center = (220, 40)
        screen.blit(text_surf, text_rect)

        # draw cards
        for i in range(0, 5):
            self.cards[i].draw(i, screen, self.FONT, self.interface_state, self.game_state)

        # draw pieces
        for x in range(0, 5):
            for y in range(0, 5):
                if self.game_state[x, y] != Piece.NONE:
                    if self.game_state[x, y] == Piece.RED_KING:
                        # red king
                        screen.blit(pieces[1], (25 + x * 95, 265 + y * 95, 90, 90))
                    elif self.game_state[x, y] == Piece.RED:
                        # red pawn
                        screen.blit(pieces[0], (25 + x * 95, 265 + y * 95, 90, 90))
                    elif self.game_state[x, y] == Piece.BLUE_KING:
                        # blue king
                        screen.blit(pieces[3], (25 + x * 95, 265 + y * 95, 90, 90))
                    elif self.game_state[x, y] == Piece.BLUE:
                        # blue pawn
                        screen.blit(pieces[2], (25 + x * 95, 265 + y * 95, 90, 90))

        # render
        self.screen.blit(pygame.transform.smoothscale(screen, SCREENRECT.size), (0, 0))
        pygame.display.flip()
